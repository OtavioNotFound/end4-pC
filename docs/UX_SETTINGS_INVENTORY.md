# Inventário das configurações — base 046a182

Inventário estático do catálogo e de todas as páginas tradicionais. Não é um
schema alternativo: opções geradas dinamicamente são referenciadas pelo componente.
Rótulos são os originais em inglês; traduções ficam nos JSONs existentes.

## Catálogo do dashboard

### Bar / Bar layout

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:187`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `bar:Layout editor` | Bar layout | barlayout  |
### Bar / Positioning & Styles

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:192`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `bar:Show Background` | Bar background | toggle  |
| `bar:Overlap windows when center-only` | Overlap windows | toggle  |
| `bar:Follow Frame Color` | Follow frame color | toggle  |
| `bar:Show Frame` | Screen frame | toggle  |
| `bar:Frame thickness` | Frame thickness | spin  |
| `bar:Autohide` | Autohide | select  |
| `bar:Group style` | Group style | select  |
| `bar:Bar style` | Bar style | select  |
| `bar:Group color` | Group color | swatch  |
| `bar:Frame color` | Frame color | swatch  |
| `bar:Screen rounded corners` | Screen rounded corners | select  |
### Bar / Dynamic Island

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:207`. requires: "dynamicIsland"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `bar:Left widget` | Left widget | select  |
| `bar:Right widget` | Right widget | select  |
| `bar:Visualizer style` | Visualizer style | select  |
| `bar:Show media controls` | Media controls | toggle  |
### Bar / Notifications

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:215`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `bar:Unread indicator: show count` | Unread count | toggle  |
| `bar:Timeout duration (if not defined by notification) (ms)` | Popup timeout (ms) | spin  |
| `bar:Notification position` | Popup position | combo  |
### Bar / Tray

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:222`. requires: "sysTray"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `bar:Make icons pinned by default` | Pinned by default | toggle  |
| `bar:Tint icons` | Tint icons | toggle  |
### Bar / Left sidebar button

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:228`. requires: "leftSidebarButton"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `bar:Icon picker` | Icon | iconpicker  |
| `bar:Icons folder` | Custom icons folder | text  |
| `bar:Colorize icon` | Colorize icon | toggle  |
| `bar:Icon color` | Icon color | swatch  |
### Bar / Divider

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:236`. requires: "divisor"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `bar:Divider/Style` | Divider style | select  |
| `bar:Space width (px)` | Space width | spin  |
### Bar / Utility buttons

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:242`. requires: "utilButtons"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `bar:Screen snip` | Screen snip | toggle  |
| `bar:Color picker` | Color picker | toggle  |
| `bar:Keyboard toggle` | Keyboard toggle | toggle  |
| `bar:Mic toggle` | Mic toggle | toggle  |
| `bar:Dark/Light toggle` | Dark/Light toggle | toggle  |
| `bar:Performance Profile` | Performance profile | toggle  |
| `bar:Record Screen` | Record screen | toggle  |
| `bar:Wallpapers Toggle` | Wallpapers toggle | toggle  |
### Bar / Workspaces

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:254`. requires: "workspaces"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `bar:Always show numbers` | Always show numbers | toggle  |
| `bar:Show app icons` | Show app icons | toggle  |
| `bar:Workspaces shown` | Workspaces shown | spin  |
| `bar:Indicator style` | Indicator style | select  |
| `bar:Numbers style` | Numbers style | select  |
| `bar:Workspaces style` | Workspaces style | select  |
### Bar / Battery

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:264`. requires: "batteryIndicator"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `bar:Battery/Style` | Battery style | batterystyle  |
| `bar:Battery/Show percentage` | Show percentage | toggle  |
| `bar:Battery/Show charging` | Charging bolt | toggle  |
### Bar / Resources

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:271`. requires: "resources"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `bar:CPU` | CPU | toggle  |
| `bar:CPU Temperature` | CPU temperature | toggle  |
| `bar:RAM` | RAM | toggle  |
| `bar:Disk` | Disk | toggle  |
| `bar:Swap` | Swap | toggle  |
| `bar:Show Percentage` | Show percentage | toggle  |
| `bar:Resources/Style` | Style | select  |
| `bar:Polling interval (ms)` | Polling interval (ms) | spin  |
### Bar / Media

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:283`. requires: "media"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `bar:Preferred player` | Preferred player | text  |
| `bar:Pin media controls` | Pin media controls | toggle  |
| `bar:Show only title` | Only title | toggle  |
| `bar:Max media width` | Max media width | spin  |
### Interface / Transparency

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:291`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `interface:Automatic (from wallpaper)` | Auto transparency | toggle  |
| `interface:Transparency/Background` | Background | slider  |
| `interface:Transparency/Content` | Content | slider  |
### Interface / Left Sidebar

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:298`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `interface:Left Sidebar/Enable` | Media player | toggle  |
| `interface:Follow Album Colors` | Album colors | toggle  |
| `interface:Enable Translator` | Translator | toggle  |
| `interface:Enable Football` | Football | toggle  |
| `interface:AI policy` | AI | select  |
| `interface:Weeb policy` | Weeb | select  |
### Interface / Right Sidebar

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:308`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `interface:Banner` | Banner | toggle  |
| `interface:Bottom Group` | Bottom group | toggle  |
| `interface:Right Sidebar/Media Player` | Media player | toggle  |
| `interface:Keep right sidebar loaded` | Keep loaded | toggle  |
| `interface:Right Sidebar/Style` | Quick toggles style | select  |
| `interface:Right Sidebar/Columns` | Toggle columns | spin  |
| `interface:Right Sidebar/Enable` | Quick sliders | toggle  |
| `interface:Brightness` | Brightness slider | toggle  |
| `interface:Volume` | Volume slider | toggle  |
| `interface:Microphone` | Mic slider | toggle  |
### Interface / Hot Corners

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:322`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `interface:Hot Corners/Enable` | Enable | toggle  |
| `interface:Hover to trigger` | Hover to trigger | toggle  |
| `interface:Place at bottom` | Place at bottom | toggle  |
| `interface:Value scroll` | Value scroll | toggle  |
| `interface:Visualize region` | Visualize region | toggle  |
| `interface:Force hover at absolute corner` | Absolute corner | toggle  |
| `interface:Vertical offset` | Vertical offset | spin  |
| `interface:Region width` | Region width | spin  |
| `interface:Region height` | Region height | spin  |
| `interface:Hot corner bottom-left` | Bottom-left | combo  |
| `interface:Hot corner bottom-right` | Bottom-right | combo  |
### Interface / Overview

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:337`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `interface:Overview/Enable` | Enable | toggle  |
| `interface:Center icons` | Center icons | toggle  |
| `interface:Scale (%)` | Scale (%) | spin  |
| `interface:Rows` | Rows | spin  |
| `interface:Overview/Columns` | Columns | spin  |
| `interface:Overview/Style` | Style | select  |
| `interface:Overview order horizontal` | Horizontal order | select  |
| `interface:Overview order vertical` | Vertical order | select  |
### Interface / Dock

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:349`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `interface:Dock/Enable` | Enable | toggle  |
| `interface:Dock/Background` | Background | toggle  |
| `interface:Hover to reveal` | Hover to reveal | toggle  |
| `interface:Pinned on startup` | Pinned on startup | toggle  |
| `interface:Dock/Media Player` | Media player | toggle  |
| `interface:Show Pin Button` | Pin button | toggle  |
| `interface:Show Apps Button` | Apps button | toggle  |
| `interface:Tint app icons` | Tint app icons | toggle  |
| `interface:Dock/Previews` | Window previews | toggle  |
| `interface:Dock/Icon size` | Icon size | spin  |
| `interface:Dock/Icon spacing` | Icon spacing | spin  |
### Interface / Dock style

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:364`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `interface:Dock/Style` | Style | select  |
| `interface:Dock/Position` | Position | select  |
| `interface:Dock/Radius` | Corner radius | spin  |
| `interface:Dock/Magnify` | Magnification | toggle  |
| `interface:Dock/Magnification` | Magnification amount (%) | spin when: "dockmagnify" |
| `interface:Dock/Follow frame color` | Follow frame color | toggle when: "dockhug" |
| `interface:Dock/Border` | Border | toggle when: "dockfloat" |
| `interface:Dock/Border width` | Border width | spin when: "dockfloat" |
| `interface:Dock/Border color` | Border color | swatch when: "dockfloat" |
| `interface:Dock/Background color` | Background color | swatch  |
### Interface / Lock screen

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:378`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `interface:Use Hyprlock (instead of Quickshell)` | Use Hyprlock | toggle  |
| `interface:Launch on startup` | Lock on startup | toggle  |
| `interface:Show Widgets` | Widgets | toggle  |
| `interface:Show Toolbars` | Toolbars | toggle  |
| `interface:Show media player info` | Media info | toggle  |
| `interface:Require password to power off/restart` | Password to power off | toggle  |
| `interface:Also unlock keyring` | Unlock keyring | toggle  |
| `interface:Center clock` | Center clock | toggle  |
| `interface:Use varying shapes for password characters` | Password shapes | toggle  |
| `interface:Enable blur` | Blur | toggle  |
| `interface:Samples` | Blur samples | spin  |
| `interface:Extra wallpaper zoom (%)` | Wallpaper zoom (%) | spin  |
### Interface / Overlay

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:394`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `interface:Enable opening zoom animation` | Opening zoom | toggle  |
| `interface:Darken screen` | Darken screen | toggle  |
| `interface:Floating image source` | Floating image source | text  |
| `interface:Crosshair code` | Crosshair code | text  |
| `interface:Timeout (ms)` | OSD timeout (ms) | spin  |
### Interface / Wallpaper selector

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:403`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `interface:Use system file picker` | System file picker | toggle  |
| `interface:Show home directory in quick access` | Home in quick access | toggle  |
| `interface:Close after selection` | Close after selection | toggle  |
| `interface:Show blur background` | Blur background | toggle  |
| `interface:Always show search bar` | Search bar | toggle  |
| `interface:Columns in grid view` | Grid columns | spin  |
| `interface:Wallpaper change interval (min)` | Change interval (min) | spin  |
| `interface:Custom wallpaper folder` | Custom wallpaper folder | text  |
| `interface:Live wallpaper folder` | Live wallpaper folder | text  |
### Desktop / Wallpaper

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:416`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `desktop:Same wallpaper` | Same wallpaper (lock) | toggle  |
| `desktop:Preview wallpaper` | Preview wallpaper | toggle  |
| `desktop:Blur wall` | Blur wallpaper | toggle  |
| `desktop:Wallpaper change interval (min)` | Change interval (min) | spin  |
| `desktop:Blur Size` | Blur size | slider  |
| `desktop:Split blur amount` | Split blur amount | select  |
| `desktop:Split blur side` | Split blur side | select  |
| `desktop:Transitions` | Transitions | combo  |
### Desktop / Centered wallpaper

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:428`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `desktop:Wallpaper/Centered wallpaper/Enable` | Enable | toggle  |
| `desktop:Wallpaper/Centered wallpaper/Show only when locked` | Only when locked | toggle  |
| `desktop:Wallpaper/Centered wallpaper/Size` | Size | slider  |
| `desktop:Centered color` | Background color | swatch  |
| `desktop:Centered shape` | Shape | shape  |
### Desktop / Multiple wallpapers

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:437`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `desktop:Collage enable` | Enable | toggle  |
| `desktop:Collage layouts` | Layouts | collagelayouts  |
| `desktop:Collage gap` | Spacing | spin  |
| `desktop:Collage margin` | Outer margin | spin  |
| `desktop:Collage radius` | Corner radius | spin  |
### Desktop / Desktop widgets

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:446`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `desktop:Widgets` | Desktop widgets | widgets  |
### Desktop / Clock

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:451`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `desktop:Clock/Enable` | Enable | toggle  |
| `desktop:Clock/Show only when locked` | Only when locked | toggle  |
| `desktop:Placement strategy` | Placement | select  |
| `desktop:Clock style` | Style | select  |
| `desktop:Clock style (locked)` | Style (locked) | select  |
### Desktop / Digital clock

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:460`. when: "clockdigital"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `desktop:Vertical` | Vertical | toggle  |
| `desktop:Animate time change` | Animate change | toggle  |
| `desktop:Show date` | Show date | toggle  |
| `desktop:Use adaptive alignment` | Adaptive alignment | toggle  |
| `desktop:Clock auto colors` | Automatic colors | toggle  |
| `desktop:Clock color` | Color | swatch  |
| `desktop:Clock font family` | Font family | combo  |
| `desktop:Font weight` | Weight | slider  |
| `desktop:Font size` | Size | slider  |
| `desktop:Font width` | Width | slider  |
| `desktop:Font roundness` | Roundness | slider  |
### Desktop / Cookie clock

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:475`. when: "clockcookie"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `desktop:Auto styling with Gemini` | Auto styling (Gemini) | toggle  |
| `desktop:Use old sine wave cookie implementation` | Old sine cookie | toggle  |
| `desktop:Constantly rotate` | Constantly rotate | toggle  |
| `desktop:Hour marks` | Hour marks | toggle  |
| `desktop:Digits in the middle` | Digits in the middle | toggle  |
| `desktop:Sides` | Sides | spin  |
| `desktop:Dial Style` | Dial style | select  |
| `desktop:Hour hand` | Hour hand | select  |
| `desktop:Minute hand` | Minute hand | select  |
| `desktop:Second hand` | Second hand | select  |
| `desktop:Date style` | Date style | select  |
### Desktop / Daily clock

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:490`. when: "clockdaily"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `desktop:Daily clock variant` | Variant | select  |
| `desktop:Clock auto colors` | Automatic colors | toggle  |
| `desktop:Clock color` | Color | swatch  |
### Desktop / Pixel clock

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:497`. when: "clockpixel"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `desktop:Pixel clock orientation` | Orientation | select  |
### Desktop / Quote

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:502`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `desktop:Clock/Quote/Enable` | Enable | toggle  |
| `desktop:Follow Clock Font` | Follow clock font | toggle  |
| `desktop:Quote text` | Quote | text  |
### Desktop / Custom image

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:509`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `desktop:Custom Image/Enable` | Enable | toggle  |
| `desktop:Image shape` | Shape | shape  |
| `desktop:Image card/Enable` | Image card | toggle  |
| `desktop:Image card layout` | Image card layout | select  |
### Desktop / Visualizer

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:517`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `desktop:Visualizer enable` | Enable | toggle  |
| `desktop:Visualizer style` | Style | select  |
| `desktop:Visualizer colors` | Colors | select  |
| `desktop:Visualizer sensitivity` | Sensitivity (%) | slider  |
| `desktop:Visualizer height` | Height | slider  |
| `desktop:Visualizer size` | Ring size | slider  |
### Desktop / Text

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:527`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `desktop:Text enable` | Enable | toggle  |
| `desktop:Text shadow` | Shadow | toggle  |
| `desktop:Text auto colors` | Automatic colors | toggle  |
| `desktop:Text content` | Text to display | text  |
| `desktop:Text font family` | Font family | combo  |
| `desktop:Text custom font` | Custom font | text  |
| `desktop:Text size` | Font size | slider  |
| `desktop:Text alignment` | Alignment | select  |
| `desktop:Text color` | Color | swatch  |
### Desktop / Canvas

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:540`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `desktop:Show alignment grid while dragging` | Alignment grid | toggle  |
| `desktop:Show snap lines when dropping` | Snap lines | toggle  |
### General / System Appearance

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:546`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `general:Icon theme` | Icon theme | combo  |
| `general:Follow icon color scheme` | Follow color scheme | toggle  |
| `general:Dynamic icon accent colors` | Dynamic accent colors | toggle  |
| `general:Prevent Breeze icon override` | Prevent Breeze override | toggle  |
| `general:Cursor theme` | Cursor theme | combo  |
| `general:System font` | System font | combo  |
| `general:Monospace font` | Monospace font | combo  |
| `general:Cursor size` | Cursor size | spin  |
| `general:System font size` | System font size | spin  |
| `general:Monospace font size` | Mono font size | spin  |
### General / Time

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:560`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `general:Time preview` | Preview | timepreview  |
| `general:Second precision` | Second precision | toggle  |
| `general:Show date` | Show date | toggle  |
| `general:Format` | Time format | select  |
### General / Battery

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:568`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `general:Low warning` | Low warning | spin  |
| `general:Critical warning` | Critical warning | spin  |
| `general:Full warning` | Full warning | spin  |
| `general:Automatic suspend` | Automatic suspend | toggle  |
### General / Audio

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:576`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `general:Earbang protection` | Earbang protection | toggle  |
| `general:Max allowed increase` | Max allowed increase | spin  |
| `general:Volume limit` | Volume limit | spin  |
### General / Sounds

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:583`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `general:Sounds/Battery` | Battery sounds | toggle  |
| `general:Sounds/Pomodoro` | Pomodoro sounds | toggle  |
| `interface:Football/Alerts` | Football live alerts | toggle when: "football" |
| `interface:Football/Scope` | Football alerts for | select when: "football" |
| `interface:Football/Goal sound` | Goal sound | toggle when: "football" |
| `interface:Football/Goal file` | Goal sound file (empty = default) | text when: "football" |
| `interface:Football/Corner sound` | Corner sound | toggle when: "football" |
| `interface:Football/Corner file` | Corner sound file (empty = default) | text when: "football" |
| `interface:Football/Notify` | Goal notifications | toggle when: "football" |
| `interface:Football/Volume` | Sound volume | spin when: "football" |
### General / Language

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:597`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `general:Interface language` | Interface language | combo  |
### General / Work safety

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:602`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `general:Hide clipboard images copied from sussy sources` | Hide clipboard images | toggle  |
| `general:Hide sussy/anime wallpapers` | Hide sussy wallpapers | toggle  |
### Hyprland / Layout

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:608`. when: "hyprland"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `hyprland:Tiling Layout` | Tiling layout | select  |
| `hyprland:Gaps In` | Gaps in | spin  |
| `hyprland:Gaps Out` | Gaps out | spin  |
### Hyprland / Dwindle

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:615`. when: "layoutdwindle"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `hyprland:opt:dwindle:preserve_split` | Preserve split direction | toggle  |
| `hyprland:opt:dwindle:smart_split` | Smart split (follow cursor) | toggle  |
| `hyprland:opt:dwindle:force_split` | Force split side | select  |
| `hyprland:opt:dwindle:default_split_ratio` | Default split ratio | spin  |
### Hyprland / Master

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:623`. when: "layoutmaster"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `hyprland:opt:master:new_status` | New windows become | select  |
| `hyprland:opt:master:orientation` | Master position | select  |
| `hyprland:opt:master:mfact` | Master size | spin  |
### Hyprland / Keyboard

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:630`. when: "hyprland"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `hyprland:Numlock by default` | Numlock by default | toggle  |
| `hyprland:Repeat delay (ms)` | Repeat delay (ms) | spin  |
| `hyprland:Repeat rate` | Repeat rate | spin  |
| `hyprland:opt:input:kb_variant` | Keyboard variant | text  |
| `hyprland:opt:input:kb_options` | Keyboard options | text  |
### Hyprland / Mouse

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:639`. when: "hyprland"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `hyprland:Follow mouse` | Follow mouse | select  |
| `hyprland:opt:input:sensitivity` | Pointer sensitivity | spin  |
| `hyprland:opt:input:accel_profile` | Acceleration profile | select  |
| `hyprland:opt:input:force_no_accel` | Disable acceleration | toggle  |
| `hyprland:opt:input:left_handed` | Left-handed buttons | toggle  |
| `hyprland:opt:misc:middle_click_paste` | Middle click paste | toggle  |
### Hyprland / Touchpad

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:649`. when: "hyprland"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `hyprland:Natural scroll` | Natural scroll | toggle  |
| `hyprland:Disable while typing` | Disable while typing | toggle  |
| `hyprland:Clickfinger behavior` | Clickfinger behavior | toggle  |
| `hyprland:Scroll factor` | Scroll factor | spin  |
| `hyprland:opt:input:touchpad:tap-to-click` | Tap to click | toggle  |
| `hyprland:opt:input:touchpad:tap-and-drag` | Tap and drag | toggle  |
| `hyprland:opt:input:touchpad:middle_button_emulation` | Middle button emulation | toggle  |
### Hyprland / Idle

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:660`. when: "hyprland"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `hyprland:Idle lock` | Lock screen | duration  |
| `hyprland:Idle screen off` | Screen off | duration  |
| `hyprland:Idle standby` | Standby | duration  |
### Hyprland / Visual & Aesthetics

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:667`. when: "hyprland"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `hyprland:Window Rounding` | Window rounding | spin  |
| `hyprland:Border Size` | Border size | spin  |
| `hyprland:Active Opacity` | Active opacity | spin  |
| `hyprland:Inactive Opacity` | Inactive opacity | spin  |
| `hyprland:Custom border colors` | Custom border colors | toggle  |
### Hyprland / Border colors

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:676`. when: "hyprbordercolor"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `hyprland:Active border color` | Active border | swatch  |
| `hyprland:Inactive border color` | Inactive border | swatch  |
| `hyprland:Active border opacity` | Active border opacity | spin  |
| `hyprland:Inactive border opacity` | Inactive border opacity | spin  |
### Hyprland / Shadows, dimming & blur

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:684`. when: "hyprland"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `hyprland:opt:decoration:shadow:enabled` | Window shadows | toggle  |
| `hyprland:opt:decoration:shadow:range` | Shadow range | spin  |
| `hyprland:opt:decoration:dim_inactive` | Dim inactive windows | toggle  |
| `hyprland:opt:decoration:dim_strength` | Dim strength | spin  |
| `hyprland:Blur` | Window blur | toggle  |
| `hyprland:Blur Size` | Blur size | spin  |
| `hyprland:Blur Passes` | Blur passes | spin  |
| `hyprland:opt:decoration:blur:noise` | Blur noise | spin  |
| `hyprland:opt:decoration:blur:vibrancy` | Blur vibrancy | spin  |
### Hyprland / Misc

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:697`. when: "hyprland"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `hyprland:Focus on activate` | Focus on activate | toggle  |
| `hyprland:opt:misc:vrr` | Variable refresh rate | select  |
| `hyprland:opt:misc:enable_swallow` | Window swallowing | toggle  |
| `hyprland:opt:misc:animate_manual_resizes` | Animate manual resizes | toggle  |
| `hyprland:opt:misc:close_special_on_empty` | Close empty special workspace | toggle  |
| `hyprland:opt:misc:disable_hyprland_logo` | Hide Hyprland logo | toggle  |
| `hyprland:opt:misc:disable_splash_rendering` | Hide splash text | toggle  |
| `hyprland:opt:misc:mouse_move_enables_dpms` | Mouse wakes the screen | toggle  |
| `hyprland:opt:misc:key_press_enables_dpms` | Keys wake the screen | toggle  |
| `hyprland:opt:xwayland:force_zero_scaling` | XWayland sharp apps | toggle  |
| `hyprland:opt:group:auto_group` | Auto-group dragged windows | toggle  |
| `hyprland:opt:binds:workspace_back_and_forth` | Workspace back and forth | toggle  |
| `hyprland:opt:binds:allow_workspace_cycles` | Allow workspace cycles | toggle  |
| `hyprland:opt:render:direct_scanout` | Direct scanout | select  |
### Hyprland / Windows

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:715`. when: "hyprland"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `hyprland:opt:general:resize_on_border` | Resize on borders | toggle  |
| `hyprland:opt:general:extend_border_grab_area` | Border grab area (px) | spin  |
| `hyprland:opt:general:allow_tearing` | Allow tearing | toggle  |
### Hyprland / Cursor

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:722`. when: "hyprland"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `hyprland:opt:cursor:no_hardware_cursors` | Hardware cursor | select  |
| `hyprland:opt:cursor:inactive_timeout` | Hide cursor after (s) | spin  |
| `hyprland:opt:cursor:hide_on_key_press` | Hide cursor while typing | toggle  |
| `hyprland:opt:cursor:warp_on_change_workspace` | Warp to new workspace | select  |
### Hyprland / Animations

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:730`. when: "hyprland"

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `hyprland:Enable` | Animations | toggle  |
| `hyprland:Presets` | Animation presets | select  |
### Services / Music Recognition

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:736`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `services:Total duration timeout (s)` | Timeout (s) | spin  |
| `services:Polling interval (s)` | Polling interval (s) | spin  |
### Services / Save paths

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:742`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `services:Video recording path` | Video recording path | text  |
| `services:Screenshot path` | Screenshot path (empty = copy) | text  |
### Services / Search

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:748`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `services:Use Levenshtein distance-based algorithm instead of fuzzy` | Levenshtein search | toggle  |
| `services:Show clipboard preview popups` | Clipboard previews | toggle  |
| `services:Base URL` | Web search base URL | text  |
| `services:Prefix action` | Prefix: Action | text  |
| `services:Prefix clipboard` | Prefix: Clipboard | text  |
| `services:Prefix emojis` | Prefix: Emojis | text  |
| `services:Prefix symbols` | Prefix: Icons | text  |
| `services:Prefix shell` | Prefix: Shell command | text  |
| `services:Prefix web` | Prefix: Web search | text  |
| `services:Prefix app` | Prefix: Apps | text  |
| `services:Prefix keybinds` | Prefix: Keybinds | text  |
### Services / Webapps

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:763`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `services:Webapps` | Webapps | webapps  |
### Services / System updates (Arch)

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:768`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `services:Enable update checks` | Update checks | toggle  |
| `services:Check interval (mins)` | Check interval (min) | spin  |
### Services / Weather

