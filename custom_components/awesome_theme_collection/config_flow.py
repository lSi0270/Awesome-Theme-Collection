"""Config flow for Awesome Theme Collection."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from . import DOMAIN

THEMES = {
    "metal_dark": "Metal Dark",
    "metal_light": "Metal Light",
    "leather_dark": "Leather Dark",
    "leather_light": "Leather Light",
    "metal_dark_shadow": "Metal Dark Shadow",
    "metal_light_shadow": "Metal Light Shadow",
    "leather_dark_shadow": "Leather Dark Shadow",
    "leather_light_shadow": "Leather Light Shadow",
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


class AwesomeThemeOptionsFlow(config_entries.OptionsFlow):
    """Manage installed themes."""

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Display the theme selection."""

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

        schema = vol.Schema(
            {
                vol.Required(
                    "themes",
                    default=current_themes,
                ): vol.All(
                    [vol.In(list(THEMES))],
                    vol.Length(min=0, max=len(THEMES)),
                )
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            description_placeholders={
                "themes": ", ".join(THEMES.values()),
            },
        )
