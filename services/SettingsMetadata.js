.pragma library

// Presentation only. Stable control/config keys and their defaults stay upstream.
var entries = {
    "interface:Glassy UI": { description: "Applies a glass effect to panels using the current wallpaper. Compositor blur is separate.", keywords: "glass glassy frosted vidro papel parede wallpaper blur", effect: "Immediate; requires a valid wallpaper image." },
    "interface:Transparency/Enable": { description: "Enables background transparency. Glassy UI is a separate effect.", keywords: "transparency opacity transparent transparência opacidade", effect: "Immediate." },
    "interface:Automatic (from wallpaper)": { description: "Adjusts background transparency from wallpaper colors and uses the original automatic content value. Manual values remain saved.", keywords: "automatic auto wallpaper automático transparência", effect: "Immediate." },
    "interface:Transparency/Background": { description: "Saved background transparency. Turn off automatic transparency to use this value.", keywords: "opacity manual opacidade fundo", unit: "%", percent: true, effect: "Immediate in manual mode." },
    "interface:Transparency/Content": { description: "Saved content transparency. Automatic mode overrides it; Glassy UI imposes the original minimum transparency.", keywords: "opacity manual opacidade conteúdo glass vidro", unit: "%", percent: true, effect: "Immediate in manual mode." },
    "desktop:Blur wall": { description: "Blurs the wallpaper, independently of panel transparency and Glassy UI.", keywords: "blur wallpaper desfoque papel parede", effect: "Immediate." },
    "desktop:Blur Size": { description: "Wallpaper blur radius in pixels.", keywords: "radius pixels raio desfoque", unit: "px", effect: "Immediate." },
    "desktop:Wallpaper change interval (min)": { description: "Time between automatic wallpaper changes. Zero disables automatic changes.", keywords: "slideshow automatic papel parede intervalo automático", unit: "min" },
    "interface:Wallpaper change interval (min)": { description: "Time between automatic wallpaper changes. Zero disables automatic changes.", keywords: "slideshow wallpaper intervalo automático", unit: "min" },
    "interface:Dock/Enable": { description: "Shows the application dock. Its style and position are configured in the same category.", keywords: "dock apps aplicativos atalhos", effect: "Immediate." },
    "interface:Hover to reveal": { description: "Reveals the dock when the pointer reaches its edge.", keywords: "dock autohide ocultar mouse ponteiro", effect: "Immediate." },
    "interface:Pinned on startup": { description: "Keeps the dock visible when the shell starts.", keywords: "dock startup inicialização fixar", effect: "Next shell start." },
    "interface:Dock/Position": { description: "Chooses the screen edge used by the dock.", keywords: "dock edge left right bottom posição canto", effect: "Immediate." },
    "interface:Dock/Style": { description: "Hug attaches the dock to the screen edge; Float leaves space around it.", keywords: "dock hug float floating flutuante borda", effect: "Immediate." },
    "interface:Dock/Magnify": { description: "Enlarges dock icons near the pointer without changing their saved base size.", keywords: "dock zoom magnify ampliar ícones", effect: "Immediate." },
    "interface:Dock/Magnification": { description: "Additional magnification near the pointer. Requires dock magnification.", keywords: "zoom dock ampliar", unit: "%" },
    "interface:Dock/Icon size": { description: "Base size of dock icons in pixels.", unit: "px", keywords: "dock ícones tamanho" },
    "interface:Dock/Icon spacing": { description: "Space between dock icons in pixels.", unit: "px" },
    "interface:Dock/Radius": { description: "Radius of dock corners in pixels.", unit: "px" },
    "bar:Space width (px)": { description: "Width of the spacer between bar widgets.", unit: "px", keywords: "bar spacing separador barra" },
    "bar:Frame thickness": { description: "Thickness of the screen frame in pixels.", unit: "px" },
    "bar:Autohide": { description: "Controls when the bar hides and reappears near the screen edge.", keywords: "bar hide barra ocultar", effect: "Immediate." },
    "bar:Polling interval (ms)": { description: "Time between resource usage updates. Smaller values update more often.", unit: "ms", keywords: "cpu ram refresh atualização intervalo" },
    "bar:Timeout duration (if not defined by notification) (ms)": { description: "Notification display time when the application does not provide one.", unit: "ms" },
    "general:Earbang protection": { title: "Volume jump protection", description: "Limits sudden volume increases to protect your hearing.", keywords: "earbang hearing volume audio ouvido proteção" },
    "services:Use Levenshtein distance-based algorithm instead of fuzzy": { title: "Typo-tolerant search", description: "Uses edit distance to match misspelled words instead of the original fuzzy search.", keywords: "levenshtein fuzzy typo search busca erros digitação" },
    "interface:Weeb policy": { title: "Anime content", description: "Controls the visibility of anime-related features. Existing policy values are preserved.", keywords: "weeb anime conteúdo" },
    "services:Polling interval (m)": { title: "Weather update interval", description: "Time between weather updates, in minutes.", unit: "min", keywords: "weather clima tempo atualização intervalo" },
    "services:City name": { description: "Used for weather when GPS is disabled or unavailable.", keywords: "weather city manual clima cidade localização" },
    "services:Enable GPS based location": { description: "Requests automatic location for weather. If the GPS backend is unavailable, the configured city is used.", keywords: "gps geoclue location weather localização cidade clima" },
    "services:Show clipboard preview popups": { description: "Shows a preview when browsing clipboard history. Requires cliphist.", keywords: "clipboard cliphist histórico área transferência" },
    "services:Check interval (mins)": { description: "Time between Arch package update checks.", unit: "min" },
    "services:Total duration timeout (s)": { description: "Maximum time allowed for music recognition.", unit: "s" },
    "services:Polling interval (s)": { description: "Time between music recognition checks.", unit: "s" },
    "hyprland:Window Rounding": { description: "Corner radius of application windows, controlled by Hyprland.", unit: "px" },
    "hyprland:Border Size": { description: "Width of application window borders.", unit: "px" },
    "hyprland:Active Opacity": { description: "Opacity of the focused application window, separate from shell transparency.", unit: "%" },
    "hyprland:Inactive Opacity": { description: "Opacity of unfocused application windows, separate from shell transparency.", unit: "%" },
    "hyprland:Presets": { description: "Changes compositor animation presets. Requires the animation include described in the full Hyprland settings.", keywords: "animation require animações preset", effect: "Applied by Hyprland." },
    "general:Dynamic icon accent colors": { description: "Recolors supported icon themes. Unsupported themes may only support light and dark variants.", keywords: "icons accent cores ícones tema", effect: "External applications may need to reopen." },
    "general:System font": { description: "Changes the system application font, independently of the shell font.", keywords: "font gtk qt fonte sistema", effect: "External applications may need to reopen." }
};