Fonte: `modules/ii/settings/DashboardSettingsCatalog.qml:774`.

| Chave estável | Rótulo | Tipo / condição |
|---|---|---|
| `services:Weather map` | Weather location | weathermap  |
| `services:Enable GPS based location` | GPS location | toggle  |
| `services:Fahrenheit unit` | Fahrenheit | toggle  |
| `services:Polling interval (m)` | Polling interval (m) | spin  |
| `services:City name` | City name | text  |

Total: **63 seções, 344 cards** (além dos hero cards de DashboardSettingsPage).

## Páginas tradicionais

### About

Fonte: `modules/ii/settings/pages/About.qml`; 208 linhas. 0 rótulos estáticos capturados.

Conteúdo composto/gerado: inspecionado pelo componente, não pelo extrator de rótulos.

### BackgroundConfig

Fonte: `modules/ii/settings/pages/BackgroundConfig.qml`; 1617 linhas. 95 rótulos estáticos capturados.

- Wallpaper
- Desktop
- Lockscreen
- Use same wallpaper for both
- Preview wallpaper
- Blur wall
- Blur Size
- Split blur amount
- Split blur side
- Wallpaper change interval (min)
- Transitions
- Live wallpaper
- Pause on battery
- Pause below charge (%, 0 to ignore)
- Centered wallpaper
- Enable
- Show only when locked
- Background Color
- Size
- Multiple wallpapers
- Layout
- Spacing
- Outer margin
- Corner radius
- Arrange the tiles from the desktop while widgets are unlocked: split, remove, change the image and drag the borders. The starred tile sets the colors and the blurred backdrop.
- Reset layout
- Clock
- Placement strategy
- Clock style
- Clock style (locked)
- Digital clock settings
- Vertical
- Animate time change
- Show date
- Use adaptive alignment
- Automatic colors
- Color
- Font family
- Font weight
- Font size
- Font width
- Font roundness
- Cookie clock settings
- Auto styling with Gemini
- Use old sine wave cookie implementation
- Sides
- Constantly rotate
- Hour marks
- Digits in the middle
- Hour hand
- Minute hand
- Second hand
- Date style
- Pixel Clock Settings
- Pixel clock orientation
- Quote
- Follow Clock Font
- Custom Image
- Image card
- Image card layout
- Visualizer
- Style
- Colors
- Sensitivity (%)
- Height
- Text
- Shadow
- Text to display
- Double-click the text on your desktop to edit it, drag its corner to resize it
- Font
- Custom Font
- Alignment
- Widgets
- Show widgets on
- Also in the desktop menu
- Canvas
- Show alignment grid while dragging
- Show snap lines when dropping

