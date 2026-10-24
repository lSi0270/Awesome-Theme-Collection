
"""Awesome Theme Collection for Home Assistant."""

from __future__ import annotations

import hashlib
import json
import logging
import re
import shutil
from pathlib import Path
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

DOMAIN = "awesome_theme_collection"
TRANSPARENT_WALLPAPER = "transparent.png"

_LOGGER = logging.getLogger(__name__)

METAL_COLOR_DEFAULTS = {
    "dashboard_color_metal_dark": (
        "linear-gradient(rgba(16, 21, 28, 0.4), "
        "rgba(16, 21, 28, 0.4))"
    ),
    "dashboard_color_metal_light": (
        "linear-gradient(rgba(224, 224, 224, 0.5), "
        "rgba(224, 224, 224, 0.5))"
    ),
    "popup_color_metal_dark": (
        "linear-gradient(rgba(16, 21, 28, 0.4), "
        "rgba(16, 21, 28, 0.4))"
    ),
    "popup_color_metal_light": (
        "linear-gradient(rgba(224, 224, 224, 0.5), "
        "rgba(224, 224, 224, 0.5))"
    ),
}

LEATHER_COLOR_DEFAULTS = {
    "dashboard_color_leather_dark": (
        "linear-gradient(rgba(16, 21, 28, 0.4), "
        "rgba(16, 21, 28, 0.4))"
    ),
    "dashboard_color_leather_light": (
        "linear-gradient(rgba(224, 224, 224, 0.8), "
        "rgba(224, 224, 224, 0.8))"
    ),
    "popup_color_leather_dark": (
        "linear-gradient(rgba(16, 21, 28, 0.4), "
        "rgba(16, 21, 28, 0.4))"
    ),
    "popup_color_leather_light": (
        "linear-gradient(rgba(224, 224, 224, 0.8), "
        "rgba(224, 224, 224, 0.8))"
    ),
}

THEME_GROUPS: dict[str, dict[str, Any]] = {
    "metal": {
        "enabled_key": "metal_enabled",
        "options_key": "themes_metal",
        "themes": {
            "flat_metal_shadows": "Awesome-Flat-Metal-Shadows-UIX.yaml",
            "flat_metal": "Awesome-Flat-Metal-UIX.yaml",
            "metal_shadows": "Awesome-Metal-Shadows-UIX.yaml",
            "metal": "Awesome-Metal-UIX.yaml",
        },
        "wallpapers": {
            "metal_dark.jpg",
            "metal2_dark.jpg",
            "metal3_dark.jpg",
            "metal4_dark.jpg",
            "metal_light.jpg",
            "metal2_light.jpg",
            "metal3_light.jpg",
            "metal4_light.jpg",
        },
        "background_keys": (
            "background_metal_dark",
            "background_metal_light",
            "background_popup_metal_dark",
            "background_popup_metal_light",
        ),
        "colors": METAL_COLOR_DEFAULTS,
    },
    "leather": {
        "enabled_key": "leather_enabled",
        "options_key": "themes_leather",
        "themes": {
            "flat_leather_shadows": "Awesome-Flat-Leather-Shadows-UIX.yaml",
            "flat_leather": "Awesome-Flat-Leather-UIX.yaml",
            "leather_shadows": "Awesome-Leather-Shadows-UIX.yaml",
            "leather": "Awesome-Leather-UIX.yaml",
        },
        "wallpapers": {
            "leather_dark.jpg",
            "leather2_dark.jpg",
            "leather3_dark.jpg",
            "leather_light.jpg",
            "leather2_light.jpg",
            "leather3_light.jpg",
        },
        "background_keys": (
            "background_leather_dark",
            "background_leather_light",
            "background_popup_leather_dark",
            "background_popup_leather_light",
        ),
        "colors": LEATHER_COLOR_DEFAULTS,
    },
}

THEMES = {
    **THEME_GROUPS["metal"]["themes"],
    **THEME_GROUPS["leather"]["themes"],
}

WALLPAPERS = (
    THEME_GROUPS["metal"]["wallpapers"]
    | THEME_GROUPS["leather"]["wallpapers"]
)