var pageKeywords = {
    quick: "appearance dark light wallpaper colors modo escuro claro tema papel parede",
    general: "system icons cursor fonts language idioma fonte ícones sistema",
    bar: "bar dock position widgets barra posição atalhos",
    desktop: "wallpaper background widgets clock papel parede relógio fundo",
    interface: "appearance transparency glass dock fonts colors aparência vidro transparência fontes",
    hyprland: "monitor display resolution scale keyboard mouse autostart tela monitor resolução escala teclado inicialização",
    niri: "monitor display resolution scale keyboard mouse tela resolução escala teclado",
    services: "weather gps clipboard dependencies clima localização histórico dependências",
    about: "diagnostic dependencies health diagnóstico dependências integridade"
};

function forKey(key) { return entries[key] ?? {}; }

function category(value, translate) {
    const tr = translate ?? (text => text);
    const aliases = { general: ["General", "Geral"], interface: ["Interface", "Appearance", "Aparência"],
        bar: ["Bar", "Bar & dock", "Barra", "Barra e dock"], desktop: ["Desktop", "Desktop & widgets", "Área de trabalho"],
        hyprland: ["Hyprland"], niri: ["Niri"], services: ["Services", "Serviços"] };
    if (Object.prototype.hasOwnProperty.call(aliases, value)) return value;
    for (const id of Object.keys(aliases))
        if (aliases[id].some(label => label === value || tr(label) === value)) return id;
    return "";
}

function categoryTitle(id) {
    return ({ general: "General", interface: "Appearance", bar: "Bar & dock", desktop: "Desktop & widgets", hyprland: "Hyprland", niri: "Niri", services: "Services" })[id] ?? "All";
}

function displayValue(key, value, percent, from, to) {
    const meta = forKey(key);
    if (meta.percent) return Math.round(value * 100) + "%";
    if (meta.unit) return Math.round(value) + " " + meta.unit;
    if (percent) return Math.round(to === from ? 0 : (value - from) / (to - from) * 100) + "%";
    return String(Math.round(value));
}