### BarConfig

Fonte: `modules/ii/settings/pages/BarConfig.qml`; 938 linhas. 75 rótulos estáticos capturados.

- Screens
- Show bar on
- All
- Bar layout
- Positioning & Styles
- Bar position
- Bar style
- Group style
- Group Color
- Show Background
- Autohide
- Overlap windows when center-only
- Show Frame
- Follow Frame Color
- Frame thickness
- Frame Color
- Dynamic Island
- Left widget
- Right widget
- Media
- Visualizer style
- Show media controls
- Notifications
- Popup position
- Unread indicator: show count
- Timeout duration (if not defined by notification) (ms)
- Tray
- Make icons pinned by default
- Tint icons
- Left sidebar button
- Icon
- Custom icons folder
- Colorize icon
- Icon color
- Divider
- Style
- Space width (px)
- Utility buttons
- Screen snip
- Color picker
- Keyboard toggle
- Mic toggle
- Dark/Light toggle
- Performance Profile
- Record Screen
- Wallpapers Toggle
- Workspaces
- Workspaces shown
- Always show numbers
- Numbers style
- Show app icons
- Indicator style
- Battery
- Battery style
- Show percentage
- Charging bolt
- Resources
- CPU
- CPU Temperature
- RAM
- Disk
- Swap
- Show Percentage
- Polling interval (ms)
- Preferred Player
- Pin media controls
- Show only title
- Max media width
- Tooltips
- Enable
- Click to show