DEFAULT_OPTIONS: dict[str, Any] = {
    "background_metal_dark": "/local/wallpaper/metal2_dark.jpg",
    "background_metal_light": "/local/wallpaper/metal2_light.jpg",
    "background_popup_metal_dark": "/local/wallpaper/metal2_dark.jpg",
    "background_popup_metal_light": "/local/wallpaper/metal2_light.jpg",
    "background_leather_dark": "/local/wallpaper/leather_dark.jpg",
    "background_leather_light": "/local/wallpaper/leather_light.jpg",
    "background_popup_leather_dark": "/local/wallpaper/leather_dark.jpg",
    "background_popup_leather_light": "/local/wallpaper/leather_light.jpg",
    **METAL_COLOR_DEFAULTS,
    **LEATHER_COLOR_DEFAULTS,
    "section_column_gap_metal": 32,
    "section_row_gap_metal": 24,
    "section_border_color_metal": "rgba(130, 130, 130, 0.2)",
    "section_column_gap_leather": 32,
    "section_row_gap_leather": 24,
    "section_border_color_leather": "rgba(130, 130, 130, 0.2)",
}

BACKGROUND_KEYS = tuple(
    key
    for group in THEME_GROUPS.values()
    for key in group["background_keys"]
)

COLOR_KEYS = tuple(
    key
    for group in THEME_GROUPS.values()
    for key in group["colors"]
)

RGBA_PATTERN = re.compile(
    r"rgba\(\s*"
    r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\s*,\s*"
    r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\s*,\s*"
    r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\s*,\s*"
    r"(?:0(?:\.\d+)?|1(?:\.0+)?)"
    r"\s*\)",
    re.IGNORECASE,
)

HEX_COLOR_PATTERN = re.compile(
    r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|"
    r"[0-9a-fA-F]{6}|[0-9a-fA-F]{8})"
)

LINEAR_GRADIENT_PATTERN = re.compile(
    r"^linear-gradient\((.*)\)$",
    re.IGNORECASE | re.DOTALL,
)


def _file_hash(path: Path) -> str:
    """Calculate the SHA-256 hash of a file."""

    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def _content_hash(content: str) -> str:
    """Calculate the SHA-256 hash of generated content."""

    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _load_manifest(path: Path) -> dict[str, Any]:
    """Load and validate the manifest of managed files."""

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

    for category in ("themes", "wallpapers"):
        for filename, digest in data[category].items():
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


def _split_css_arguments(value: str) -> list[str] | None:
    """Split CSS arguments at top-level commas only."""

    arguments: list[str] = []
    depth = 0
    start = 0

    for index, char in enumerate(value):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                return None
        elif char == "," and depth == 0:
            argument = value[start:index].strip()
            if not argument:
                return None
            arguments.append(argument)
            start = index + 1

    if depth != 0:
        return None

    final_argument = value[start:].strip()

    if not final_argument:
        return None

    arguments.append(final_argument)
    return arguments


def _valid_gradient_stop(value: str) -> bool:
    """Validate one HEX or RGBA gradient stop with optional percentage."""

    value = value.strip()
    percentage_pattern = r"(?:\s+(\d+(?:\.\d+)?%))?"

    hex_match = re.fullmatch(
        rf"(#[0-9a-fA-F]{{3}}|#[0-9a-fA-F]{{4}}|"
        rf"#[0-9a-fA-F]{{6}}|#[0-9a-fA-F]{{8}})"
        rf"{percentage_pattern}",
        value,
    )

    if hex_match and HEX_COLOR_PATTERN.fullmatch(hex_match.group(1)):
        return True

    rgba_match = re.fullmatch(
        rf"(rgba\([^()]*\)){percentage_pattern}",
        value,
        re.IGNORECASE,
    )

    return bool(
        rgba_match
        and RGBA_PATTERN.fullmatch(rgba_match.group(1))
    )


def _valid_theme_color(value: Any) -> bool:
    """Validate a HEX color or linear gradient with supported stops."""

    if not isinstance(value, str):
        return False

    value = value.strip()

    if (
        not value
        or any(
            char in value
            for char in ('"', "'", "\\", "\n", "\r", ";", "{", "}")
        )
    ):
        return False

    if HEX_COLOR_PATTERN.fullmatch(value):
        return True

    match = LINEAR_GRADIENT_PATTERN.fullmatch(value)

    if not match:
        return False

    arguments = _split_css_arguments(match.group(1))

    if arguments is None:
        return False

    direction_pattern = re.compile(
        r"(?:"
        r"to\s+(?:(?:left|right|top|bottom)"
        r"(?:\s+(?:left|right|top|bottom))?)"
        r"|[-+]?(?:\d+(?:\.\d*)?|\.\d+)"
        r"(?:deg|grad|rad|turn)"
        r")",
        re.IGNORECASE,
    )

    if arguments and direction_pattern.fullmatch(arguments[0]):
        stops = arguments[1:]
    else:
        stops = arguments

    if len(stops) < 2:
        return False

    return all(_valid_gradient_stop(stop) for stop in stops)

