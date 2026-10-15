"""Awesome Theme Collection for Home Assistant."""

from __future__ import annotations

import hashlib
import json
import logging
import shutil
from pathlib import Path
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

DOMAIN = "awesome_theme_collection"

_LOGGER = logging.getLogger(__name__)

THEMES = {
    "flat_leather_shadows": "Awesome-Flat-Leather-Shadows-UIX.yaml",
    "flat_leather": "Awesome-Flat-Leather-UIX.yaml",
    "flat_metal_shadows": "Awesome-Flat-Metal-Shadows-UIX.yaml",
    "flat_metal": "Awesome-Flat-Metal-UIX.yaml",
    "leather_shadows": "Awesome-Leather-Shadows-UIX.yaml",
    "leather": "Awesome-Leather-UIX.yaml",
    "metal_shadows": "Awesome-Metal-Shadows-UIX.yaml",
    "metal": "Awesome-Metal-UIX.yaml",
}

WALLPAPERS = {
    "leather_dark.jpg",
    "leather_light.jpg",
    "metal2_dark.jpg",
    "metal2_light.jpg",
}


def _file_hash(path: Path) -> str:
    """Calculate the SHA-256 hash of a file."""

    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def _load_manifest(path: Path) -> dict[str, Any]:
    """Load the manifest of integration-managed files."""

    if not path.exists():
        return {"themes": {}, "wallpapers": {}}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        raise ValueError(
            "Die Dateiverwaltung konnte nicht gelesen werden."
        ) from err

    if (
        not isinstance(data, dict)
        or not isinstance(data.get("themes"), dict)
        or not isinstance(data.get("wallpapers"), dict)
    ):
        raise ValueError(
            "Die Dateiverwaltung hat ein ungültiges Format."
        )

    for section in ("themes", "wallpapers"):
        for filename, digest in data[section].items():
            if (
                not isinstance(filename, str)
                or Path(filename).name != filename
                or not isinstance(digest, str)
                or len(digest) != 64
                or any(
                    char not in "0123456789abcdef"
                    for char in digest
                )
            ):
                raise ValueError(
                    "Die Dateiverwaltung enthält ungültige Einträge."
                )

    return data


