"""Awesome Theme Collection for Home Assistant."""

from __future__ import annotations

import shutil
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "awesome_theme_collection"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Awesome Theme Collection from a config entry."""

    integration_dir = Path(__file__).parent
    assets_dir = integration_dir / "assets"

    themes_source = assets_dir / "themes"
    wallpaper_source = assets_dir / "wallpaper"

    themes_target = Path(hass.config.path("themes"))
    wallpaper_target = Path(hass.config.path("www", "wallpaper"))

    await hass.async_add_executor_job(
        _copy_assets,
        themes_source,
        themes_target,
        wallpaper_source,
        wallpaper_target,
    )

    return True


def _copy_assets(
    themes_source: Path,
    themes_target: Path,
    wallpaper_source: Path,
    wallpaper_target: Path,
) -> None:
    """Copy theme and wallpaper files to Home Assistant."""

    themes_target.mkdir(parents=True, exist_ok=True)
    wallpaper_target.mkdir(parents=True, exist_ok=True)

    if themes_source.exists():
        for source_file in themes_source.iterdir():
            if source_file.is_file():
                shutil.copy2(
                    source_file,
                    themes_target / source_file.name,
                )

    if wallpaper_source.exists():
        for source_file in wallpaper_source.iterdir():
            if source_file.is_file():
                shutil.copy2(
                    source_file,
                    wallpaper_target / source_file.name,
                )
