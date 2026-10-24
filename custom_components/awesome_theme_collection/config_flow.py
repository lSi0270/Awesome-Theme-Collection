"""Config flow for Awesome Theme Collection."""

from __future__ import annotations

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
)


THEME_GROUPS: dict[str, dict[str, Any]] = {
    "metal": {
        "enabled_key": "metal_enabled",
        "themes_key": "themes_metal",
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
        "themes_key": "themes_leather",
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

HEX_COLOR_PATTERN = re.compile(
    r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|"
    r"[0-9a-fA-F]{6}|[0-9a-fA-F]{8})"
)

LINEAR_GRADIENT_PATTERN = re.compile(
    r"^linear-gradient\((.*)\)$",
    re.IGNORECASE | re.DOTALL,
)


def _section_key(base: str, group: str) -> str:
    """Return a group-specific section option key."""

    return f"{base}_{group}"


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

    # A plain HEX/RGBA color is intentionally not accepted.
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


def _get_wallpaper_options(
    wallpaper_dir: Path,
    current_options: dict[str, Any],
) -> list[dict[str, str]]:
    """Find wallpapers and always offer the transparent system asset."""

    wallpapers: dict[str, str] = {}

    for config in THEME_GROUPS.values():
        for url in config["backgrounds"].values():
            wallpapers[url] = f"{Path(url).name} (Standard)"

    # Always offer a transparent background, even if the file is
    # temporarily missing from the target directory.
    transparent_url = f"/local/wallpaper/{TRANSPARENT_WALLPAPER}"
    wallpapers[transparent_url] = "Transparent (kein Hintergrundbild)"

    try:
        if wallpaper_dir.is_dir():
            for path in wallpaper_dir.iterdir():
                try:
                    if (
                        path.is_file()
                        and path.suffix.lower() in WALLPAPER_EXTENSIONS
                    ):
                        url = "/local/wallpaper/" + quote(
                            path.name,
                            safe="",
                        )

                        if url == transparent_url:
                            continue

                        wallpapers[url] = path.name
                except OSError:
                    continue
    except OSError:
        pass

    for key, value in current_options.items():
        if (
            key.startswith("background_")
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

            return self.async_create_entry(
                title="",
                data=options,
            )

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
            except (KeyError, TypeError) as err:
                raise ValueError(
                    "Die übermittelten Gruppeneinstellungen sind ungültig."
                ) from err

            new_options = dict(options)

            new_options[config["themes_key"]] = [
                key
                for key in config["themes"]
                if theme_data.get(key, False)
            ]

            for key in config["backgrounds"]:
                value = background_data.get(key)

                if not _valid_background_path(value):
                    return self.async_show_form(
                        step_id=group,
                        data_schema=await self._group_schema(group),
                        errors={"base": "invalid_background"},
                    )

                new_options[key] = value

            if background_data.get("reset_backgrounds", False):
                new_options.update(config["backgrounds"])

            for key, default_value in config["colors"].items():
                value = background_data.get(key, default_value)

                if not _valid_theme_color(value):
                    return self.async_show_form(
                        step_id=group,
                        data_schema=await self._group_schema(group),
                        errors={"base": "invalid_theme_color"},
                    )

                new_options[key] = value.strip()

            if background_data.get("reset_colors", False):
                new_options.update(config["colors"])

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
                    section_keys["section_border_color"]:
                        DEFAULT_SECTION_BORDER_COLOR,
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
                    or not 0 <= column_gap <= 50
                    or isinstance(row_gap, bool)
                    or not isinstance(row_gap, (int, float))
                    or not 0 <= row_gap <= 50
                ):
                    return self.async_show_form(
                        step_id=group,
                        data_schema=await self._group_schema(group),
                        errors={"base": "invalid_spacing"},
                    )

                if (
                    not isinstance(color, str)
                    or not RGBA_PATTERN.fullmatch(color)
                ):
                    return self.async_show_form(
                        step_id=group,
                        data_schema=await self._group_schema(group),
                        errors={"base": "invalid_rgba"},
                    )

                new_options.update({
                    section_keys["section_column_gap"]: column_gap,
                    section_keys["section_row_gap"]: row_gap,
                    section_keys["section_border_color"]: color,
                })

            return self.async_create_entry(
                title="",
                data=new_options,
            )

        return self.async_show_form(
            step_id=group,
            data_schema=await self._group_schema(group),
        )

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
            config["themes_key"],
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
            vol.Optional(
                key,
                default=key in selected_themes,
            ): selector.BooleanSelector()
            for key in config["themes"]
        }

        background_fields: dict[Any, Any] = {}

        for key, default_path in config["backgrounds"].items():
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

            color_key = self._color_key_for_background(key, group)

            if color_key is not None:
                default_color = config["colors"][color_key]
                saved_color = options.get(color_key, default_color)

                if not _valid_theme_color(saved_color):
                    saved_color = default_color

                background_fields[
                    vol.Required(
                        color_key,
                        default=saved_color,
                    )
                ] = selector.TextSelector()

        background_fields[
            vol.Optional("reset_backgrounds", default=False)
        ] = selector.BooleanSelector()

        background_fields[
            vol.Optional("reset_colors", default=False)
        ] = selector.BooleanSelector()

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
            ): selector.NumberSelector(
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
            ): selector.NumberSelector(
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
            vol.Optional("reset_sections", default=False):
                selector.BooleanSelector(),
        }

        return vol.Schema({
            vol.Required("themes"): section(
                vol.Schema(theme_fields),
                {"collapsed": True},
            ),
            vol.Required("backgrounds"): section(
                vol.Schema(background_fields),
                {"collapsed": True},
            ),
            vol.Required("sections"): section(
                vol.Schema(section_fields),
                {"collapsed": True},
            ),
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