### GeneralConfig

Fonte: `modules/ii/settings/pages/GeneralConfig.qml`; 636 linhas. 49 rótulos estáticos capturados.

- System Appearance
- Icon theme
- Follow color scheme
- Dynamic accent colors
- Prevent Breeze override
- Cursor theme
- Cursor size
- System font
- System font size
- Monospace font
- Monospace font size
- Time
- Format
- Second precision
- Show date
- Clock String Format
- Date String Format
- Device batteries
- Low warning
- Critical warning
- Notify when a device battery is low
- Battery
- Automatic suspend
- at
- Full warning
- Audio
- Earbang protection
- Max allowed increase
- Volume limit
- Sounds
- Pomodoro
- Football
- Live alerts
- Alerts for
- Goal sound
- Goal sound file (empty = default)
- Corner sound
- Corner sound file (empty = default)
- Goal notifications
- Sound volume
- Language
- Interface Language
- Locale code
- Work safety
- Hide clipboard images copied from sussy sources
- Hide sussy/anime wallpapers

### HyprlandConfig

Fonte: `modules/ii/settings/pages/HyprlandConfig.qml`; 1249 linhas. 107 rótulos estáticos capturados.

- Displays
- Enabled
- Resolution & Refresh Rate
- Orientation
- Scale
- Position X
- Position Y
- HDR & Color Management
- Couldn't confirm this display's HDR capability from its EDID. Options are shown but may not do anything.
- This display's EDID does not report HDR support, so HDR options are disabled here. Open an issue in GitHub if you think this is a mistake.
- Bit depth
- Color management
- SDR brightness
- SDR saturation
- SDR min (nits)
- SDR max (nits)
- HDR min (nits)
- HDR peak (nits)
- HDR max average luminance (nits)
- Layout
- Tiling Layout
- Dwindle
- Preserve split direction
- Smart split (follow the cursor)
- Force split side
- Default split ratio
- Master
- New windows become
- Master position
- Master size
- Input
- Keyboard
- Keyboard layout
- Numlock by default
- Repeat delay (ms)
- Repeat rate
- Keyboard variant
- Keyboard options
- Follow mouse
- Mouse
- Pointer sensitivity
- Acceleration profile
- Disable acceleration (raw input)
- Left-handed buttons
- Middle click paste
- Touchpad
- Natural scroll
- Disable while typing
- Clickfinger behavior
- Tap to click
- Tap and drag
- Middle button emulation (3-finger tap)
- Scroll factor
- Idle
- Visual & Aesthetics
- Window Rounding
- Blur
- Blur Size
- Blur Passes
- Gaps In
- Gaps Out
- Active Opacity
- Inactive Opacity
- Border Size
- Custom border colors
- Border Color Management
- Active border
- Active border opacity
- Inactive border
- Inactive border opacity
- Shadows, dimming & blur
- Window shadows
- Shadow range
- Dim inactive windows
- Dim strength
- Blur noise
- Blur vibrancy
- Misc
- Focus on activate
- Variable refresh rate (VRR)
- Window swallowing (terminal swallows launched apps)
- Animate manual resizes
- Close empty special workspace
- Hide the Hyprland logo
- Hide the splash text
- Mouse wakes the screen
- Keys wake the screen
- XWayland: sharp apps (force zero scaling)
- Auto-group dragged windows
- Switching to the current workspace goes back
- Allow workspace cycles
- Direct scanout (fullscreen apps)
- Windows & Cursor
- Windows
- Resize windows by dragging their borders
- Border grab area (px)
- Allow tearing (lower latency in games)
- Cursor
- Hardware cursor
- Hide cursor after inactivity (s, 0 = never)
- Hide cursor while typing
- Move cursor to the new workspace
- Autostart Apps
- Animations
- Enable
- Presets
- Animation presets require a require line in your hyprland.lua. Add the following line to enable presets:

