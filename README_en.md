<p align="center">
  <a href="https://github.com/lSi0270/Awesome-Theme-Collection/blob/main/README.md">Deutsch</a> · <b>English</b>
</p>

# Awesome Theme Collection for Home Assistant

This is a collection of UIX themes with matching backgrounds for Home Assistant. The themes style (almost) all standard HA cards, custom cards, bubble cards and mushroom cards with a consistent look.
In addition, all pages (Settings, Profiles, HACS, etc.) and dialogues, as well as bubble card pop-ups, feature the dashboard background. The themes all use the same color scheme but differ in terms of card styling – with or without shadows – and the choice of background.

## Included Themes

- Awesome-Metal-Shadows-UIX

<p align="center">
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Metal-Shadows-UIX_dark.jpg" alt="Awesome-Metal-Shadows-UIX_dark" width="45%" />
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Metal-Shadows-UIX_light.jpg" alt="Awesome-Metal-Shadows-UIX_light" width="45%" />
</p>

- Awesome-Metal-UIX

<p align="center">
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Metal-UIX_dark.jpg" alt="Awesome-Metal-UIX_dark" width="45%" />
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Metal-UIX_light.jpg" alt="Awesome-Metal-UIX_light" width="45%" />
</p>

- Awesome-Leather-Shadows-UIX

<p align="center">
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Leather-Shadows-UIX_dark.jpg" alt="Awesome-Leather-Shadows-UIX_dark" width="45%" />
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Leather-Shadows-UIX_light.jpg" alt="Awesome-Leather-Shadows-UIX_light" width="45%" />
</p>

- Awesome-Leather-UIX

<p align="center">
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Leather-UIX_dark.jpg" alt="Awesome-Leather-UIX_dark" width="45%" />
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Leather-UIX_light.jpg" alt="Awesome-Leather-UIX_light" width="45%" />
</p>

- Awesome-Flat-Metal-Shadows-UIX

<p align="center">
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Flat-Metal-Shadows-UIX_dark.jpg" alt="Awesome-Flat-Metal-Shadows-UIX_dark" width="45%" />
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Flat-Metal-Shadows-UIX_light.jpg" alt="Awesome-Flat-Metal-Shadows-UIX_light" width="45%" />
</p>

- Awesome-Flat-Metal-UIX

<p align="center">
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Flat-Metal-UIX_dark.jpg" alt="Awesome-Flat-Metal-UIX_dark" width="45%" />
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Flat-Metal-UIX_light.jpg" alt="Awesome-Flat-Metal-UIX_light" width="45%" />
</p>

- Awesome-Flat-Leather-Shadows-UIX

<p align="center">
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Flat-Leather-Shadows-UIX_dark.jpg" alt="Awesome-Flat-Leather-Shadows-UIX_dark" width="45%" />
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Flat-Leather-Shadows-UIX_light.jpg" alt="Awesome-Flat-Leather-Shadows-UIX_light" width="45%" />
</p>

- Awesome-Flat-Leather-UIX

<p align="center">
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Flat-Leather-UIX_dark.jpg" alt="Awesome-Flat-Leather-UIX_dark" width="45%" />
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Flat-Leather-UIX_light.jpg" alt="Awesome-Flat-Leather-UIX_light" width="45%" />
</p>


To use them, the themes must be loaded when HA starts (see installation instructions). As the themes make extensive use of the UIX extension, the UIX extension must be installed to achieve the intended look (see installation instructions).
It will work without UIX, but will then simply look like a standard HA theme with a different color scheme. The themes are aimed at anyone who doesn’t want to style everything manually but still wants an attractive, consistent look.

Special thanks go to Piranha1605 for his HATG (https://github.com/Piranha1605/ha-theme-generator) and Lint-Free-Technology for the UIX extension (https://github.com/Lint-Free-Technology/uix).
Without them, this collection of themes would never become reality.


## Installation instructions

Please follow the steps below carefully to ensure everything works smoothly!

### 1. Home Assistant configuration

The integration is deliberately designed **not** to modify your `configuration.yaml`. You must therefore add the following entry manually. If the entry already exists, please skip to step 2.
To ensure Home Assistant can use the installed themes, add the following to your `configuration.yaml`:

    frontend:
      themes: !include_dir_merge_named themes

After changing `configuration.yaml`, restart Home Assistant.

### 2. Install the UIX extension

If the UIX extension is already installed and the UIX settings have been configured under ‘Experimental settings’, please skip to step 3.

Search for ‘uix’ in HACS and install the UIX extension ((https://github.com/Lint-Free-Technology/uix)).

After restarting HA, go to “Settings/Devices & Services/UI eXtension for Home Assistant”. Then click the “cog” (Configure).

Select “Experimental settings” and tick “Always patch ha-card” and “Style frame panels loaded as iframe” (this is necessary to ensure that all parts of the theme work as they should)

### 3. Installing the Awesome Theme Collection

1. add *`https://github.com/lSi0270/Awesome-Theme-Collection`* manually in HACS as a custom repository (category **Integration**), install **Awesome Theme Collection**  and restart Home Assistant.
2. Go to **Settings/Devices & Services**.
3. **Add integration**.
4. Search for **Awesome Theme Collection**.
5. Install the integration (‘Reload designs’ will run automatically after installation).
6. In the integration settings, you can select or deselect the themes you want or don’t want.
7. Go to **Profile** (User) and, under “Design”, select the desired theme and the desired “Design Mode”

The integration automatically creates the necessary directories for the themes (/config/themes/) and for the wallpapers (/config/www/wallpaper/).

### 4. Have fun

I certainly hope that some of you will enjoy it as much as I do.

## Support

If you encounter a problem or have a suggestion for improvement, please open an issue in the GitHub repository.
