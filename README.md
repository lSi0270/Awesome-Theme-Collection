[Deutsch](#awesome_theme_kollektion) · [English](#awesome_theme_collection)

# Awesome Theme Kollektion

Das ist eine Kollektion von UIX-Themes mit passenden Hintergründen für Home Assistant. Die Themes stylen (fast) alle HA-Standard-Karten, Custom-Karten, Bubble-Karten und Mushroom-Karten mit einem einheitlichen Aussehen.
Zusätzlich werden alle Seiten (Einstellungen, Profile, HACS usw.) und Dialoge, Bubble-Card-Popups mit dem Dashboard-Hintergrund versehen. Die Themes nutzen alle das gleiche Farbschema, unterscheiden sich beim Kartenstyling, mit Schatten oder Ohne und der Wahl des Hintergrundes.

[Themes](#enthaltene_themes) · [Installation](#installationsanweisungen) · [Versionen](#versionen)

## Enthaltene Themes

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


Für die Nutzung ist es erforderlich, das die Themes beim HA-Start geladen werden (siehe Installationsanweisungen). Da die Themes intensiven Gebrauch von der UIX-Erweiterung machen, ist es für das vorgesehene Aussehen erforderlich das die UIX-Erweiterung installiert ist (siehe Installationsanweisungen).
Ohne UIX funktioniert es auch, aber sieht dann nur nach einem Standard-HA-Theme mit anderer Farbpalette aus. Die Themes richten sich an Alle die nicht alles von Hand stylen wollen, aber trotzdem ein schönes, gleichmäßiges Aussehen haben wollen.

Besonderer Dank geht an Piranha1605 für seinen HATG (https://github.com/Piranha1605/ha-theme-generator) und Lint-Free-Technology für die UIX-Erweiterung (https://github.com/Lint-Free-Technology/uix).
Ohne die Beiden wäre die Themes-Kollektion nicht enstanden.

## Installationsanweisungen

Bitte gehen Sie die folgenden Schritte genau durch, um eine reibungslose Funktion zu gewährleisten !

### 1. Home Assistant Konfiguration

Die Integration modifiziert mit Absicht **nicht** deine `configuration.yaml`. Deshalb muss der folgende Eintrag auch selbst von Hand erledigt werden. Wenn der Eintrag bereits vorhanden ist, bitte zu 2. springen.

Damit Home Assistant die installierten Themes auch nutzen kann, füge Folgendes deiner `configuration.yaml` hinzu:

    frontend:
      themes: !include_dir_merge_named themes

Nach der Änderung der `configuration.yaml`, Home Assistant neu starten.

### 2. UIX-Erweiterung installieren

Wenn die UIX-Erweiterung bereits installiert ist und die UIX-Einstellungen in "Experimental settings" gemacht sind, bitte zu 3. springen.

In HACS nach "uix" suchen und die UIX-Erweiterung ((https://github.com/Lint-Free-Technology/uix) installieren.

Nach HA-Neustart zu "Einstellungen/Geräte & Dienste/UI eXtension for Home Assistant" gehen. Dann auf das "Zahnrad" (Konfigurieren) klicken.

"Experimental settings" auswählen und "Always patch ha-card" und "Style frame panels loaded as iframe" anhaken (notwendig damit alle Teile des Themes auch so funktionieren wie sie sollen)

### 3. Installation der Awesome Theme Kollektion

1. **https://github.com/lSi0270/Awesome-Theme-Collection** in HACS manuell als benutzerdefiniertes Repository (Kategorie **Integration**) hinzufügen, **Awesome Theme Collection** herunterladen und Home Assistant neu starten.
2. Zu **Einstellungen/Geräte & Dienste**.
3. **Integration hinzufügen**.
4. **Awesome Theme Collection** suchen.
5. Integration installieren ("Designs neu laden" wird nach der Installation automatisch ausgeführt).
6. In den Integrations-Einstellungen können gewünschte und nicht gewünschte Themes an- oder abgewählt werden.
7. Zu **Profil** (Benutzer) und unter "Design" das gewünschte Design auswählen und den gewünschten "Design-Modus" 

Die Integration legt automatisch die erforderlichen Verzeichnisse an für die Themes (/config/themes/) und für die Hintergründe (/config/www/wallpaper/).

### 4. Spaß haben

Ich hoffe es zumindest, das es dem Einen oder Anderen auch so gut gefällt wie mir selbst.

## Support

Wenn du ein Problem findest oder einen Verbesserungsvorschlag hast, öffne eine issue im Github Repository.

<p align="center">
  <b>[Deutsch](#awesome_theme_kollektion)</b> · <b>[English](#awesome_theme_collection)</b>
</p>

## Versionen

v1.0.5
- setzt einen dezenten Rand für Sections wenn Hintergrund gesetzt
- state-active-color (light) korrigiert

v1.0.4
Installationroutine angepasst (Installation routine updated):
- Auswahlmöglichkeit der Themes in den Integrations-Einstellungen
- keine Fehlermeldungen mehr im Log nach Neustart
- "Designs neu laden" wird jetzt automatisch ausgeführt nach Installation/Deinstallation

v1.0.3
- Neuer Metallhintergrund (New Metal Background)
- Screenshots aktualisiert (Screenshots updated)

v1.0.2
- mehr Farben korrigiert, Transparenzwerte teilweise angepasst, mehr Dialoge mit Dashboard-Hintergrund

v1.0.1
- Einige Farben korrigiert für HA-Karten, Bubble-Karten, Mushroom-Karten

v1.0.0
- Erstes Release (8 UIX-Themes mit Light & Dark Sektion)


<p align="center">
  <b>[Deutsch](#awesome_theme_kollektion)</b> · <b>[English](#awesome_theme_collection)</b>
</p>

# Awesome Theme Collection

This is a collection of UIX themes with matching backgrounds for Home Assistant. The themes style (almost) all standard HA cards, custom cards, bubble cards and mushroom cards with a consistent look.
In addition, all pages (Settings, Profiles, HACS, etc.) and dialogues, as well as bubble card pop-ups, feature the dashboard background. The themes all use the same color scheme but differ in terms of card styling – with or without shadows – and the choice of background.

<p align="center">
  <b>[Themes](#included_themes)</b> · <b>[Installation](#installation_instructions)</b> · <b>[Versions](#versions)</b>
</p>

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

1. add *`https://github.com/lSi0270/Awesome-Theme-Collection`* manually in HACS as a custom repository (category **Integration**), load **Awesome Theme Collection**  and restart Home Assistant.
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

## Versions

v1.0.5
- adds a subtle border to sections when a background is set
- state-active-color (light) corrected

v1.0.4
option to select themes in the integration settings
- no more error messages in the log after a restart
- "reload designs" is now carried out automatically after installation/uninstallation

v1.0.3
- new metal background
- screenshots updated

v1.0.2
- more colors fixes, transparency values partially adjusted, more dialog boxes with a dashboard background

v1.0.1
- some color fixes for HA-Cards, Bubble-Cards, Mushroom-Cards

v1.0.0
- first release (8 UIX-Themes with Light & Dark Section)
