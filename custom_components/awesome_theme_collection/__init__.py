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

FONT_SIZE_DEFAULTS: dict[str, int] = {
    "xs": 11,
    "s": 12,
    "m": 14,
    "l": 16,
    "xl": 18,
    "2xl": 20,
    "3xl": 24,
    "4xl": 28,
    "5xl": 36,
}

FONT_SIZE_VARIABLES: dict[str, str] = {
    "xs": "ha-font-size-xs",
    "s": "ha-font-size-s",
    "m": "ha-font-size-m",
    "l": "ha-font-size-l",
    "xl": "ha-font-size-xl",
    "2xl": "ha-font-size-2xl",
    "3xl": "ha-font-size-3xl",
    "4xl": "ha-font-size-4xl",
    "5xl": "ha-font-size-5xl",
}

TEXT_COLOR_DEFAULTS: dict[str, dict[str, str]] = {
    "metal": {
        "primary_text_color_dark": "#E7EDF5",
        "secondary_text_color_dark": "#ADB9C7",
        "disabled_text_color_dark": "#636366",
        "heading_title_color_dark": "#FFBB88",
        "primary_text_color_light": "#202020",
        "secondary_text_color_light": "#373737",
        "disabled_text_color_light": "#8E8E8E",
        "heading_title_color_light": "#221100",
    },
    "leather": {
        "primary_text_color_dark": "#E7EDF5",
        "secondary_text_color_dark": "#ADB9C7",
        "disabled_text_color_dark": "#636366",
        "heading_title_color_dark": "#FFBB88",
        "primary_text_color_light": "#202020",
        "secondary_text_color_light": "#373737",
        "disabled_text_color_light": "#8E8E8E",
        "heading_title_color_light": "#221100",
    },
}

TEXT_COLOR_VARIABLES: dict[str, str] = {
    "primary_text_color_dark": "primary-text-color",
    "secondary_text_color_dark": "secondary-text-color",
    "disabled_text_color_dark": "disabled-text-color",
    "heading_title_color_dark": "ha-heading-card-title-color",
    "primary_text_color_light": "primary-text-color",
    "secondary_text_color_light": "secondary-text-color",
    "disabled_text_color_light": "disabled-text-color",
    "heading_title_color_light": "ha-heading-card-title-color",
}

ICON_DEFAULTS: dict[str, int] = {"icon_size": 24}
ICON_LIMITS: dict[str, tuple[int, int, int]] = {
    "icon_size": (16, 36, 1),
}
ICON_OFF_COLOR_DEFAULTS: dict[str, str] = {
    "icon_off_color_dark": "#929292",
    "icon_off_color_light": "#626262",
}

PRIMARY_COLOR_DEFAULTS: dict[str, str] = {
    "primary_color_dark": "#0A5CFF",
    "accent_color_dark": "#FFB200",
    "primary_color_light": "#0A5CFF",
    "accent_color_light": "#BA4B00",
}
CARD_BORDER_RADIUS_DEFAULT = 10

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
    **{
        f"font_size_{size}_{group}": default
        for group in ("metal", "leather")
        for size, default in FONT_SIZE_DEFAULTS.items()
    },
    **{
        f"{key}_{group}": value
        for group, colors in TEXT_COLOR_DEFAULTS.items()
        for key, value in colors.items()
    },
    **{
        f"{key}_{group}": value
        for group in ("metal", "leather")
        for key, value in ICON_DEFAULTS.items()
    },
    **{
        f"{key}_{group}": value
        for group in ("metal", "leather")
        for key, value in ICON_OFF_COLOR_DEFAULTS.items()
    },
    **{
        f"{key}_{group}": value
        for group in ("metal", "leather")
        for key, value in PRIMARY_COLOR_DEFAULTS.items()
    },
    "card_border_radius_metal": CARD_BORDER_RADIUS_DEFAULT,
    "card_border_radius_leather": CARD_BORDER_RADIUS_DEFAULT,
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

TEXT_COLOR_KEYS = tuple(
    f"{key}_{group}"
    for group, colors in TEXT_COLOR_DEFAULTS.items()
    for key in colors
)