### InterfaceConfig

Fonte: `modules/ii/settings/pages/InterfaceConfig.qml`; 1542 linhas. 136 rótulos estáticos capturados.

- Color Schemes
- Color scheme
- Material follows your wallpaper
- Accent
- Secondary
- Transparency
- Enable
- Automatic (from wallpaper)
- Background
- Content
- Settings Panel
- Style
- Dashboard animation speed
- Border width
- Border Color
- Left Sidebar
- Media Player
- Follow Album Colors
- AI
- Weeb
- Enable Translator
- Football
- Right Sidebar
- Quick toggles
- Columns
- Sliders
- Brightness
- Volume
- Microphone
- Hot Corners
- Top
- Hover to trigger
- Place at bottom
- Value scroll
- Visualize region
- Force hover at absolute corner
- Vertical offset
- Region width
- Region height
- Bottom
- Bottom-left
- Bottom-right
- Overview
- Center icons
- Scale (%)
- Default Settings
- Rows
- Dock
- Hover to reveal
- Pinned on startup
- Appearance
- Magnification
- Magnification amount (%)
- Position
- Corner radius
- Background color
- Follow frame color
- Border
- Border color
- Icons
- Window previews
- Icon size
- Icon spacing
- Buttons & Media
- Show Pin Button
- Show Apps Button
- Tint app icons
- Lock screen
- Use Hyprlock (instead of Quickshell)
- Launch on startup
- Show Widgets
- Show Toolbars
- Show media player info
- Security
- Require password to power off/restart
- Also unlock keyring
- Style: General
- Center clock
- Use varying shapes for password characters
- Style: Blurred
- Enable blur
- Samples
- Extra wallpaper zoom (%)
- Overlay
- Enable opening zoom animation
- Darken screen
- Floating Image
- Image source
- Crosshair
- Crosshair code
- Press Super+G to open the overlay and pin the crosshair
- Region selector (screen snipping/Google Lens)
- Hint target regions
- Google Lens
- Selection Type
- Rectangular selection
- Show aim lines
- Circle selection
- Stroke width
- Padding
- On-screen display
- Timeout (ms)
- Wallpaper selector
- Columns in grid view
- Wallpaper change interval (min)
- Custom Wallpaper Folder
- Live Wallpaper Folder
- Fonts
- Main font
- Numbers font
- Title font
- Monospace font
- Nerd Fonts icons
- Reading font
- Expressive font
- Color generation
- Shell & utilities
- Qt apps
- Terminal
- Keep Konsole color scheme
- Force dark mode in terminal
- Terminal: Harmony (%)
- Terminal: Harmonize threshold
- Terminal: Foreground boost (%)

