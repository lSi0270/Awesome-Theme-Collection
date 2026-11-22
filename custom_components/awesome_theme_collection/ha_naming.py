"""Optional frontend-only entity naming feature, isolated from theme management.

Behavior based on tcrgit/ha-no-device-prefix (MIT); see THIRD_PARTY_NOTICES.md.
"""
from __future__ import annotations

import logging
import re
from pathlib import Path

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import HomeAssistantView, StaticPathConfig
from homeassistant.core import HomeAssistant
from homeassistant.helpers import label_registry as lr

_LOGGER = logging.getLogger(__name__)
KEY = "awesome_theme_collection_ha_naming"
URL = "/awesome_theme_collection/ha-naming.js"
SETTINGS_URL = "/awesome_theme_collection/ha-naming-settings.json"


def _seed_labels(hass: HomeAssistant) -> None:
    """Create labels once if no equivalent exists; never delete user labels."""
    registry = lr.async_get(hass)
    names = {re.sub(r"[^a-z0-9]", "", value.lower())
             for item in registry.labels.values()
             for value in (item.label_id, item.name)}
    for label, equivalents in (
        ("keep-prefix", {"keepprefix", "keepdeviceprefix"}),
        ("omit-prefix", {"omitprefix", "omitdeviceprefix", "noprefix", "nodeviceprefix"}),
    ):
        if not names.intersection(equivalents):
            try:
                registry.async_create(label, icon="mdi:label-outline")
            except ValueError:
                _LOGGER.debug("Label %s already exists", label)


class NamingSettingsView(HomeAssistantView):
    """Expose only two nonsensitive booleans to the browser."""
    url = SETTINGS_URL
    name = "awesome_theme_collection:ha_naming_settings"
    requires_auth = False

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass

    async def get(self, request):
        state = self.hass.data.get(KEY, {})
        return self.json({
            "enabled": bool(state.get("enabled", False)),
            "opt_in_mode": state.get("mode", "opt_out") != "opt_out",
        })


async def async_setup_ha_naming(hass: HomeAssistant, options: dict) -> None:
    """Register once per HA runtime, update flags after each options reload."""
    enabled = bool(options.get("feature_ha_naming", True))
    mode = options.get("ha_naming_mode", "opt_out")
    if mode not in ("opt_in", "opt_out"):
        mode = "opt_out"
    hass.data[KEY] = {"enabled": enabled, "mode": mode}
    if enabled:
        try:
            _seed_labels(hass)
        except Exception:
            _LOGGER.exception("HA-Namensgebung: Labels konnten nicht angelegt werden")
    if hass.data.get(f"{KEY}_registered"):
        return
    js_path = Path(__file__).parent / "ha-naming.js"
    await hass.http.async_register_static_paths([
        StaticPathConfig(url_path=URL, path=str(js_path), cache_headers=False),
    ])
    hass.http.register_view(NamingSettingsView(hass))
    add_extra_js_url(hass, URL)
    hass.data[f"{KEY}_registered"] = True


def async_disable_ha_naming(hass: HomeAssistant) -> None:
    """Disarm any loaded frontend module without removing unrelated resources."""
    hass.data[KEY] = {"enabled": False, "mode": "opt_out"}
