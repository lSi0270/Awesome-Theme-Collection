"""Optional, isolated user appearance action for Awesome Theme Collection.

Uses an internal Home Assistant frontend API; errors in this module must
never interrupt theme installation, configuration, or unloading.
"""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError

DOMAIN = "awesome_theme_collection"
SERVICE = "set_design_mode"
_LOGGER = logging.getLogger(__name__)


def _validate_request(data: dict) -> dict:
    """Require at least one change without resetting the other setting."""
    if "mode" not in data and "theme" not in data:
        raise vol.Invalid("Mindestens 'mode' oder 'theme' angeben.")
    return data


SERVICE_SCHEMA = vol.All(
    vol.Schema(
        {
            vol.Optional("mode"): vol.In(("auto", "light", "dark")),
            vol.Optional("theme"): vol.All(str, vol.Length(min=1)),
        },
        extra=vol.PREVENT_EXTRA,
    ),
    _validate_request,
)


async def async_set_user_appearance(
    hass: HomeAssistant, *, mode: str | None, theme: str | None
) -> int:
    """Update all active real users, preserving any unspecified properties."""
    try:
        from homeassistant.components.frontend.storage import async_user_store
    except (ImportError, AttributeError) as err:
        raise HomeAssistantError(
            "Die interne Frontend-Speicherfunktion ist nicht verfügbar."
        ) from err

    try:
        users = await hass.auth.async_get_users()
    except Exception as err:
        raise HomeAssistantError(
            "Die Home-Assistant-Benutzer konnten nicht geladen werden."
        ) from err

    targets = [u for u in users if u.is_active and not u.system_generated]
    if not targets:
        _LOGGER.warning("Keine aktiven Home-Assistant-Benutzer gefunden")
        return 0

    changed = 0
    failed = 0
    for user in targets:
        try:
            store = await async_user_store(hass, user.id)
            previous = store.data.get("theme")
            settings = dict(previous) if isinstance(previous, dict) else {}
            if theme is not None:
                settings["theme"] = theme
            if mode == "auto":
                settings.pop("dark", None)
            elif mode is not None:
                settings["dark"] = mode == "dark"
            await store.async_set_item("theme", settings)
            changed += 1
        except Exception:
            failed += 1
            _LOGGER.exception(
                "Design-Einstellung für Benutzer %s fehlgeschlagen", user.id
            )

    if failed:
        raise HomeAssistantError(
            f"Design-Einstellungen für {changed} Benutzer aktualisiert, "
            f"für {failed} Benutzer fehlgeschlagen. Siehe Protokoll."
        )
    return changed


async def _handle_action(hass: HomeAssistant, call: ServiceCall) -> None:
    """Handle optional theme and/or mode selection."""
    try:
        changed = await async_set_user_appearance(
            hass,
            mode=call.data.get("mode"),
            theme=call.data.get("theme"),
        )
    except HomeAssistantError:
        raise
    except Exception as err:
        _LOGGER.exception("Design-Modus-Aktion fehlgeschlagen")
        raise HomeAssistantError(
            "Design-Modus konnte nicht geändert werden. Siehe Protokoll."
        ) from err
    _LOGGER.info("Design-Einstellungen für %s Benutzer aktualisiert", changed)


def async_register_design_mode_action(hass: HomeAssistant) -> None:
    """Register independently from the main integration lifecycle."""
    if hass.services.has_service(DOMAIN, SERVICE):
        return

    async def handle(call: ServiceCall) -> None:
        await _handle_action(hass, call)

    hass.services.async_register(
        DOMAIN, SERVICE, handle, schema=SERVICE_SCHEMA
    )


def async_unregister_design_mode_action(hass: HomeAssistant) -> None:
    """Remove the optional action without affecting other integration services."""
    if hass.services.has_service(DOMAIN, SERVICE):
        hass.services.async_remove(DOMAIN, SERVICE)