### NiriConfig

Fonte: `modules/ii/settings/pages/NiriConfig.qml`; 662 linhas. 50 rótulos estáticos capturados.

- Displays
- Enabled
- Resolution & Refresh Rate
- Orientation
- Variable refresh rate (VRR)
- Scale
- Position X
- Position Y
- Layout
- Gaps
- Center focused column
- Default column width
- Input
- Keyboard
- Keyboard layout
- Numlock by default
- Repeat delay (ms)
- Repeat rate
- Focus follows mouse
- Touchpad
- Tap to click
- Natural scroll
- Disable while typing
- Scroll factor
- Acceleration speed
- Mouse
- Visual & Aesthetics
- Window Rounding
- Border
- Border Size
- Focus ring
- Focus ring width
- Shadows
- Shadow softness
- Shadow spread
- Blur
- Blur Passes
- Blur Offset
- Blur Noise (%)
- Blur Saturation (%)
- Cursor
- Cursor theme
- Cursor size
- Hide while typing
- Animations
- Enable
- Slowdown (×10)

### Profile

Fonte: `modules/ii/settings/pages/Profile.qml`; 868 linhas. 16 rótulos estáticos capturados.

- Avatar
- Avatar path
- Pick a folder above to see avatars here
- Identity
- Display name
- Hostname
- Requires authentication to change
- Description text
- Presets
- Save as
- Import ZIP
- Show online presets
- No presets yet
- Downloaded
- Imported
- Browse Online