def _validate_options(options: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize all group-specific options."""

    values = {
        key: options.get(key, default)
        for key, default in DEFAULT_OPTIONS.items()
    }

    for key in BACKGROUND_KEYS:
        path = values[key]

        if (
            not isinstance(path, str)
            or not path.startswith("/local/")
            or any(
                char in path
                for char in ('"', "'", "\\", "\n", "\r")
            )
            or ".." in Path(path).parts
            or "?" in path
            or "#" in path
        ):
            raise ValueError(f"Ungültiger Hintergrundpfad: {key}")

    for key in COLOR_KEYS:
        color = values[key]

        if not _valid_theme_color(color):
            raise ValueError(f"Ungültige Theme-Farbe: {key}")

        values[key] = color.strip()

    for key in (
        "section_column_gap_metal",
        "section_row_gap_metal",
        "section_column_gap_leather",
        "section_row_gap_leather",
    ):
        value = values[key]

        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not 0 <= value <= 50
        ):
            raise ValueError(f"Ungültiger Abstand: {key}")

        values[key] = f"{value:g}px"

    for key in (
        "section_border_color_metal",
        "section_border_color_leather",
    ):
        color = values[key]

        if (
            not isinstance(color, str)
            or not RGBA_PATTERN.fullmatch(color)
        ):
            raise ValueError(
                f"Ungültige Abschnitt-Rahmenfarbe: {key}"
            )

    return values


def _validate_sources(
    themes_source: Path,
    wallpaper_source: Path,
) -> None:
    """Validate every required source before changing installed files."""

    if not themes_source.is_dir():
        raise FileNotFoundError(
            f"Theme-Quellverzeichnis fehlt: {themes_source}"
        )

    if not wallpaper_source.is_dir():
        raise FileNotFoundError(
            f"Wallpaper-Quellverzeichnis fehlt: {wallpaper_source}"
        )

    for filename in THEMES.values():
        source = themes_source / filename

        if not source.is_file():
            raise FileNotFoundError(
                f"Theme-Quelldatei fehlt: {source}"
            )

    for filename in WALLPAPERS:
        source = wallpaper_source / filename

        if not source.is_file():
            raise FileNotFoundError(
                f"Wallpaper-Quelldatei fehlt: {source}"
            )

    transparent_source = wallpaper_source / TRANSPARENT_WALLPAPER

    if not transparent_source.is_file():
        raise FileNotFoundError(
            f"Transparentes Wallpaper fehlt: {transparent_source}"
        )


def _render_theme(
    source: Path,
    values: dict[str, Any],
    group: str,
) -> str:
    """Render a theme using validated and normalized options."""

    if group not in THEME_GROUPS:
        raise ValueError(f"Unbekannter Theme-Bereich: {group}")

    content = source.read_text(encoding="utf-8")
    config = THEME_GROUPS[group]

    for key in config["background_keys"]:
        marker = f"ATC_{key.upper()}"

        pattern = re.compile(
            r"url\((['\"])[^'\"]*\1\)"
            + r"(\s*/\*\s*"
            + re.escape(marker)
            + r"\s*\*/)"
        )

        content, count = pattern.subn(
            lambda match: (
                f"url({match.group(1)}{values[key]}{match.group(1)})"
                f"{match.group(2)}"
            ),
            content,
        )

        if count > 4:
            raise ValueError(
                f"Der Marker {marker} kommt zu oft in {source.name} vor."
            )

    suffix = group.upper()

    color_markers = {
        f"dashboard_color_{group}_dark": (
            f"ATC_DASHBOARD_COLOR_{suffix}_DARK"
        ),
        f"dashboard_color_{group}_light": (
            f"ATC_DASHBOARD_COLOR_{suffix}_LIGHT"
        ),
        f"popup_color_{group}_dark": (
            f"ATC_POPUP_COLOR_{suffix}_DARK"
        ),
        f"popup_color_{group}_light": (
            f"ATC_POPUP_COLOR_{suffix}_LIGHT"
        ),
    }

    for key, marker in color_markers.items():
        pattern = re.compile(
            r'(?m)^(\s*[^:\r\n]+:\s*")'
            r'[^"\r\n]*?'
            r'(\s*/\*\s*'
            + re.escape(marker)
            + r'\s*\*/)'
        )

        content, count = pattern.subn(
            lambda match: (
                f"{match.group(1)}"
                f"{values[key]}"
                f"{match.group(2)}"
            ),
            content,
        )

        if count > 4:
            raise ValueError(
                f"Der Marker {marker} kommt zu oft in {source.name} vor."
            )

    gap_markers = {
        f"section_column_gap_{group}": (
            "ha-view-sections-column-gap",
            f"ATC_SECTION_COLUMN_GAP_{suffix}",
        ),
        f"section_row_gap_{group}": (
            "ha-view-sections-row-gap",
            f"ATC_SECTION_ROW_GAP_{suffix}",
        ),
    }

    for key, (yaml_key, marker) in gap_markers.items():
        pattern = re.compile(
            rf"(?m)^(\s*{re.escape(yaml_key)}:\s*)"
            rf"[^#\r\n]*"
            rf"(\s+#\s*{re.escape(marker)}\s*)$"
        )

        content, count = pattern.subn(
            lambda match: (
                f"{match.group(1)}{values[key]}{match.group(2)}"
            ),
            content,
        )

        if count > 2:
            raise ValueError(
                f"Der Marker {marker} kommt zu oft in {source.name} vor."
            )

    border_marker = f"ATC_SECTION_BORDER_COLOR_{suffix}"

    border_pattern = re.compile(
        r"(border:\s*1px\s+solid\s+)"
        r".*?"
        + r"(\s*/\*\s*"
        + re.escape(border_marker)
        + r"\s*\*/\s*;)"
    )

    content, border_count = border_pattern.subn(
        lambda match: (
            f"{match.group(1)}"
            f"{values[f'section_border_color_{group}']}"
            f"{match.group(2)}"
        ),
        content,
    )

    if border_count > 2:
        raise ValueError(
            f"Der Marker {border_marker} kommt zu oft in {source.name} vor."
        )

    return content

def _write_content_atomic(target: Path, content: str) -> None:
    """Write generated content atomically."""

    target.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = target.with_suffix(target.suffix + ".tmp")

    try:
        temporary_path.write_text(content, encoding="utf-8")
        temporary_path.replace(target)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def _sync_file(
    source: Path,
    target: Path,
    managed: dict[str, str],
    *,
    selected: bool,
    content: str | None = None,
) -> bool:
    """Install, update or safely remove an integration-managed file."""

    filename = source.name
    previous_hash = managed.get(filename)

    if target.is_dir():
        raise OSError(
            f"Installationsziel ist ein Verzeichnis: {target}"
        )

    if not selected:
        if previous_hash is None:
            return False

        if not target.exists():
            managed.pop(filename, None)
            return False

        if not target.is_file():
            raise OSError(
                f"Installationsziel ist keine reguläre Datei: {target}"
            )

        if _file_hash(target) != previous_hash:
            _LOGGER.warning(
                "Datei wurde manuell verändert und wird nicht gelöscht: %s",
                filename,
            )
            managed.pop(filename, None)
            return False

        target.unlink()
        managed.pop(filename, None)
        _LOGGER.info("Verwaltete Datei entfernt: %s", filename)
        return True

    if not source.is_file():
        raise FileNotFoundError(f"Quelldatei fehlt: {source}")

    source_hash = (
        _content_hash(content)
        if content is not None
        else _file_hash(source)
    )

    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists():
        if not target.is_file():
            raise OSError(
                f"Installationsziel ist keine reguläre Datei: {target}"
            )

        target_hash = _file_hash(target)

        if target_hash == source_hash:
            managed[filename] = source_hash
            return False

        if previous_hash is None:
            _LOGGER.warning(
                "Vorhandene, nicht verwaltete Datei wird nicht "
                "überschrieben: %s",
                filename,
            )
            return False

        if target_hash != previous_hash:
            _LOGGER.warning(
                "Datei wurde manuell verändert und wird nicht "
                "überschrieben: %s",
                filename,
            )
            managed.pop(filename, None)
            return False

        if content is None:
            shutil.copy2(source, target)
        else:
            _write_content_atomic(target, content)

        managed[filename] = source_hash
        _LOGGER.info("Datei aktualisiert: %s", filename)
        return True

    if content is None:
        shutil.copy2(source, target)
    else:
        _write_content_atomic(target, content)

    managed[filename] = source_hash
    _LOGGER.info("Datei installiert: %s", filename)
    return True


def _selected_themes(options: dict[str, Any]) -> set[str]:
    """Return enabled themes, migrating the legacy theme selection."""

    legacy_themes = options.get("themes", list(THEMES))

    if (
        not isinstance(legacy_themes, list)
        or any(not isinstance(key, str) for key in legacy_themes)
    ):
        raise ValueError("Die bisherige Theme-Auswahl ist ungültig.")

    if len(legacy_themes) != len(set(legacy_themes)):
        raise ValueError(
            "Die bisherige Theme-Auswahl enthält Duplikate."
        )

    unknown_legacy = set(legacy_themes) - set(THEMES)

    if unknown_legacy:
        raise ValueError(
            f"Unbekannte bisherige Themes: {sorted(unknown_legacy)}"
        )

    selected: set[str] = set()

    for group, config in THEME_GROUPS.items():
        enabled = options.get(config["enabled_key"], True)

        if not isinstance(enabled, bool):
            raise ValueError(
                f"Ungültiger Aktivierungswert: {config['enabled_key']}"
            )

        group_themes = options.get(config["options_key"])

        if group_themes is None:
            group_themes = [
                key
                for key in config["themes"]
                if key in legacy_themes
            ]

        if (
            not isinstance(group_themes, list)
            or any(not isinstance(key, str) for key in group_themes)
        ):
            raise ValueError(
                f"Die Theme-Auswahl für {group} ist ungültig."
            )

        if len(group_themes) != len(set(group_themes)):
            raise ValueError(
                f"Die Theme-Auswahl für {group} enthält Duplikate."
            )

        unknown = set(group_themes) - set(config["themes"])

        if unknown:
            raise ValueError(
                f"Unbekannte Themes für {group}: {sorted(unknown)}"
            )

        if enabled:
            selected.update(group_themes)

    return selected


def _sync_assets(
    themes_source: Path,
    wallpaper_source: Path,
    themes_target: Path,
    wallpaper_target: Path,
    manifest_path: Path,
    options: dict[str, Any],
) -> bool:
    """Synchronize enabled theme groups and their wallpapers."""

    _validate_sources(themes_source, wallpaper_source)

    selected_themes = _selected_themes(options)
    values = _validate_options(options)

    manifest = _load_manifest(manifest_path)
    managed_themes = manifest["themes"]
    managed_wallpapers = manifest["wallpapers"]

    changed = False

    for group, config in THEME_GROUPS.items():
        enabled = options.get(config["enabled_key"], True)

        for key, filename in config["themes"].items():
            source = themes_source / filename
            selected = enabled and key in selected_themes

            rendered_content = (
                _render_theme(source, values, group)
                if selected
                else None
            )

            changed |= _sync_file(
                source,
                themes_target / filename,
                managed_themes,
                selected=selected,
                content=rendered_content,
            )

    # The transparent wallpaper is a permanent system asset.
    selected_wallpapers: set[str] = {TRANSPARENT_WALLPAPER}

    for config in THEME_GROUPS.values():
        if options.get(config["enabled_key"], True):
            selected_wallpapers.update(config["wallpapers"])

    all_wallpapers = WALLPAPERS | {TRANSPARENT_WALLPAPER}

    for filename in sorted(all_wallpapers):
        source = wallpaper_source / filename

        changed |= _sync_file(
            source,
            wallpaper_target / filename,
            managed_wallpapers,
            selected=filename in selected_wallpapers,
        )

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
    wallpaper_target = Path(hass.config.path("www", "wallpaper"))

    manifest_path = Path(
        hass.config.path(
            ".storage",
            "awesome_theme_collection_manifest.json",
        )
    )

    options = dict(entry.options)

    try:
        changed = await hass.async_add_executor_job(
            _sync_assets,
            themes_source,
            wallpaper_source,
            themes_target,
            wallpaper_target,
            manifest_path,
            options,
        )
    except (OSError, ValueError, TypeError) as err:
        _LOGGER.exception(
            "Installation der Awesome Theme Collection fehlgeschlagen"
        )
        raise HomeAssistantError(
            "Die Themes konnten nicht vollständig synchronisiert werden. "
            "Bitte prüfe die Asset-Dateien, Optionen und Schreibrechte."
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

    selected = _selected_themes(options)

    _LOGGER.info(
        "Awesome Theme Collection eingerichtet: %s von %s Themes. "
        "Dateien geändert: %s",
        len(selected),
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
