# Awesome Theme Kollektion

Das ist eine Kollektion von UIX-Themes mit passenden Hintergründen für Home Assistant. Die Themes stylen (fast) alle HA-Standard-Karten, Custom-Karten, Bubble-Karten und Mushroom-Karten mit einem einheitlichen Aussehen.

Zusätzlich werden alle Seiten (Einstellungen, Profile, HACS usw.) und Dialoge, Bubble-Card-Popups mit einem Bild-Hintergrund versehen. 

Die Themes nutzen alle das gleiche Farbschema, unterscheiden sich beim Kartenstyling, mit Schatten oder Ohne und der Wahl des Hintergrundes.

[Installation](#installationsanweisungen) · [Einstellungen](#einstellungen) · [Änderungen](#änderungen) · [English](#awesome-theme-collection)

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


Für die Nutzung ist es erforderlich, das die Themes beim Start von Home Assistant geladen werden (siehe [Installationsanweisungen](#installationsanweisungen)). 

Da die Themes intensiven Gebrauch von der UIX-Erweiterung machen, ist es für das vorgesehene Aussehen erforderlich das die UIX-Erweiterung installiert ist (siehe Installationsanweisungen).
Ohne UIX funktioniert es auch, aber sieht dann nur nach einem Standard-HA-Theme mit anderer Farbpalette aus. Die Themes richten sich an Alle die nicht alles von Hand stylen wollen, aber trotzdem ein schönes, gleichmäßiges Aussehen haben wollen.

Besonderer Dank geht an Piranha1605 für seinen HATG (https://github.com/Piranha1605/ha-theme-generator) und Lint-Free-Technology für die UIX-Erweiterung (https://github.com/Lint-Free-Technology/uix).
Ohne die Beiden wäre die Themes-Kollektion nicht enstanden.

[🏠 Anfang](#awesome-theme-kollektion)



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

In HACS nach `uix` suchen und die UIX-Erweiterung (`https://github.com/Lint-Free-Technology/uix`) installieren.

Nach HA-Neustart zu "Einstellungen/Geräte & Dienste/UI eXtension for Home Assistant" gehen. Dann auf das "Zahnrad" (Konfigurieren) klicken.

`Experimental settings` auswählen und `Always patch ha-card` und `Style frame panels loaded as iframe` anhaken (notwendig damit alle Teile des Themes auch so funktionieren wie sie sollen)

### 3. Installation der Awesome Theme Kollektion

<p>
  <a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=lSi0270&amp;repository=awesome-theme-collection&amp;category=integration"><img src="https://my.home-assistant.io/badges/hacs_repository.svg" alt="Repository in Home Assistant öffnen" height="32"></a>
</p>

1. `https://github.com/lSi0270/Awesome-Theme-Collection` in HACS manuell als benutzerdefiniertes Repository (Kategorie **Integration**) hinzufügen, **Awesome Theme Collection** herunterladen und Home Assistant neu starten.
2. **Einstellungen/Geräte & Dienste**.
3. **Integration hinzufügen**.
4. **Awesome Theme Collection** suchen.
5. Integration installieren ("Designs neu laden" wird nach der Installation automatisch ausgeführt).
6. In den Integrations-Einstellungen können diverse [Einstellungen](einstellungen) gemacht werden.
7. Zu **Profil** (Benutzer) und unter "Design" das gewünschte Design auswählen und den gewünschten "Design-Modus" 

Die Integration legt automatisch die erforderlichen Verzeichnisse an für die Themes (`/config/themes/`) und für die Hintergründe (`/config/www/wallpaper/`).

### 4. Spaß haben

Ich hoffe es zumindest, das es dem Einen oder Anderen auch so gut gefällt wie mir selbst.

[🏠 Anfang](#awesome-theme-kollektion)



## Einstellungen

In den Integration-Einstellungen könne diverse Modifikationen vorgenommen werden. Es gibt 3 Untermenüs.

- Bereiche aktivieren/deaktivieren
- Awesome-Metall-Themes
- Awesome-Leder-Themes

Eine Auswähl öffnet das passende Dialogfenster.

### Bereiche aktivieren/deaktivieren

Hier kann ein ganzer Themen-Bereich aktiviert/deaktiviert werden. Das heisst wenn **"Awesome-Metall-Themes" oder "Awesome-Leder-Themes"** deaktiviert wird, werden alle passenden Themes und Hintergrundbilder dazu deaktiviert (aus öffentlichen Bereich entfernt).

Die Themes und Hintergründe werden nach Aktivierung wieder freigegeben, das heisst Sie werden bei Deaktivierung nicht komplett gelöscht und sind in den Integration-Einstellungen jederzeit wieder verfügbar (solange die Integration nicht deinstalliert wird).

### Awesome-Metall-Themes

Hier werden alle Einstellungen die die Metall-Themes betreffen gemacht und sind unabhängig von den anderen Bereichen.

#### Auswahl

Hier können einzelne **Themes aus diesem Bereich aktiviert/deaktiviert werden.** Dabei werden nur die Themes aus dem öffentlichen Bereich entfernt. Die passenden Hintergründe bleiben für die anderen Themes verfügbar.

#### Hintergründe

Hier können die **Bild- und Farb-Hintergründe für Dashboard- und Popup-Hintergrund (Dialoge, Bubble-Card Popups)** eingestellt werden (oder auch eine Kombination von Beiden).

Es stehen alle Bilder die in `/config/www/wallpaper/` hinterlegt sind zur Verfügung. Das heisst man kann auch eigene Bilder in das Verzeichnis kopieren, die dann in der jeweiligen Auswahl vorhanden sind.
Ich habe bereits ein paar **zusätzliche Hintergründe zur Auswahl** hinzugefügt (Passend mit _dark und _light gekennzeichnet).

Unterteilt ist der Bereich in **"Dashboard" und "Popups"** mit je einer Bild- und Farbauswahl für **"Dunkel" und "Hell"-Modus**.

z.B. "Dashboard-Bild-Dunkel" und "Dashboard-Farbe-Dunkel" stellt den Dashboard-Bild-Hintergrund und Dashboard-Farb-Hintergrund für den "Dunkel"-Design-Modus zusammen. Die beiden Werte werden dabei immer kombiniert.
Das Gleiche gilt auch für die anderen Felder im gleichen Maße.

Es kann unter der Bildauswahl auch "Transparent - kein Hintergrundbild" ausgewählt werden (wenn kein Bildhintergrund gewünscht). Alternativ kann in den rgba-Werten der Alpha auf 1 gesetzt werden (Farbe dann 100% deckend).

**Farbwert und Linear-Grandient nur verändern wenn man weiss was man tut, da ich nicht garantieren kann ob wirklich alle Falscheingaben abgefangen werden.**

**Wenn ein Linear-Gradient-Generator verwendet wird, bitte nur den eigentlichen Gradienten kopieren. Das heisst ohne "background: " am Anfang und ohne ";" am Ende, da sonst der Wert als ungültig abgelehnt wird.**

Es ist nur **ein Linear-Gradient erlaubt**, allerdings sind auch **mehr Zwischenwerte möglich** sowie auch ein anderer Winkel für den Verlauf und Prozent-Positionen.
Damit sind aber schon ziemlich viele wilde Kombinationen aus Bild- und Farb-Hintergrund möglich.

Beachten Sie bei der Wahl des Hintergrund-Bildes und der Hintergrund-Farbe darauf das die Lesbarkeit weiterhin gegeben ist (wählen sie deshalb nur zum Bereich passende Bilder und Farben aus).

Übernommen werden die Änderungen mit **"OK"**. Wenn etwas Falsches eingegeben wurde kommt eine "rote Fehlermeldung" im Dialog und der Wert wird wieder auf den Standard-Wert gesetzt.

Wenn **"Auf Standard-Hintergründe zurücksetzen"** aktiviert ist werden **mit "OK" die Voreinstellungen wieder hergestellt für die Bildhintergründe.**

Wenn **"Auf Standard-Farben zurücksetzen"** aktiviert ist werden mit **"OK" die Voreinstellungen wieder hergestellt für die Farbwerte.**

*Alle Einstellungen gelten hier nur für alle Hintergründe und Farben der Metall-Themes.*

#### Abschnittsabstände und Rahmenfarbe

Hier können die Abschnittsabstände (Sections) für **horizontale und vertikale Abstände der Abschnitte (Sections)** eingestellt werden (um weniger Platz zu verschwenden). Es sind Werte zwischen **0-50px möglich**. Ich würde aber nicht empfehlen die Werte auf 0 zu setzen, da dann die Abschnitte direkt aneinander liegen.

Außerdem kann eine Rahmenfarbe festgelegt werden.
**Die Rahmenfarbe ist aber nur aktiv wenn für den jeweiligen Abschnitt ein Hintergrund festgelegt ist.**

Übernommen werden die Änderungen mit **"OK"**. Wenn etwas Falsches eingegeben wurde kommt eine "rote Fehlermeldung" im Dialog und der Wert wird wieder auf den Standard-Wert gesetzt.

Wenn **"Auf Standard zurücksetzen"** aktiviert ist werden **mit "OK" die Voreinstellungen wieder hergestellt in diesem Bereich.**

*Alle Einstellungen gelten hier nur für alle  Abschnitte der Metall-Themes.*


## Awesome-Leder-Themes

Alle Einstellungen sind die Gleichen wie im Awesome-Metall-Themes Bereich. Siehe [**Awesome-Metall-Themes**](#awesome-metall-themes)

*Alle Einstellungen gelten hier nur für alle Leder-Themes.*

[🏠 Anfang](#awesome-theme-kollektion)


## Support

Wenn du ein Problem findest oder einen Verbesserungsvorschlag hast, öffne eine issue im Github Repository.


## Änderungen

v1.1.0
- es sind jetzt andere (auch eigene) Bildhintergründe möglich (einstellbar über die Integrations-Einstellungen) getrennt für die Metall- und Leder-Themes,
  getrennt für Dashboard und Popups (HA-Dialoge, Bubble-Card-Popups) jeweils für "Hell" und "Dunkel"-Modus. 
  (eigene Bilder nach /config/www/wallpaper/ kopieren) Ich habe bereits ein paar zusätzliche Hintergründe zur Auswahl hinzugefügt (Passend mit _dark und _light gekennzeichnet).

- ausserdem sind mehrstufige Farbverläufe möglich als Hintergrund, getrennt für Dashboard und Popups (HA-Dialoge, Bubble-Card-Popups) jeweils für "Hell" und "Dunkel"-Modus. 
  Der Bildhintergrund kann zusätzlich dazu erhalten bleiben, wenn im Farbverlauf eine Alphawert kleiner 1 gesetzt ist oder ein optional auswählbarer transparenter Hintergrund gewählt wurde.

- zusätzlich kann jeweils ein ganzer Bereich an Themes deaktiviert werden (Metall- und Leder-Themes), die aber nur aus dem öffentlichen Bereich entfernt werden und jederzeit wieder reaktiviert werden können

- neu ist auch ein zusätzlicher Bereich in dem die Abschnittsabstände und Rahmenfarbe für Abschnitte (Sections) in beiden Theme-Bereichen getrennt einstellbar ist

- es sind noch mehr System-Dialoge mit dem Theme-Styling versehen


v1.0.5
- setzt einen dezenten Rand für Abschnitte (Sections) wenn Hintergrund gesetzt

- state-active-color (light) korrigiert


v1.0.4
- Auswahlmöglichkeit der Themes in den Integrations-Einstellungen

- keine Fehlermeldungen mehr im Log nach Neustart

- "Designs neu laden" wird jetzt automatisch ausgeführt nach Installation/Deinstallation


v1.0.3
- Neuer Metallhintergrund

- Screenshots aktualisiert


v1.0.2
- mehr Farben korrigiert, Transparenzwerte teilweise angepasst, mehr Dialoge mit Dashboard-Hintergrund

v1.0.1
- Einige Farben korrigiert für HA-Karten, Bubble-Karten, Mushroom-Karten


v1.0.0
- Erstes Release (8 UIX-Themes mit Light & Dark Sektion)


[🏠 Anfang](#awesome-theme-kollektion)


# Awesome Theme Collection

This is a collection of UIX themes with matching backgrounds for Home Assistant. The themes style (almost) all standard HA cards, custom cards, bubble cards and mushroom cards with a consistent look.

In addition, all pages (Settings, Profiles, HACS, etc.) and dialogues, as well as bubble card pop-ups, feature a picture background.

The themes all use the same color scheme but differ in terms of card styling – with or without shadows – and the choice of background.

[Installation](#installation-instructions) · [Settings](#settings) · [Changes](#changes) · [Deutsch](#awesome-theme-kollektion)

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


To use them, the themes must be loaded when Home Assistant starts (see [installation instructions](#installation-instructions)).

As the themes make extensive use of the UIX extension, the UIX extension must be installed to achieve the intended look (see installation instructions).
It will work without UIX, but will then simply look like a standard HA theme with a different color scheme. The themes are aimed at anyone who doesn’t want to style everything manually but still wants an attractive, consistent look.

Special thanks go to Piranha1605 for his HATG (https://github.com/Piranha1605/ha-theme-generator) and Lint-Free-Technology for the UIX extension (https://github.com/Lint-Free-Technology/uix).
Without them, this collection of themes would never become reality.

[🏠 Home](#awesome-theme-collection)

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

Search for `uix` in HACS and install the UIX extension (https://github.com/Lint-Free-Technology/uix).

After restarting HA, go to “Settings/Devices & Services/UI eXtension for Home Assistant”. Then click the “cog” (Configure).

Select `Experimental settings` and tick `Always patch ha-card` and `Style frame panels loaded as iframe` (this is necessary to ensure that all parts of the theme work as they should)

### 3. Installing the Awesome Theme Collection

<p>
  <a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=lSi0270&amp;repository=awesome-theme-collection&amp;category=integration"><img src="https://my.home-assistant.io/badges/hacs_repository.svg" alt="Repository in Home Assistant öffnen" height="32"></a>
</p>

1. add *`https://github.com/lSi0270/Awesome-Theme-Collection`* manually in HACS as a custom repository (category **Integration**), load **Awesome Theme Collection**  and restart Home Assistant.
2. **Settings/Devices & Services**.
3. **Add integration**.
4. Search for **Awesome Theme Collection**.
5. Install the integration (‘Reload designs’ will run automatically after installation).
6. Various [settings](#settings) can be configured in the integration settings.
7. Go to **Profile** (User) and, under “Design”, select the desired theme and the desired “Design Mode”

The integration automatically creates the necessary directories for the themes (/config/themes/) and for the wallpapers (/config/www/wallpaper/).

### 4. Have fun

I certainly hope that some of you will enjoy it as much as I do.

[🏠 Home](#awesome-theme-collection)


## Settings

Various changes can be made in the integration settings. There are 3 sub-menus.

- Enable/disable sections
- Awesome Metal Themes
- Awesome Leather Themes

Selecting an option opens the corresponding dialog box.

### Enable/disable sections

Here, an entire theme section can be enabled or disabled. This means that if **‘Awesome Metal Themes’ or ‘Awesome Leather Themes’** is disabled, all corresponding themes and background images will be disabled (removed from the public area).

The themes and backgrounds are made available again once enabled; this means they are not completely deleted when disabled and remain available at any time in the integration settings (provided the integration is not uninstalled).

### Awesome Metal Themes

All settings relating to the metal themes are configured here and are independent of the other sections.

#### Selection

Here, individual **themes from this section can be enabled or disabled.** Only the themes are removed from the public area. The corresponding background images remain available for the other themes.

#### Backgrounds

Here you can set the **image and color backgrounds for the dashboard and pop-up backgrounds (dialogs, bubble card pop-ups)** (or a combination of both).

All images stored in `/config/www/wallpaper/` are available. This means you can also copy your own images into this directory, which will then appear in the relevant selection.
I’ve already added a **few extra backgrounds to the selection** (labelled _dark and _light as appropriate).

The section is divided into **“Dashboard” and “Pop-ups”**, each with an image and color selection for **“Dark” and “Light”-Mode**.

For example, “Dashboard Image – Dark” and “Dashboard Color – Dark” combine the dashboard image background and dashboard color background for the “Dark” design mode. These two settings are always combined.
The same applies to the other fields in exactly the same way.

Under ‘Image selection’, you can also choose ‘Transparent – no background image’ (if you do not want a background image). Alternatively, you can set the alpha value to 1 in the rgba values (the color will then be 100% opaque).

**Only change the color value and linear gradient if you know what you’re doing, as I cannot guarantee that all incorrect entries will be caught.**

**If you are using a linear gradient generator, please copy only the gradient itself. That is, without ‘background: ’ at the start and without ‘;’ at the end, as otherwise the value will be rejected as invalid.**

Only **one linear gradient is permitted**, although **more intermediate values are possible**, as well as a different angle for the gradient and percentage positions.
This already allows for quite a few wild combinations of image and color backgrounds.

When choosing the background image and background color, please ensure that readability is maintained (therefore, only select images and colors that are suitable for the area).

The changes are applied by clicking **‘OK’**. If an incorrect value is entered, a "red error message" appears in the dialog box and the value is reset to its default value.

If **‘Reset to default backgrounds’** is enabled, **clicking ‘OK’ will restore the default settings for image backgrounds.**

If **"Reset to default colors"** is enabled, **clicking "OK" will restore the default settings for the color values.**

*All settings here apply only to the backgrounds and colors of the metal themes.*

#### Section spacing and border color

Here you can set the section spacing for **horizontal and vertical spacing between sections** (to minimise wasted space). Values between **0–50px** are possible. However, I would not recommend setting the values to 0, as the sections will then be right up against one another.

You can also specify a border color.
**However, the border color is only active if a background has been set for the relevant section.**

Changes are applied by clicking **“OK”**. If an incorrect value is entered, a "red error message" appears in the dialog box and the value is reset to its default value.

If **“Reset to default”** is enabled, **clicking “OK” will restore the default settings in this section.**

*All settings here apply only to all sections of the Metal themes.*


## Awesome Leather Themes

All settings are the same as in the Awesome Metal Themes section. See [**Awesome Metal Themes**](#awesome-metal-themes)

*All settings here apply only to all leather themes.*

[🏠 Home](#awesome-theme-collection)


## Support

If you encounter a problem or have a suggestion for improvement, please open an issue in the GitHub repository.


## Changes

v1.1.0
- Different image backgrounds (including your own) are now available (configurable via the integration settings), separately for the metal and leather themes,
  separately for the dashboard and pop-ups (HA dialogues, bubble card pop-ups), for both ‘Light’ and ‘Dark’ modes. 
  (copy your own images to /config/www/wallpaper/) I’ve already added a few extra backgrounds to the selection (labelled _dark and _light as appropriate).

- Multi-level color gradients are also available as backgrounds, separately for the dashboard and pop-ups (HA dialogs, bubble card pop-ups), for both ‘Light’ and ‘Dark’ modes. 
  The image background can also be retained if an alpha value of less than 1 is set in the color gradient or if an optional transparent background has been selected.

- In addition, an entire set of themes can be deactivated (Metal and Leather themes); however, these are only removed from the public area and can be reactivated at any time

- Another new feature is an additional section where the spacing between sections and the border colour for sections can be set separately in both theme areas

- Even more system dialog boxes now feature theme styling


v1.0.5
- adds a subtle border to sections when a background is set

- state-active-color (light) corrected


v1.0.4
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


[🏠 Home](#awesome-theme-collection)
