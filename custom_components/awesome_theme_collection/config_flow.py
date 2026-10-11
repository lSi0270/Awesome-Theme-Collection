"""Config flow for Awesome Theme Collection."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from . import DOMAIN

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


class AwesomeThemeConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
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

        return self.async_show_form(
            step_id="user",
        )

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
        """Show the individual theme checkboxes."""

        if user_input is not None:
            selected_themes = [
                key
                for key in THEMES
                if user_input.get(key, False)
            ]

            return self.async_create_entry(
                title="",
                data={
                    "themes": selected_themes,
                },
            )

        current_themes = self.config_entry.options.get(
            "themes",
            list(THEMES),
        )

        schema_fields = {}

        for key in THEMES:
            schema_fields[
                vol.Optional(
                    key,
                    default=key in current_themes,
                )
            ] = selector.BooleanSelector()

        schema = vol.Schema(schema_fields)

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
        )
