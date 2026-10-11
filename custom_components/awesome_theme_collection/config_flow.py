"""Config flow for Awesome Theme Collection."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from . import DOMAIN

THEMES = {
    "flat_leather_shadows": {
        "name": "Awesome Flat Leather Shadows",
        "filename": "Awesome-Flat-Leather-Shadows-UIX.yaml",
    },
    "flat_leather": {
        "name": "Awesome Flat Leather",
        "filename": "Awesome-Flat-Leather-UIX.yaml",
    },
    "flat_metal_shadows": {
        "name": "Awesome Flat Metal Shadows",
        "filename": "Awesome-Flat-Metal-Shadows-UIX.yaml",
    },
    "flat_metal": {
        "name": "Awesome Flat Metal",
        "filename": "Awesome-Flat-Metal-UIX.yaml",
    },
    "leather_shadows": {
        "name": "Awesome Leather Shadows",
        "filename": "Awesome-Leather-Shadows-UIX.yaml",
    },
    "leather": {
        "name": "Awesome Leather",
        "filename": "Awesome-Leather-UIX.yaml",
    },
    "metal_shadows": {
        "name": "Awesome Metal Shadows",
        "filename": "Awesome-Metal-Shadows-UIX.yaml",
    },
    "metal": {
        "name": "Awesome Metal",
        "filename": "Awesome-Metal-UIX.yaml",
    },
}


class AwesomeThemeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the initial setup."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Set up the integration."""

        if self._async_current_entries():
            return self.async_abort(
                reason="single_instance_allowed"
            )

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


class AwesomeThemeOptionsFlow(
    config_entries.OptionsFlowWithReload
):
    """Manage the installed themes."""

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Show the theme selection."""

        if user_input is not None:
            return self.async_create_entry(
                title="",
                data={
                    "themes": user_input["themes"],
                },
            )

        current_themes = self.config_entry.options.get(
            "themes",
            list(THEMES),
        )

        options = [
            {
                "label": theme["name"],
                "value": key,
            }
            for key, theme in THEMES.items()
        ]

        schema = vol.Schema(
            {
                vol.Required(
                    "themes",
                    default=current_themes,
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=options,
                        multiple=True,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                )
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
        )
