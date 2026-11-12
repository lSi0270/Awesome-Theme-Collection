"""Config flow for Awesome Theme Collection."""

from __future__ import annotations

import logging
import math
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import section
from homeassistant.helpers import selector

from . import (
    DEFAULT_OPTIONS,
    DOMAIN,
    THEMES as INSTALL_THEMES,
    TRANSPARENT_WALLPAPER,
    SIDEBAR_DEFAULTS,
    TOOLBAR_DEFAULTS,
)

_LOGGER = logging.getLogger(__name__)


FONT_SIZES: dict[str, int] = {
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

FONT_DESCRIPTIONS: dict[str, str] = {
    "xs": "Kleine Statusanzeigen, kurze Hinweise, kompakte Labels",
    "s": "Sekundärtexte, Untertitel, Zeitstempel, kleine Beschriftungen",
    "m": "Normaler Text, Standardbeschriftungen, Entitätsnamen",
    "l": "Hervorgehobener Text, wichtige Statusinformationen, Kartenüberschriften",
    "xl": "Größere Überschriften, Abschnittstitel",
    "2xl": "Hauptüberschriften, prominente Werte",
    "3xl": "Große Überschriften, wichtige Messwerte",
    "4xl": "Sehr große Kennzahlen, Temperatur oder Energieverbrauch",
    "5xl": "Besonders prominente Zahlen, z. B. auf einem Wandtablet",
}


def _font_key(size: str, group: str) -> str:
    """Return a group-specific font option key."""
    return f"font_size_{size}_{group}"


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


ICON_DEFAULTS: dict[str, int] = {"icon_size": 24}
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

def _text_color_key(name: str, group: str) -> str:
    """Return a group-specific text color option key."""
    return f"{name}_{group}"


def _icon_key(name: str, group: str) -> str:
    """Return a group-specific icon option key."""
    return f"{name}_{group}"


class _RangeNumberSelector(selector.NumberSelector):
    """Keep native bounded sliders but defer range checks to the options flow.

    Home Assistant's NumberSelector validates min/max before the options-flow
    handler runs. Deferring that check lets the integration handle invalid
    values and show its translated error messages. The selector configuration
    still contains min/max, so the frontend keeps the bounded slider UI.
    """

    def __call__(self, data: Any) -> float:
        """Convert the submitted value without enforcing the selector range."""
        if isinstance(data, bool):
            raise vol.Invalid("Expected a number")
        try:
            return float(data)
        except (TypeError, ValueError) as err:
            raise vol.Invalid("Expected a number") from err


def _section_key(base: str, group: str) -> str:
    """Return a group-specific section option key."""
    return f"{base}_{group}"


def _valid_hex_color(value: Any) -> bool:
    """Validate a six-digit HEX color."""
    return (
        isinstance(value, str)
        and bool(HEX_COLOR_PATTERN.fullmatch(value.strip()))
    )


def _rgb_to_hex(value: Any) -> str | None:
    """Convert an RGB color list to a six-digit HEX color string."""
    if (
        not isinstance(value, (list, tuple))
        or len(value) != 3
        or any(
            isinstance(channel, bool)
            or not isinstance(channel, int)
            or not 0 <= channel <= 255
            for channel in value
        )
    ):
        return None

    return "#{:02X}{:02X}{:02X}".format(*value)


def _hex_to_rgb(value: str) -> list[int]:
    """Convert a six-digit HEX color string to an RGB list."""
    value = value.strip().lstrip("#")

    return [
        int(value[index:index + 2], 16)
        for index in (0, 2, 4)
    ]


THEME_GROUPS: dict[str, dict[str, Any]] = {
    "metal": {
        "enabled_key": "metal_enabled",
        "options_key": "themes_metal",
        "themes": (
            "flat_metal_shadows",
            "flat_metal",
            "metal_shadows",
            "metal",
        ),
        "backgrounds": {
            "background_metal_dark": DEFAULT_OPTIONS[
                "background_metal_dark"
            ],
            "background_metal_light": DEFAULT_OPTIONS[
                "background_metal_light"
            ],
            "background_popup_metal_dark": DEFAULT_OPTIONS[
                "background_popup_metal_dark"
            ],
            "background_popup_metal_light": DEFAULT_OPTIONS[
                "background_popup_metal_light"
            ],
        },
        "colors": {
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
        },
    },
    "leather": {
        "enabled_key": "leather_enabled",
        "options_key": "themes_leather",
        "themes": (
            "flat_leather_shadows",
            "flat_leather",
            "leather_shadows",
            "leather",
        ),
        "backgrounds": {
            "background_leather_dark": DEFAULT_OPTIONS[
                "background_leather_dark"
            ],
            "background_leather_light": DEFAULT_OPTIONS[
                "background_leather_light"
            ],
            "background_popup_leather_dark": DEFAULT_OPTIONS[
                "background_popup_leather_dark"
            ],
            "background_popup_leather_light": DEFAULT_OPTIONS[
                "background_popup_leather_light"
            ],
        },
        "colors": {
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
        },
    },
}


THEMES = {
    "flat_leather_shadows": "Awesome Flat Leather Shadows",
    "flat_leather": "Awesome Flat Leather",
    "flat_metal_shadows": "Awesome Flat Metal Shadows",
    "flat_metal": "Awesome Flat Metal",
    "leather_shadows": "Awesome Leather Shadows",
    "leather": "Awesome Leather",
    "metal_shadows": "Awesome Metal Shadows",
    "metal": "Awesome Metal",
}

if set(THEMES) != set(INSTALL_THEMES):
    raise RuntimeError(
        "Die Theme-Auswahl in config_flow.py stimmt nicht mit "
        "__init__.py überein."
    )


DEFAULT_SECTION_COLUMN_GAP = 32
DEFAULT_SECTION_ROW_GAP = 24
DEFAULT_SECTION_BORDER_COLOR = "rgba(130, 130, 130, 0.2)"
SECTION_DEFAULTS: dict[str, dict[str, str]] = {
    "metal": {
        "section_background_dark": "/local/wallpaper/metal3_dark.jpg",
        "section_color_dark": "linear-gradient(rgba(26, 31, 38, 0.4), rgba(26, 31, 38, 0.4))",
        "section_background_light": "/local/wallpaper/metal2_light.jpg",
        "section_color_light": "linear-gradient(rgba(224, 224, 224, 0.5), rgba(224, 224, 224, 0.5))",
    },
    "leather": {
        "section_background_dark": "/local/wallpaper/leather2_dark.jpg",
        "section_color_dark": "linear-gradient(rgba(22, 25, 28, 0.20), rgba(22, 25, 28, 0.20))",
        "section_background_light": "/local/wallpaper/leather2_light.jpg",
        "section_color_light": "linear-gradient(rgba(224, 224, 224, 0.60), rgba(224, 224, 224, 0.60))",
    },
}

WALLPAPER_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

RGBA_PATTERN = re.compile(
    r"rgba\(\s*"
    r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\s*,\s*"
    r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\s*,\s*"
    r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\s*,\s*"
    r"(?:0(?:\.\d+)?|1(?:\.0+)?)"
    r"\s*\)",
    re.IGNORECASE,
)

HEX_COLOR_PATTERN = re.compile(r"#[0-9a-fA-F]{6}")

LINEAR_GRADIENT_PATTERN = re.compile(
    r"^linear-gradient\((.*)\)$",
    re.IGNORECASE | re.DOTALL,
)


def _valid_background_path(value: Any) -> bool:
    """Validate a local wallpaper URL."""
    if (
        not isinstance(value, str)
        or not value.startswith("/local/wallpaper/")
        or any(
            char in value
            for char in ('"', "'", "\\", "\n", "\r", "?", "#")
        )
    ):
        return False

    path = Path(value)
    return (
        ".." not in path.parts
        and path.name not in {"", ".", ".."}
    )


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
    """Validate a HEX or RGBA gradient stop with optional percentage."""
    value = value.strip()
    percentage_pattern = r"(?:\s+(\d+(?:\.\d+)?%))?"

    hex_match = re.fullmatch(
        rf"(#[0-9a-fA-F]{{3}}|#[0-9a-fA-F]{{4}}|"
        rf"#[0-9a-fA-F]{{6}}|#[0-9a-fA-F]{{8}})"
        rf"{percentage_pattern}",
        value,
    )

    if hex_match:
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
    """Validate a linear gradient with optional direction and positions."""
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

    return len(stops) >= 2 and all(
        _valid_gradient_stop(stop) for stop in stops
    )


def _get_wallpaper_options(
    wallpaper_dir: Path,
    current_options: dict[str, Any],
) -> list[dict[str, str]]:
    """Find wallpapers and always offer the transparent system asset."""
    wallpapers: dict[str, str] = {}

    for config in THEME_GROUPS.values():
        for url in config["backgrounds"].values():
            wallpapers[url] = f"{Path(url).name} (Standard)"
    for defaults in SECTION_DEFAULTS.values():
        for name, url in defaults.items():
            if name.startswith("section_background_"):
                wallpapers[url] = f"{Path(url).name} (Standard)"

    transparent_url = f"/local/wallpaper/{TRANSPARENT_WALLPAPER}"
    wallpapers[transparent_url] = "Transparent"

    try:
        if wallpaper_dir.is_dir():
            for path in wallpaper_dir.iterdir():
                try:
                    if (
                        path.is_file()
                        and path.suffix.lower() in WALLPAPER_EXTENSIONS
                    ):
                        url = "/local/wallpaper/" + quote(
                            path.name, safe=""
                        )

                        if url != transparent_url:
                            wallpapers[url] = path.name

                except OSError:
                    continue

    except OSError:
        pass

    for key, value in current_options.items():
        if (
            (key.startswith("background_") or key.startswith("section_background_"))
            and _valid_background_path(value)
            and value not in wallpapers
        ):
            wallpapers[value] = (
                f"{Path(value).name} (Datei nicht gefunden)"
            )

    return [
        {"label": label, "value": value}
        for value, label in sorted(
            wallpapers.items(),
            key=lambda item: item[1].casefold(),
        )
    ]


async def get_wallpaper_options(
    hass: HomeAssistant,
    current_options: dict[str, Any],
) -> list[dict[str, str]]:
    """Find wallpapers without blocking the event loop."""
    wallpaper_dir = Path(hass.config.path("www", "wallpaper"))

    return await hass.async_add_executor_job(
        _get_wallpaper_options,
        wallpaper_dir,
        current_options,
    )

class AwesomeThemeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the initial setup."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Set up the integration."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(
                title="Awesome Theme Collection",
                data={},
            )

        return self.async_show_form(step_id="user")

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> AwesomeThemeOptionsFlow:
        """Create the options flow."""
        return AwesomeThemeOptionsFlow()


class AwesomeThemeOptionsFlow(config_entries.OptionsFlowWithReload):
    """Manage independent Metal and Leather configuration."""

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Show enabled areas and the available configuration steps."""
        options = self.config_entry.options
        menu_options = ["areas"]

        if options.get("metal_enabled", True):
            menu_options.append("metal")

        if options.get("leather_enabled", True):
            menu_options.append("leather")

        return self.async_show_menu(
            step_id="init",
            menu_options=menu_options,
        )

    async def async_step_areas(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Enable or disable the theme areas."""
        options = dict(self.config_entry.options)

        if user_input is not None:
            options.update(user_input)
            return self.async_create_entry(title="", data=options)

        return self.async_show_form(
            step_id="areas",
            data_schema=vol.Schema({
                vol.Required(
                    "metal_enabled",
                    default=options.get("metal_enabled", True),
                ): selector.BooleanSelector(),
                vol.Required(
                    "leather_enabled",
                    default=options.get("leather_enabled", True),
                ): selector.BooleanSelector(),
            }),
        )

    async def async_step_metal(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Configure the Metal theme area."""
        return await self._async_step_group("metal", user_input)

    async def async_step_leather(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Configure the Leather theme area."""
        return await self._async_step_group("leather", user_input)

    async def _async_step_group(
        self,
        group: str,
        user_input: dict[str, Any] | None,
    ) -> config_entries.ConfigFlowResult:
        """Configure one theme group independently."""
        if group not in THEME_GROUPS:
            raise ValueError(f"Unbekannter Theme-Bereich: {group}")

        options = dict(self.config_entry.options)
        config = THEME_GROUPS[group]

        if user_input is not None:
            try:
                theme_data = user_input["themes"]
                background_data = user_input["backgrounds"]
                section_data = user_input["sections"]
                font_data = user_input["fonts"]
                text_color_data = user_input["text_colors"]
                icon_data = user_input["icons"]
                primary_color_data = user_input["primary_colors"]
                card_data = user_input["cards"]
                sidebar_data = user_input["sidebar"]
                toolbar_data = user_input["toolbar"]

            except (KeyError, TypeError) as err:
                _LOGGER.exception(
                    "ATC: Ungültige Gruppeneinstellungen für %s",
                    group,
                )
                raise ValueError(
                    "Die übermittelten Gruppeneinstellungen sind ungültig."
                ) from err

            new_options = dict(options)

            # Theme-Auswahl
            new_options[config["options_key"]] = [
                key
                for key in config["themes"]
                if theme_data.get(key, False)
            ]

            # Hintergrundbilder
            for key in config["backgrounds"]:
                value = background_data.get(key)

                if not _valid_background_path(value):
                    return self.async_show_form(
                        step_id=group,
                        data_schema=await self._group_schema(group),
                        errors={"backgrounds": "invalid_background"},
                    )

                new_options[key] = value

            if background_data.get("reset_backgrounds", False):
                new_options.update(config["backgrounds"])

            # Dashboard- und Popup-Farben
            for key, default_value in config["colors"].items():
                value = background_data.get(key, default_value)

                if not _valid_theme_color(value):
                    return self.async_show_form(
                        step_id=group,
                        data_schema=await self._group_schema(group),
                        errors={"backgrounds": "invalid_theme_color"},
                    )

                new_options[key] = value.strip()

            if background_data.get("reset_colors", False):
                new_options.update(config["colors"])

            # Abschnittsabstände und Rahmenfarbe
            section_keys = {
                "section_column_gap": _section_key(
                    "section_column_gap", group
                ),
                "section_row_gap": _section_key(
                    "section_row_gap", group
                ),
                "section_border_color": _section_key(
                    "section_border_color", group
                ),
            }

            if section_data.get("reset_sections", False):
                new_options.update({
                    section_keys["section_column_gap"]:
                        DEFAULT_SECTION_COLUMN_GAP,
                    section_keys["section_row_gap"]:
                        DEFAULT_SECTION_ROW_GAP,
                    section_keys["section_border_color"]: DEFAULT_SECTION_BORDER_COLOR,
                    **{f"{key}_{group}": value for key, value in SECTION_DEFAULTS[group].items()},
                    f"section_background_always_set_{group}": "Off",
                })

            else:
                column_gap = section_data.get(
                    section_keys["section_column_gap"]
                )
                row_gap = section_data.get(
                    section_keys["section_row_gap"]
                )
                color = section_data.get(
                    section_keys["section_border_color"]
                )

                if (
                    isinstance(column_gap, bool)
                    or not isinstance(column_gap, (int, float))
                    or not math.isfinite(column_gap)
                    or not 0 <= column_gap <= 50
                    or isinstance(row_gap, bool)
                    or not isinstance(row_gap, (int, float))
                    or not math.isfinite(row_gap)
                    or not 0 <= row_gap <= 50
                ):
                    return self.async_show_form(
                        step_id=group,
                        data_schema=await self._group_schema(group),
                        errors={"sections": "invalid_spacing"},
                    )

                if (
                    not isinstance(color, str)
                    or not RGBA_PATTERN.fullmatch(color)
                ):
                    return self.async_show_form(
                        step_id=group,
                        data_schema=await self._group_schema(group),
                        errors={"sections": "invalid_rgba"},
                    )

                new_options.update({
                    section_keys["section_column_gap"]: column_gap,
                    section_keys["section_row_gap"]: row_gap,
                    section_keys["section_border_color"]: color,
                })
                for name, default_value in SECTION_DEFAULTS[group].items():
                    key = f"{name}_{group}"
                    value = section_data.get(key, default_value)
                    if name.startswith("section_background_"):
                        if not _valid_background_path(value):
                            return self.async_show_form(step_id=group, data_schema=await self._group_schema(group), errors={"sections": "invalid_background"})
                    elif not _valid_theme_color(value):
                        return self.async_show_form(step_id=group, data_schema=await self._group_schema(group), errors={"sections": "invalid_theme_color"})
                    new_options[key] = value.strip() if isinstance(value, str) else value
                always_value = section_data.get(f"section_background_always_set_{group}", False)
                new_options[f"section_background_always_set_{group}"] = "On" if always_value else "Off"

            # Schriftgrößen
            if font_data.get("reset_fonts", False):
                for size, default_value in FONT_SIZES.items():
                    new_options[_font_key(size, group)] = default_value

            else:
                for size, default_value in FONT_SIZES.items():
                    key = _font_key(size, group)
                    value = font_data.get(key, default_value)

                    if (
                        isinstance(value, bool)
                        or not isinstance(value, (int, float))
                        or not math.isfinite(value)
                        or int(value) != value
                        or not 8 <= value <= 46
                    ):
                        return self.async_show_form(
                            step_id=group,
                            data_schema=await self._group_schema(group),
                            errors={"fonts": "invalid_font_size"},
                        )

                    new_options[key] = int(value)

            # Schriftfarben: HEX-Werte direkt übernehmen und normalisieren
            color_defaults = TEXT_COLOR_DEFAULTS[group]

            if text_color_data.get("reset_text_colors", False):
                for name, default_value in color_defaults.items():
                    new_options[_text_color_key(name, group)] = default_value

            else:
                for name, default_value in color_defaults.items():
                    key = _text_color_key(name, group)
                    value = text_color_data.get(key, default_value)

                    if not _valid_hex_color(value):
                        return self.async_show_form(
                            step_id=group,
                            data_schema=await self._group_schema(group),
                            errors={"text_colors": "invalid_hex_color"},
                        )

                    new_options[key] = value.strip().upper()

            # Seitenleiste und Kopfleiste
            for area_name, area_data, defaults in (
                ("sidebar", sidebar_data, SIDEBAR_DEFAULTS[group]),
                ("toolbar", toolbar_data, TOOLBAR_DEFAULTS[group]),
            ):
                if area_data.get(f"reset_{area_name}", False):
                    for name, default_value in defaults.items():
                        new_options[f"{name}_{group}"] = default_value
                    continue

                for name, default_value in defaults.items():
                    key = f"{name}_{group}"
                    value = area_data.get(key, default_value)
                    if name.endswith("_title"):
                        if (not isinstance(value, str) or len(value) > 20
                                or any(ord(char) < 32 for char in value)):
                            return self.async_show_form(
                                step_id=group,
                                data_schema=await self._group_schema(group),
                                errors={area_name: "invalid_sidebar_title"},
                            )
                        new_options[key] = value
                    elif name.endswith("_fontsize"):
                        if (
                            isinstance(value, bool)
                            or not isinstance(value, (int, float))
                            or not math.isfinite(value)
                            or int(value) != value
                            or not 14 <= value <= 24
                        ):
                            return self.async_show_form(
                                step_id=group,
                                data_schema=await self._group_schema(group),
                                errors={area_name: "invalid_sidebar_font_size"},
                            )
                        new_options[key] = int(value)
                    elif "text_color" in name:
                        if not _valid_hex_color(value):
                            return self.async_show_form(
                                step_id=group,
                                data_schema=await self._group_schema(group),
                                errors={area_name: "invalid_hex_color"},
                            )
                        new_options[key] = value.strip().upper()
                    elif "_background_color_" in name:
                        if not _valid_theme_color(value):
                            return self.async_show_form(
                                step_id=group,
                                data_schema=await self._group_schema(group),
                                errors={area_name: "invalid_theme_color"},
                            )
                        new_options[key] = value.strip()
                    elif name.endswith("_background_dark") or name.endswith("_background_light"):
                        if not _valid_background_path(value):
                            return self.async_show_form(
                                step_id=group,
                                data_schema=await self._group_schema(group),
                                errors={area_name: "invalid_background"},
                            )
                        new_options[key] = value

            # Icon-Einstellungen
            if icon_data.get("reset_icons", False):
                for name, default_value in ICON_DEFAULTS.items():
                    new_options[_icon_key(name, group)] = default_value
                for name, default_value in ICON_OFF_COLOR_DEFAULTS.items():
                    new_options[_icon_key(name, group)] = default_value
                new_options[f"icons_glow_{group}"] = "On"
            else:
                for name, default_value in ICON_DEFAULTS.items():
                    key = _icon_key(name, group)
                    value = icon_data.get(key, default_value)
                    if (isinstance(value, bool) or not isinstance(value, (int, float))
                            or not math.isfinite(value)):
                        return self.async_show_form(
                            step_id=group, data_schema=await self._group_schema(group),
                            errors={"icons": "invalid_icon_size"})
                    if name == "icon_size" and (not 16 <= value <= 36 or int(value) != value):
                        return self.async_show_form(step_id=group, data_schema=await self._group_schema(group), errors={"icons": "invalid_icon_size"})
                    new_options[key] = int(value)

                for name, default_value in ICON_OFF_COLOR_DEFAULTS.items():
                    key = _icon_key(name, group)
                    value = icon_data.get(key, default_value)
                    if not _valid_hex_color(value):
                        return self.async_show_form(step_id=group, data_schema=await self._group_schema(group), errors={"icons": "invalid_hex_color"})
                    new_options[key] = value.strip().upper()
                glow_value = icon_data.get(f"icons_glow_{group}", True)
                new_options[f"icons_glow_{group}"] = "On" if glow_value else "Off"

            # Primär-Farben
            primary_color_keys = {
                name: f"{name}_{group}"
                for name in PRIMARY_COLOR_DEFAULTS
            }

            if primary_color_data.get("reset_primary_colors", False):
                for name, default_value in PRIMARY_COLOR_DEFAULTS.items():
                    new_options[primary_color_keys[name]] = default_value
            else:
                for name, default_value in PRIMARY_COLOR_DEFAULTS.items():
                    key = primary_color_keys[name]
                    value = primary_color_data.get(key, default_value)
                    if not _valid_hex_color(value):
                        return self.async_show_form(
                            step_id=group,
                            data_schema=await self._group_schema(group),
                            errors={"primary_colors": "invalid_hex_color"},
                        )
                    new_options[key] = value.strip().upper()


            # Karten: Karten-Radius und Steuerungs-Schalter
            radius_key = f"card_border_radius_{group}"
            if card_data.get("reset_cards", False):
                new_options[radius_key] = CARD_BORDER_RADIUS_DEFAULT
                new_options[f"control_set_background_{group}"] = "On"
            else:
                radius = card_data.get(radius_key, CARD_BORDER_RADIUS_DEFAULT)
                if (
                    isinstance(radius, bool)
                    or not isinstance(radius, (int, float))
                    or not math.isfinite(radius)
                    or int(radius) != radius
                    or not 0 <= radius <= 28
                ):
                    return self.async_show_form(
                        step_id=group,
                        data_schema=await self._group_schema(group),
                        errors={"cards": "invalid_card_radius"},
                    )
                new_options[radius_key] = int(radius)
                control_value = card_data.get(f"control_set_background_{group}", True)
                new_options[f"control_set_background_{group}"] = "On" if control_value else "Off"

            return self.async_create_entry(title="", data=new_options)

        # Schema mit Diagnoseprotokollierung erstellen
        try:
            schema = await self._group_schema(group)

            _LOGGER.debug(
                "ATC DEBUG: Schema für %s erfolgreich erstellt",
                group,
            )

            return self.async_show_form(
                step_id=group,
                data_schema=schema,
            )

        except Exception:
            _LOGGER.exception(
                "ATC DEBUG: Fehler beim Erstellen des Schemas für %s",
                group,
            )
            raise

    async def _group_schema(self, group: str) -> vol.Schema:
        """Build the settings form for one theme group."""
        options = self.config_entry.options
        config = THEME_GROUPS[group]

        wallpaper_options = await get_wallpaper_options(
            self.hass,
            options,
        )

        legacy_themes = options.get("themes", list(THEMES))

        if (
            not isinstance(legacy_themes, list)
            or any(not isinstance(key, str) for key in legacy_themes)
        ):
            legacy_themes = list(THEMES)

        selected_themes = options.get(
            config["options_key"],
            [
                key for key in config["themes"]
                if key in legacy_themes
            ],
        )

        if (
            not isinstance(selected_themes, list)
            or any(
                not isinstance(key, str)
                or key not in config["themes"]
                for key in selected_themes
            )
        ):
            selected_themes = [
                key for key in config["themes"]
                if key in legacy_themes
            ]

        theme_fields = {
            vol.Optional(key, default=key in selected_themes):
                selector.BooleanSelector()
            for key in config["themes"]
        }

        suffix = group

        dashboard_keys = (
            f"background_{suffix}_dark",
            f"dashboard_color_{suffix}_dark",
            f"background_{suffix}_light",
            f"dashboard_color_{suffix}_light",
        )

        popup_keys = (
            f"background_popup_{suffix}_dark",
            f"popup_color_{suffix}_dark",
            f"background_popup_{suffix}_light",
            f"popup_color_{suffix}_light",
        )

        # Hintergrundbilder und Farben
        background_fields: dict[Any, Any] = {}

        for key in (*dashboard_keys, *popup_keys):
            if key in config["backgrounds"]:
                default_path = config["backgrounds"][key]
                saved_path = options.get(key, default_path)

                if not _valid_background_path(saved_path):
                    saved_path = default_path

                background_fields[
                    vol.Required(key, default=saved_path)
                ] = selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=wallpaper_options,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                )

            else:
                default_color = config["colors"][key]
                saved_color = options.get(key, default_color)

                if not _valid_theme_color(saved_color):
                    saved_color = default_color

                background_fields[
                    vol.Required(key, default=saved_color)
                ] = selector.TextSelector()

        background_fields[
            vol.Optional("reset_backgrounds", default=False)
        ] = selector.BooleanSelector()

        background_fields[
            vol.Optional("reset_colors", default=False)
        ] = selector.BooleanSelector()

        # Abschnittseinstellungen
        section_fields = {
            vol.Required(
                _section_key("section_column_gap", group),
                default=options.get(
                    _section_key("section_column_gap", group),
                    options.get(
                        "section_column_gap",
                        DEFAULT_SECTION_COLUMN_GAP,
                    ),
                ),
            ): _RangeNumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=50,
                    step=1,
                    mode=selector.NumberSelectorMode.SLIDER,
                    unit_of_measurement="px",
                )
            ),
            vol.Required(
                _section_key("section_row_gap", group),
                default=options.get(
                    _section_key("section_row_gap", group),
                    options.get(
                        "section_row_gap",
                        DEFAULT_SECTION_ROW_GAP,
                    ),
                ),
            ): _RangeNumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=50,
                    step=1,
                    mode=selector.NumberSelectorMode.SLIDER,
                    unit_of_measurement="px",
                )
            ),
            vol.Required(
                _section_key("section_border_color", group),
                default=options.get(
                    _section_key("section_border_color", group),
                    options.get(
                        "section_border_color",
                        DEFAULT_SECTION_BORDER_COLOR,
                    ),
                ),
            ): selector.TextSelector(),
        }
        section_switch_key = f"section_background_always_set_{group}"
        section_fields[vol.Required(
            section_switch_key,
            default=options.get(section_switch_key, "Off") == "On",
        )] = selector.BooleanSelector()
        for name, default_value in SECTION_DEFAULTS[group].items():
            key = f"{name}_{group}"
            saved_value = options.get(key, default_value)
            if name.startswith("section_background_"):
                if not _valid_background_path(saved_value):
                    saved_value = default_value
                section_fields[vol.Required(key, default=saved_value)] = selector.SelectSelector(
                    selector.SelectSelectorConfig(options=wallpaper_options, mode=selector.SelectSelectorMode.DROPDOWN)
                )
            else:
                if not _valid_theme_color(saved_value):
                    saved_value = default_value
                section_fields[vol.Required(key, default=saved_value)] = selector.TextSelector()
        section_fields[vol.Optional("reset_sections", default=False)] = selector.BooleanSelector()

        # Schriftgrößen
        font_fields: dict[Any, Any] = {}

        for size, default_value in FONT_SIZES.items():
            key = _font_key(size, group)
            saved_value = options.get(key, default_value)

            if (
                isinstance(saved_value, bool)
                or not isinstance(saved_value, (int, float))
                or not math.isfinite(saved_value)
                or int(saved_value) != saved_value
                or not 8 <= saved_value <= 46
            ):
                saved_value = default_value

            font_fields[
                vol.Required(key, default=int(saved_value))
            ] = selector.NumberSelector(
                selector.NumberSelectorConfig(
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="px",
                )
            )

        font_fields[
            vol.Optional("reset_fonts", default=False)
        ] = selector.BooleanSelector()

        # Schriftfarben: einfache HEX-Texteingabefelder
        text_color_fields: dict[Any, Any] = {}
        color_defaults = TEXT_COLOR_DEFAULTS[group]

        for name, default_value in color_defaults.items():
            key = _text_color_key(name, group)
            saved_value = options.get(key, default_value)

            if not _valid_hex_color(saved_value):
                saved_value = default_value

            # Native HTML color input: displays a color swatch and opens
            # the browser's color picker without submitting the config flow.
            # The browser returns the same six-digit HEX string used by ATC.
            text_color_fields[
                vol.Required(key, default=saved_value.upper())
            ] = selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.COLOR
                )
            )

        text_color_fields[
            vol.Optional("reset_text_colors", default=False)
        ] = selector.BooleanSelector()

        # Seitenleiste und Kopfleiste
        def _navigation_fields(area: str, defaults: dict[str, Any]) -> dict[Any, Any]:
            fields: dict[Any, Any] = {}
            for name, default_value in defaults.items():
                key = f"{name}_{group}"
                saved = options.get(key, default_value)
                if name.endswith("_title"):
                    if not isinstance(saved, str) or len(saved) > 20:
                        saved = default_value
                    fields[vol.Required(key, default=saved)] = selector.TextSelector()
                elif name.endswith("_fontsize"):
                    if (isinstance(saved, bool) or not isinstance(saved, (int, float))
                            or not math.isfinite(saved) or int(saved) != saved
                            or not 14 <= saved <= 24):
                        saved = default_value
                    fields[vol.Required(key, default=int(saved))] = _RangeNumberSelector(
                        selector.NumberSelectorConfig(
                            min=14, max=24, step=1,
                            mode=selector.NumberSelectorMode.BOX,
                            unit_of_measurement="px",
                        )
                    )
                elif "text_color" in name:
                    if not _valid_hex_color(saved):
                        saved = default_value
                    fields[vol.Required(key, default=saved.upper())] = selector.TextSelector(
                        selector.TextSelectorConfig(type=selector.TextSelectorType.COLOR)
                    )
                elif "_background_color_" in name:
                    if not _valid_theme_color(saved):
                        saved = default_value
                    fields[vol.Required(key, default=saved)] = selector.TextSelector()
                elif name.endswith("_background_dark") or name.endswith("_background_light"):
                    if not _valid_background_path(saved):
                        saved = default_value
                    fields[vol.Required(key, default=saved)] = selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=wallpaper_options,
                            mode=selector.SelectSelectorMode.DROPDOWN,
                        )
                    )
            fields[vol.Optional(f"reset_{area}", default=False)] = selector.BooleanSelector()
            return fields

        sidebar_fields = _navigation_fields("sidebar", SIDEBAR_DEFAULTS[group])
        toolbar_fields = _navigation_fields("toolbar", TOOLBAR_DEFAULTS[group])

        # Icon-Einstellungen
        icon_fields: dict[Any, Any] = {}
        icon_ranges = {
            "icon_size": {"min": 16, "max": 36},
        }
        for name, default_value in ICON_DEFAULTS.items():
            key = _icon_key(name, group)
            saved = options.get(key, default_value)
            limits = icon_ranges[name]
            if (isinstance(saved, bool) or not isinstance(saved, (int, float))
                    or not math.isfinite(saved) or not limits["min"] <= saved <= limits["max"]
                    or int(saved) != saved):
                saved = default_value
            ns = _RangeNumberSelector(selector.NumberSelectorConfig(
                min=limits["min"], max=limits["max"], step=1,
                mode=selector.NumberSelectorMode.SLIDER,
                unit_of_measurement="px"))
            lang = (self.hass.config.language or "en").split("-")[0]
            messages = {
                "de": {"icon_size": "Die Icon-Größe muss zwischen 16 und 36 Pixel liegen."},
                "en": {"icon_size": "Icon size must be between 16 and 36 pixels."},
            }
            ns.config["validation_message"] = messages.get(lang, messages["en"])[name]
            icon_fields[vol.Required(key, default=int(saved))] = ns

        icon_fields[vol.Required(
            f"icons_glow_{group}",
            default=options.get(f"icons_glow_{group}", "On") == "On",
        )] = selector.BooleanSelector()

        for name, default_value in ICON_OFF_COLOR_DEFAULTS.items():
            key = _icon_key(name, group)
            saved = options.get(key, default_value)
            if not _valid_hex_color(saved):
                saved = default_value
            icon_fields[vol.Required(key, default=saved.upper())] = selector.TextSelector(
                selector.TextSelectorConfig(type=selector.TextSelectorType.COLOR))

        icon_fields[
            vol.Optional("reset_icons", default=False)
        ] = selector.BooleanSelector()

        # Primär-Farben und Karten-Radius
        primary_color_fields: dict[Any, Any] = {}
        for name, default_value in PRIMARY_COLOR_DEFAULTS.items():
            key = f"{name}_{group}"
            saved = options.get(key, default_value)
            if not _valid_hex_color(saved):
                saved = default_value
            primary_color_fields[
                vol.Required(key, default=saved.upper())
            ] = selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.COLOR
                )
            )

        primary_color_fields[
            vol.Optional("reset_primary_colors", default=False)
        ] = selector.BooleanSelector()

        # Karten: Radius und Hintergrund für Steuerungs-Schalter
        card_fields: dict[Any, Any] = {}
        radius_key = f"card_border_radius_{group}"
        saved_radius = options.get(radius_key, CARD_BORDER_RADIUS_DEFAULT)
        if (
            isinstance(saved_radius, bool) or not isinstance(saved_radius, (int, float))
            or not math.isfinite(saved_radius) or int(saved_radius) != saved_radius
            or not 0 <= saved_radius <= 28
        ):
            saved_radius = CARD_BORDER_RADIUS_DEFAULT
        card_fields[vol.Required(radius_key, default=int(saved_radius))] = _RangeNumberSelector(
            selector.NumberSelectorConfig(min=0, max=28, step=1, mode=selector.NumberSelectorMode.SLIDER, unit_of_measurement="px")
        )
        card_fields[vol.Required(
            f"control_set_background_{group}",
            default=options.get(f"control_set_background_{group}", "On") == "On",
        )] = selector.BooleanSelector()
        card_fields[vol.Optional("reset_cards", default=False)] = selector.BooleanSelector()

        # Gesamtschema erstellen
        return vol.Schema({
            vol.Required("themes"): section(
                vol.Schema(theme_fields),
                {"collapsed": True},
            ),
            vol.Required("backgrounds"): section(
                vol.Schema(background_fields),
                {"collapsed": True},
            ),
            vol.Required("sections"): section(vol.Schema(section_fields), {"collapsed": True}),
            vol.Required("cards"): section(vol.Schema(card_fields), {"collapsed": True}),
            vol.Required("sidebar"): section(vol.Schema(sidebar_fields), {"collapsed": True}),
            vol.Required("toolbar"): section(vol.Schema(toolbar_fields), {"collapsed": True}),
            vol.Required("icons"): section(vol.Schema(icon_fields), {"collapsed": True}),
            vol.Required("fonts"): section(vol.Schema(font_fields), {"collapsed": True}),
            vol.Required("text_colors"): section(vol.Schema(text_color_fields), {"collapsed": True}),
            vol.Required("primary_colors"): section(vol.Schema(primary_color_fields), {"collapsed": True}),
        })

    @staticmethod
    def _color_key_for_background(
        background_key: str,
        group: str,
    ) -> str | None:
        """Return the matching dashboard or popup color option key."""
        suffix = "metal" if group == "metal" else "leather"

        if background_key == f"background_{suffix}_dark":
            return f"dashboard_color_{suffix}_dark"

        if background_key == f"background_{suffix}_light":
            return f"dashboard_color_{suffix}_light"

        if background_key == f"background_popup_{suffix}_dark":
            return f"popup_color_{suffix}_dark"

        if background_key == f"background_popup_{suffix}_light":
            return f"popup_color_{suffix}_light"

        return None