ICON_KEYS = tuple(
    f"{key}_{group}"
    for group in ("metal", "leather")
    for key in ICON_DEFAULTS
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

    for key in TEXT_COLOR_KEYS:
        color = values[key]

        if (
            not isinstance(color, str)
            or not re.fullmatch(r"#[0-9a-fA-F]{6}", color)
        ):
            raise ValueError(f"Ungültige Textfarbe: {key}")

        values[key] = color.upper()

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

    for group in ("metal", "leather"):
        for size, default in FONT_SIZE_DEFAULTS.items():
            key = f"font_size_{size}_{group}"
            value = values[key]

            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or int(value) != value
                or not 8 <= value <= 46
            ):
                raise ValueError(
                    f"Ungültige Schriftgröße: {key}"
                )

            values[key] = int(value)

    for group in ("metal", "leather"):
        for key, (minimum, maximum, step) in ICON_LIMITS.items():
            option_key = f"{key}_{group}"
            value = values[option_key]
            if (isinstance(value, bool) or not isinstance(value, (int, float))
                    or not minimum <= value <= maximum or int(value) != value):
                raise ValueError(f"Ungültige Icon-Einstellung: {option_key}")
            values[option_key] = int(value)
        for key in ICON_OFF_COLOR_DEFAULTS:
            option_key = f"{key}_{group}"
            value = values[option_key]
            if not isinstance(value, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", value.strip()):
                raise ValueError(f"Ungültige Icon-Farbe: {option_key}")
            values[option_key] = value.strip().upper()

    for group in ("metal", "leather"):
        for key in PRIMARY_COLOR_DEFAULTS:
            option_key = f"{key}_{group}"
            color = values[option_key]
            if (
                not isinstance(color, str)
                or not re.fullmatch(r"#[0-9A-Fa-f]{6}", color.strip())
            ):
                raise ValueError(f"Ungültige Primär-/Akzentfarbe: {option_key}")
            values[option_key] = color.strip().upper()

        radius_key = f"card_border_radius_{group}"
        radius = values[radius_key]
        if (
            isinstance(radius, bool)
            or not isinstance(radius, (int, float))
            or int(radius) != radius
            or not 0 <= radius <= 28
        ):
            raise ValueError(f"Ungültiger Karten-Radius: {radius_key}")
        values[radius_key] = int(radius)

    return values

def _replace_atc_value(
    content: str,
    marker: str,
    value: str,
) -> tuple[str, int]:
    """
    Replace the value immediately before an ATC marker.

    The CSS variable name is deliberately ignored.
    The property name and ATC comment remain unchanged.
    Supports YAML comments and CSS comments.
    """
    pattern = re.compile(
        r"(?m)^"
        r"([ \t]*[^:\r\n]+:[ \t]*)"
        r".*?"
        r"([ \t]*(?:"
        r"\#[ \t]*"
        r"|/\*[ \t]*"
        r")"
        + re.escape(marker)
        + r"(?:[ \t]*\*/)?"
        r"[^\r\n]*)$"
    )

    return pattern.subn(
        lambda match: (
            f'{match.group(1)}"{value}"{match.group(2)}'
        ),
        content,
    )


def _replace_atc_rgba(
    content: str,
    marker: str,
    value: str,
) -> tuple[str, int]:
    """Replace only the RGBA color before an ATC CSS comment.

    Keep the CSS property and every declaration before the color intact,
    e.g. ``border: 1px solid rgba(...) /* ATC_... */``.
    The replacement is deliberately unquoted.
    """
    pattern = re.compile(
        r"(rgba\([^()\r\n]*\))"
        r"([ \t]*/\*[ \t]*"
        + re.escape(marker)
        + r"[ \t]*\*/)" ,
        re.IGNORECASE,
    )

    return pattern.subn(
        lambda match: f"{value}{match.group(2)}",
        content,
    )


def _replace_atc_gradient(
    content: str,
    marker: str,
    value: str,
) -> tuple[str, int]:
    """
    Replace only the linear-gradient before an ATC marker.

    Preserve the surrounding YAML string, CSS comments
    and any additional CSS declarations on the same line.
    """
    pattern = re.compile(
        r"(linear-gradient\((?:[^()]|\([^()]*\))*\))"
        r"(\s*/\*[ \t]*"
        + re.escape(marker)
        + r"[ \t]*\*/)",
        re.IGNORECASE,
    )

    return pattern.subn(
        lambda match: f"{value}{match.group(2)}",
        content,
    )


def _replace_atc_background(
    content: str,
    marker: str,
    value: str,
) -> tuple[str, int]:
    """
    Replace only the URL inside url() before an ATC marker.

    Preserve url(), its original quote style and the ATC comment.
    """
    pattern = re.compile(
        r"(url\(\s*)(['\"]?)"
        r"[^'\")\r\n]*"
        r"(['\"]?\s*\))"
        r"(\s*/\*[ \t]*"
        + re.escape(marker)
        + r"[ \t]*\*/)"
    )

    return pattern.subn(
        lambda match: (
            f"{match.group(1)}"
            f"{match.group(2)}"
            f"{value}"
            f"{match.group(3)}"
            f"{match.group(4)}"
        ),
        content,
    )


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
    """Render a theme using ATC markers as the only lookup criteria."""
    if group not in THEME_GROUPS:
        raise ValueError(f"Unbekannter Theme-Bereich: {group}")

    content = source.read_text(encoding="utf-8")
    suffix = group.upper()

    # Hintergrundbilder.
    for key in THEME_GROUPS[group]["background_keys"]:
        marker = f"ATC_{key.upper()}"

        content, count = _replace_atc_background(
            content,
            marker,
            values[key],
        )

        if count > 4:
            raise ValueError(
                f"Der Marker {marker} kommt zu oft in {source.name} vor."
            )

    # Dashboard- und Popup-Farben.
    # Wichtig: Bei kombinierten YAML/CSS-Zeilen nur den Gradient ersetzen.
    for key in THEME_GROUPS[group]["colors"]:
        marker = f"ATC_{key.upper()}"

        content, count = _replace_atc_gradient(
            content,
            marker,
            values[key],
        )

        # Fallback für eigenständige YAML-Farbwerte.
        if count == 0:
            content, count = _replace_atc_value(
                content,
                marker,
                values[key],
            )

        if count > 4:
            raise ValueError(
                f"Der Marker {marker} kommt zu oft in {source.name} vor."
            )

    # Abschnittsabstände.
    gap_keys = (
        f"section_column_gap_{group}",
        f"section_row_gap_{group}",
    )

    for key in gap_keys:
        marker = f"ATC_{key.upper()}"

        content, count = _replace_atc_value(
            content,
            marker,
            values[key],
        )

        if count > 4:
            raise ValueError(
                f"Der Marker {marker} kommt zu oft in {source.name} vor."
            )

    # Abschnitt-Rahmenfarbe.
    key = f"section_border_color_{group}"
    marker = f"ATC_{key.upper()}"

    content, count = _replace_atc_rgba(
        content,
        marker,
        values[key],
    )

    if count > 4:
        raise ValueError(
            f"Der Marker {marker} kommt zu oft in {source.name} vor."
        )

    # Schriftgrößen.
    for size in FONT_SIZE_DEFAULTS:
        key = f"font_size_{size}_{group}"
        marker = f"ATC_FONT_SIZE_{size.upper()}"

        formatted_value = f"{values[key]}px"

        content, count = _replace_atc_value(
            content,
            marker,
            formatted_value,
        )

        if count > 4:
            raise ValueError(
                f"Der Marker {marker} kommt zu oft in {source.name} vor."
            )

    # Textfarben.
    for key in TEXT_COLOR_DEFAULTS[group]:
        option_key = f"{key}_{group}"
        marker = f"ATC_{key.upper()}_{suffix}"

        content, count = _replace_atc_value(
            content,
            marker,
            values[option_key],
        )

        if count > 4:
            raise ValueError(
                f"Der Marker {marker} kommt zu oft in {source.name} vor."
            )

    # Icon-Größe.
    marker = f"ATC_ICON_SIZE_{suffix}"
    content, count = _replace_atc_value(
        content, marker, f"{values[f'icon_size_{group}']}px"
    )
    if count > 4:
        raise ValueError(f"Der Marker {marker} kommt zu oft in {source.name} vor.")

    # Icon-Farbe (aus/deaktiviert) im jeweiligen Darstellungsmodus.
    for key in ICON_OFF_COLOR_DEFAULTS:
        marker = f"ATC_{key.upper()}_{suffix}"
        content, count = _replace_atc_value(content, marker, values[f"{key}_{group}"])
        if count > 4:
            raise ValueError(f"Der Marker {marker} kommt zu oft in {source.name} vor.")

    # Primär- und Akzentfarben für Hell- und Dunkel-Modus.
    for key in PRIMARY_COLOR_DEFAULTS:
        marker = f"ATC_{key.upper()}_{suffix}"
        content, count = _replace_atc_value(
            content, marker, values[f"{key}_{group}"]
        )
        if count > 4:
            raise ValueError(
                f"Der Marker {marker} kommt zu oft in {source.name} vor."
            )

    # Karten-Radius (ein Marker je Theme-Abschnitt / Design-Modus).
    marker = f"ATC_CARD_BORDER_RADIUS_{suffix}"
    content, count = _replace_atc_value(
        content, marker, f"{values[f'card_border_radius_{group}']}px"
    )
    if count > 4:
        raise ValueError(
            f"Der Marker {marker} kommt zu oft in {source.name} vor."
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


def _remove_managed_assets(
    themes_target: Path,
    wallpaper_target: Path,
    manifest_path: Path,
) -> None:
    """Remove unchanged integration-managed files during uninstall."""
    try:
        manifest = _load_manifest(manifest_path)
    except (OSError, ValueError, TypeError):
        _LOGGER.exception(
            "Die Dateiverwaltung konnte bei der Deinstallation nicht "
            "gelesen werden. Themes und Wallpaper bleiben daher erhalten."
        )
        # The manifest belongs to this integration and must not be left in
        # .storage, even if it is corrupt. Without valid hashes, deleting
        # asset files would not be safe.
        try:
            manifest_path.unlink(missing_ok=True)
        except OSError:
            _LOGGER.exception(
                "Die Manifest-Datei konnte nicht entfernt werden: %s",
                manifest_path,
            )
        return

    for category, target_dir in (
        ("themes", themes_target),
        ("wallpapers", wallpaper_target),
    ):
        for filename, expected_hash in manifest[category].items():
            target = target_dir / filename

            # _load_manifest validates that each entry is a plain filename.
            if not target.exists():
                continue

            if target.is_dir() or not target.is_file():
                _LOGGER.warning(
                    "Verwaltete Datei ist kein reguläres File und wird "
                    "nicht entfernt: %s",
                    target,
                )
                continue

            try:
                if _file_hash(target) != expected_hash:
                    _LOGGER.warning(
                        "Datei wurde manuell verändert und bleibt bei "
                        "der Deinstallation erhalten: %s",
                        target,
                    )
                    continue

                target.unlink()
                _LOGGER.info(
                    "Verwaltete Datei bei der Deinstallation entfernt: %s",
                    target,
                )
            except OSError:
                _LOGGER.exception(
                    "Verwaltete Datei konnte nicht entfernt werden: %s",
                    target,
                )

    try:
        manifest_path.unlink(missing_ok=True)
        _LOGGER.debug("Dateiverwaltung entfernt: %s", manifest_path)
    except OSError:
        _LOGGER.exception(
            "Die Manifest-Datei konnte nicht entfernt werden: %s",
            manifest_path,
        )


async def async_remove_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Remove unchanged files managed by this integration on uninstall."""
    themes_target = Path(hass.config.path("themes"))
    wallpaper_target = Path(hass.config.path("www", "wallpaper"))
    manifest_path = Path(
        hass.config.path(
            ".storage",
            "awesome_theme_collection_manifest.json",
        )
    )

    await hass.async_add_executor_job(
        _remove_managed_assets,
        themes_target,
        wallpaper_target,
        manifest_path,
    )

    try:
        await hass.services.async_call(
            "frontend",
            "reload_themes",
            {},
            blocking=True,
        )
    except HomeAssistantError:
        _LOGGER.exception(
            "Die Integration wurde entfernt, aber die Themes konnten "
            "nicht neu geladen werden."
        )


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload the integration."""
    return True
