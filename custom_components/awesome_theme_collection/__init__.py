"""Awesome Theme Collection for Home Assistant."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

DOMAIN = "awesome_theme_collection"

_LOGGER = logging.getLogger(__name__)


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

    try:
        await hass.async_add_executor_job(
            _copy_assets,
            themes_source,
            themes_target,
            wallpaper_source,
            wallpaper_target,
        )
    except (OSError, ValueError) as err:
        _LOGGER.exception(
            "Installation der Themes oder Hintergründe fehlgeschlagen"
        )
        raise HomeAssistantError(
            "Die Theme-Dateien konnten nicht vollständig "
            "installiert werden. Bitte prüfe die Asset-Dateien "
            "und die Schreibrechte der Home-Assistant-Verzeichnisse."
        ) from err

    _LOGGER.info(
        "Awesome Theme Collection erfolgreich eingerichtet"
    )
    return True


def _copy_assets(
    themes_source: Path,
    themes_target: Path,
    wallpaper_source: Path,
    wallpaper_target: Path,
) -> None:
    """Validate and copy theme and wallpaper files."""

    for source_dir in (themes_source, wallpaper_source):
        if not source_dir.is_dir():
            raise FileNotFoundError(
                f"Benötigtes Asset-Verzeichnis fehlt: {source_dir}"
            )

        if not any(item.is_file() for item in source_dir.iterdir()):
            raise ValueError(
                f"Asset-Verzeichnis enthält keine Dateien: {source_dir}"
            )

    themes_target.mkdir(parents=True, exist_ok=True)
    wallpaper_target.mkdir(parents=True, exist_ok=True)

    for source_dir, target_dir in (
        (themes_source, themes_target),
        (wallpaper_source, wallpaper_target),
    ):
        for source_file in source_dir.iterdir():
            if source_file.is_file():
                shutil.copy2(
                    source_file,
                    target_dir / source_file.name,
                )

                _LOGGER.debug(
                    "Datei installiert: %s",
                    source_file.name,
                )


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload the integration."""

    return True
