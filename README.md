<p align="center">
  <b>Deutsch</b> · <a href="https://github.com/lSi0270/Awesome-Theme-Collection/blob/main/README_en.md">English</a>
</p>

# Awesome Theme Kollektion für Home Assistant

Das ist eine Kollektion von UIX-Themes mit passenden Hintergründen für Home Assistant. Die Themes stylen (fast) alle HA-Standard-Karten, Custom-Karten, Bubble-Karten und Mushroom-Karten mit einem einheitlichen Aussehen.
Zusätzlich werden alle Seiten (Einstellungen, Profile, HACS usw.) und Dialoge, Bubble-Card-Popups mit dem Dashboard-Hintergrund versehen. Die Themes nutzen alle das gleiche Farbschema, unterscheiden sich beim Kartenstyling, mit Schatten oder Ohne, Wahl des Hintergrundes.

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
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Metal-UIX_dark.jpg" alt="Awesome-Flat-Metal-UIX_dark" width="45%" />
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Metal-UIX_light.jpg" alt="Awesome-Flat-Metal-UIX_light" width="45%" />
</p>

- Awesome-Flat-Leather-Shadows-UIX

<p align="center">
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Leather-Shadows-UIX_dark.jpg" alt="Awesome-Flat-Leather-Shadows-UIX_dark" width="45%" />
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Leather-Shadows-UIX_light.jpg" alt="Awesome-Flat-Leather-Shadows-UIX_light" width="45%" />
</p>

- Awesome-Flat-Leather-UIX

<p align="center">
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Leather-UIX_dark.jpg" alt="Awesome-Flat-Leather-UIX_dark" width="45%" />
  <img src="https://raw.githubusercontent.com/lSi0270/Awesome-Theme-Collection/main/screenshots/Awesome-Leather-UIX_light.jpg" alt="Awesome-Flat-Leather-UIX_light" width="45%" />
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

1. **HACS** in Home Assistant öffnen.
2. Nach **Awesome Theme Collection** suchen.
3. Integration downloaden und installieren.
4. Home Assistant neu starten.
5. Zu **Einstellungen/Geräte & Dienste**.
6. **Integration hinzufügen**.
7. **Awesome Theme Collection** suchen.
8. Integration hinzufügen.
9. Zu **Einstellungen/Werkzeuge/Aktionen** und "Designs neu laden" auswählen.
10. Zu **Profil** (Benutzer) und unter "Design" das gewünschte Design auswählen und den gewünschten "Design-Modus" 

Die Integration legt automatisch die erforderlichen Verzeichnisse an für die Themes (/config/themes/) und für die Hintergründe (/config/www/wallpaper/).

### 4. Spaß haben

Ich hoffe es zumindest, das es dem Einen oder Anderen auch so gut gefällt wie mir selbst.

## Support

Wenn du ein Problem findest oder einen Verbesserungsvorschlag hast, öffne eine issue im Github Repository.
