"""Config flow for Awesome Theme Collection."""

from __future__ import annotations

from typing import Any

from homeassistant import config_entries

from . import DOMAIN


class AwesomeThemeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Awesome Theme Collection."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle the user setup."""

        if user_input is not None:
            return self.async_create_entry(
                title="Awesome Theme Collection",
                data={},
            )

        return self.async_show_form(
            step_id="user",
        )
