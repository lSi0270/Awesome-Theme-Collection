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
    "metal_dark.jpg",
    "metal_light.jpg",
}

WALLPAPER_FAMILY = {
    "flat_leather_shadows": "leather",
    "flat_leather": "leather",
    "leather_shadows": "leather",
    "leather": "leather",
    "flat_metal_shadows": "metal",
    "flat_metal": "metal",
    "metal_shadows": "metal",
    "metal": "metal",
}


def _file_hash(path: Path) -> str:
    """Calculate the SHA-256 hash of a file."""

    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def _load_manifest(path: Path) -> dict[str, Any]:
    """Load the manifest of managed files."""

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

    return data


def _save_manifest(path: Path, data: dict[str, Any]) -> None:
    """Save the managed-file manifest atomically."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(".tmp")

    temporary_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(path)


def _validate_sources(
    themes_source: Path,
    wallpaper_source: Path,
) -> None:
    """Validate all required source files."""

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
) -> None:
    """Install, update or remove a managed file."""

    filename = source.name
    previous_hash = managed.get(filename)

    if not selected:
        if previous_hash is None:
            return

        if not target.exists():
            managed.pop(filename, None)
            return

        if target.is_file() and _file_hash(target) == previous_hash:
            target.unlink()
            managed.pop(filename, None)
            _LOGGER.info("Datei entfernt: %s", filename)
        else:
            managed.pop(filename, None)
            _LOGGER.warning(
                "Datei %s wurde verändert und bleibt erhalten.",
                filename,
            )

        return

    source_hash = _file_hash(source)

    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        managed[filename] = source_hash
        _LOGGER.info("Datei installiert: %s", filename)
        return

    if not target.is_file():
        raise OSError(
            f"Installationsziel ist keine reguläre Datei: {target}"
        )

    target_hash = _file_hash(target)

    if previous_hash is None:
        if target_hash == source_hash:
            managed[filename] = source_hash
        else:
            _LOGGER.warning(
                "Datei %s existiert bereits und wird nicht "
                "überschrieben, da ihre Herkunft unbekannt ist.",
                filename,
            )
        return

    if target_hash != previous_hash:
        managed.pop(filename, None)
        _LOGGER.warning(
            "Datei %s wurde manuell verändert und wird nicht "
            "überschrieben.",
            filename,
        )
        return

    if target_hash != source_hash:
        shutil.copy2(source, target)
        _LOGGER.info("Datei aktualisiert: %s", filename)

    managed[filename] = source_hash


def _sync_assets(
    themes_source: Path,
    wallpaper_source: Path,
    themes_target: Path,
    wallpaper_target: Path,
    manifest_path: Path,
    selected_themes: list[str],
) -> None:
    """Synchronize the selected themes and required wallpapers."""

    _validate_sources(themes_source, wallpaper_source)

    unknown_themes = set(selected_themes) - set(THEMES)
    if unknown_themes:
        raise ValueError(
            f"Unbekannte Theme-Auswahl: {sorted(unknown_themes)}"
        )

    manifest = _load_manifest(manifest_path)
    managed_themes = manifest["themes"]
    managed_wallpapers = manifest["wallpapers"]

    for key, filename in THEMES.items():
        _sync_file(
            themes_source / filename,
            themes_target / filename,
            managed_themes,
            selected=key in selected_themes,
        )

    required_families = {
        WALLPAPER_FAMILY[key] for key in selected_themes
    }

    for filename in sorted(WALLPAPERS):
        family = filename.split("_", maxsplit=1)[0]

        _sync_file(
            wallpaper_source / filename,
            wallpaper_target / filename,
            managed_wallpapers,
            selected=family in required_families,
        )

    _save_manifest(
        manifest_path,
        {
            "themes": managed_themes,
            "wallpapers": managed_wallpapers,
        },
    )


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
    wallpaper_target = Path(hass.config.path("www", "wallpaper"))
    manifest_path = Path(
        hass.config.path(
            ".storage",
            "awesome_theme_collection_manifest.json",
        )
    )

    selected_themes = entry.options.get("themes", list(THEMES))

    try:
        await hass.async_add_executor_job(
            _sync_assets,
            themes_source,
            wallpaper_source,
            themes_target,
            wallpaper_target,
            manifest_path,
            selected_themes,
        )
    except (OSError, ValueError) as err:
        _LOGGER.exception(
            "Installation der Awesome Theme Collection fehlgeschlagen"
        )
        raise HomeAssistantError(
            "Die Themes konnten nicht vollständig synchronisiert werden. "
            "Bitte prüfe die Quelldateien und Schreibrechte."
        ) from err

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
        "Awesome Theme Collection eingerichtet: %s von %s Themes.",
        len(selected_themes),
        len(THEMES),
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload the integration."""

    return True