### QuickConfig

Fonte: `modules/ii/settings/pages/QuickConfig.qml`; 587 linhas. 1 rótulos estáticos capturados.

- Wallpaper & Colors

### ServicesConfig

Fonte: `modules/ii/settings/pages/ServicesConfig.qml`; 463 linhas. 34 rótulos estáticos capturados.

- AI
- Networking
- Music Recognition
- Total duration timeout (s)
- Polling interval (s)
- Save paths
- Video Recording Path
- Screenshot Path (leave empty to just copy)
- Search
- Use Levenshtein distance-based algorithm instead of fuzzy
- Show clipboard preview popups
- Prefixes
- Action
- Clipboard
- Emojis
- Icons
- Shell command
- Web search
- Apps
- Keybinds
- Base URL
- Webapps
- Website URL
- Could not create: %1
- Your webapps
- System updates (Arch only)
- Enable update checks
- Check interval (mins)
- Weather
- Enable GPS based location
- Fahrenheit unit
- Polling interval (m)
- City name

## Componentes compostos e fluxos revisados

`DashboardContent`, `DashboardSettingsPage`, `DashboardSettingsCatalog`,
`Settings`, `SettingsContent`, `SettingsPages`, `SettingsSearchIndex`,
`SettingsQuickControls`, `DashboardGroupRail`, `DashboardBarLayoutCard`,
`DashboardBarPositionCard`, `DashboardWidgetsCard`, `DashboardSchemeCard`,
`DashboardWallpapersPage`, `DashboardPresetsPage`, `DashboardPresetDetail`,
`MonitorConfigOption` (Hyprland/Niri), `FirstRunExperience`, `welcome.qml`,
`WallpaperResources`, `Presets`, `Weather`, `Cliphist`, `HyprlandOptions` e
`doctor.py`. As listas geradas desses componentes continuam nas fontes originais.