def _save_manifest(path: Path, data: dict[str, Any]) -> None:
    """Save the manifest atomically."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(".tmp")

    try:
        temporary_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        temporary_path.replace(path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def _validate_sources(
    themes_source: Path,
    wallpaper_source: Path,
) -> None:
    """Validate all required source files before synchronization."""

    if not themes_source.is_dir():
        raise FileNotFoundError(
            f"Theme-Verzeichnis fehlt: {themes_source}"
        )

    if not wallpaper_source.is_dir():
        raise FileNotFoundError(
            f"Wallpaper-Verzeichnis fehlt: {wallpaper_source}"
        )

    for filename in THEMES.values():
        if not (themes_source / filename).is_file():
            raise FileNotFoundError(
                f"Theme-Datei fehlt: {filename}"
            )

    for filename in WALLPAPERS:
        if not (wallpaper_source / filename).is_file():
            raise FileNotFoundError(
                f"Wallpaper-Datei fehlt: {filename}"
            )


def _sync_file(
    source: Path,
    target: Path,
    managed: dict[str, str],
    *,
    selected: bool,
) -> bool:
    """Install, update or remove a file managed by this integration.

    Returns True if the target file was installed, updated or removed.
    """

    filename = source.name

    if not selected:
        # These filenames are explicitly managed by this integration.
        # Remove deselected themes even if an older installation did
        # not yet record them in the manifest.
        if target.is_dir():
            raise OSError(
                f"Installationsziel ist ein Verzeichnis: {target}"
            )

        if target.exists():
            if not target.is_file():
                raise OSError(
                    f"Installationsziel ist keine reguläre Datei: {target}"
                )

            target.unlink()
            _LOGGER.info("Datei entfernt: %s", filename)
            changed = True
        else:
            changed = False

        managed.pop(filename, None)
        return changed

    if not source.is_file():
        raise FileNotFoundError(
            f"Quelldatei fehlt: {source}"
        )

    source_hash = _file_hash(source)

    if target.exists() and not target.is_file():
        raise OSError(
            f"Installationsziel ist keine reguläre Datei: {target}"
        )

    target.parent.mkdir(parents=True, exist_ok=True)

    if target.is_file():
        target_hash = _file_hash(target)

        if target_hash == source_hash:
            # The file is already current. Record it as managed so
            # that subsequent updates and deselection work correctly.
            managed[filename] = source_hash
            return False

        # The source repository is authoritative for these filenames.
        # This also repairs files left behind by older versions.
        shutil.copy2(source, target)
        managed[filename] = source_hash

        _LOGGER.info("Datei aktualisiert: %s", filename)
        return True

    shutil.copy2(source, target)
    managed[filename] = source_hash

    _LOGGER.info("Datei installiert: %s", filename)
    return True


def _sync_assets(
    themes_source: Path,
    wallpaper_source: Path,
    themes_target: Path,
    wallpaper_target: Path,
    manifest_path: Path,
    selected_themes: list[str],
) -> bool:
    """Synchronize selected themes and all wallpapers.

    Wallpapers remain installed regardless of the selected themes.
    Returns True if any theme or wallpaper changed.
    """

    _validate_sources(themes_source, wallpaper_source)

    if (
        not isinstance(selected_themes, list)
        or any(not isinstance(key, str) for key in selected_themes)
    ):
        raise ValueError("Die Theme-Auswahl ist ungültig.")

    if len(selected_themes) != len(set(selected_themes)):
        raise ValueError(
            "Die Theme-Auswahl enthält Duplikate."
        )

    unknown_themes = set(selected_themes) - set(THEMES)

    if unknown_themes:
        raise ValueError(
            f"Unbekannte Theme-Auswahl: {sorted(unknown_themes)}"
        )

    manifest = _load_manifest(manifest_path)
    managed_themes = manifest["themes"]
    managed_wallpapers = manifest["wallpapers"]

    changed = False

    # Install, update or remove every known theme according to
    # the current selection.
    for key, filename in THEMES.items():
        changed |= _sync_file(
            themes_source / filename,
            themes_target / filename,
            managed_themes,
            selected=key in selected_themes,
        )

    # Keep all wallpapers installed and update them when necessary.
    for filename in sorted(WALLPAPERS):
        changed |= _sync_file(
            wallpaper_source / filename,
            wallpaper_target / filename,
            managed_wallpapers,
            selected=True,
        )

    # Persist the manifest only after the file synchronization succeeds.
    _save_manifest(
        manifest_path,
        {
            "themes": managed_themes,
            "wallpapers": managed_wallpapers,
        },
    )

    return changed


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Awesome Theme Collection."""

    integration_dir = Path(__file__).parent
    assets_dir = integration_dir / "assets"

    themes_source = assets_dir / "themes"
    wallpaper_source = assets_dir / "wallpaper"

    themes_target = Path(hass.config.path("themes"))
    wallpaper_target = Path(
        hass.config.path("www", "wallpaper")
    )

    manifest_path = Path(
        hass.config.path(
            ".storage",
            "awesome_theme_collection_manifest.json",
        )
    )

    selected_themes = entry.options.get(
        "themes",
        list(THEMES),
    )

    try:
        changed = await hass.async_add_executor_job(
            _sync_assets,
            themes_source,
            wallpaper_source,
            themes_target,
            wallpaper_target,
            manifest_path,
            selected_themes,
        )
    except (OSError, ValueError, TypeError) as err:
        _LOGGER.exception(
            "Installation der Awesome Theme Collection fehlgeschlagen"
        )
        raise HomeAssistantError(
            "Die Themes konnten nicht vollständig synchronisiert werden. "
            "Bitte prüfe die Asset-Dateien, die Dateiverwaltung und "
            "die Schreibrechte."
        ) from err

    # Reload the frontend themes after every successful synchronization,
    # including a synchronization where all files were already current.
    try:
        await hass.services.async_call(
            "frontend",
            "reload_themes",
            {},
            blocking=True,
        )
    except HomeAssistantError:
        _LOGGER.exception(
            "Die Dateien wurden synchronisiert, aber die Themes "
            "konnten nicht neu geladen werden."
        )

    _LOGGER.info(
        "Awesome Theme Collection eingerichtet: %s von %s Themes. "
        "Dateien geändert: %s",
        len(selected_themes),
        len(THEMES),
        changed,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload the integration."""

    return True