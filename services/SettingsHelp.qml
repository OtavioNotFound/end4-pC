pragma Singleton

import QtQuick
import Quickshell
import qs.modules.common
import qs.services
import "SettingsMetadata.js" as Metadata

Singleton {
    id: root

    function title(key, fallback) {
        const name = Metadata.forKey(key).title
        return name ? Translation.tr(name) : fallback
    }

    function category(value) { return Metadata.category(value, Translation.tr) }
    function categoryTitle(id) { return Translation.tr(Metadata.categoryTitle(id)) }
    function unit(key) { return Metadata.forKey(key).unit ?? "" }
    function displayValue(key, value, percent, from, to) { return Metadata.displayValue(key, value, percent, from, to) }

    function text(key) {
        const data = Metadata.forKey(key)
        return [data.description ? Translation.tr(data.description) : "", data.effect ? Translation.tr(data.effect) : "", root.warning(key)].filter(value => value).join("\n")
    }

    function warning(key) {
        if (key === "interface:Glassy UI" && !WallpaperResources.desktopSource)
            return Translation.tr("Wallpaper unavailable. Choose a valid wallpaper or run the configuration check.")
        if (key === "services:Enable GPS based location" && Config.options.bar.weather.enableGPS && !Weather.gpsActive)
            return Translation.tr("GPS is unavailable. Weather is using the configured city.")
        if (key === "services:Show clipboard preview popups" && Cliphist.availabilityKnown && !Cliphist.available)
            return Translation.tr("Clipboard history is unavailable. Install cliphist, then restart the shell to detect it.")
        return ""
    }

    readonly property var usedWidgets: Array.from(Config.options.bar.layouts.leftLayout)
        .concat(Array.from(Config.options.bar.layouts.middleLayout), Array.from(Config.options.bar.layouts.rightLayout))

    function conditionReason(when, requires) {
        if (requires && !root.usedWidgets.includes(requires))
            return Translation.tr("Add this widget to the bar layout to configure it here.")
        if (["barautohide", "barsuper"].includes(when) && !Config.options.bar.autoHide.enable) return Translation.tr("Enable bar autohide to use this option.")
        if (when === "barsuper" && !Config.options.bar.autoHide.showWhenPressingSuper.enable) return Translation.tr("Enable reveal with Super to use this delay.")
        if (when === "material" && ColorSchemes.current !== "") return Translation.tr("Select the Material color scheme to use this option.")
        if (when === "dockmagnify" && Config.options.dock.position !== "bottom") return Translation.tr("Dock magnification is available only at the bottom edge.")
        if (when === "dockmagnify" && !Config.options.dock.magnify) return Translation.tr("Enable dock magnification to use this option.")
        if (when === "dockhug" && Config.options.dock.style !== "hug") return Translation.tr("Select the Hug dock style to use this option.")
        if (when === "dockfloat" && Config.options.dock.style !== "float") return Translation.tr("Select the Float dock style to use this option.")
        if (when === "football" && !Config.options.sidebar.football.enable) return Translation.tr("Enable Football to use this option.")
        if (when === "hyprbordercolor" && !Config.options.hyprland.general.borderColor.enable) return Translation.tr("Enable custom window border colors to use this option.")
        if (when === "layoutdwindle" && Config.options.hyprland.general.layout !== "dwindle") return Translation.tr("Select the Dwindle tiling layout to use this option.")
        if (when === "layoutmaster" && Config.options.hyprland.general.layout !== "master") return Translation.tr("Select the Master tiling layout to use this option.")
        const styles = { clockdigital: "digital", clockcookie: "cookie", clockdaily: "daily", clockpixel: "pixel" }
        if (styles[when] && Config.options.background.widgets.clock.style !== styles[when]) return Translation.tr("Select the matching clock style to use this option.")
        return ""
    }

    function compatible(entry) {
        return !(["hyprland", "layoutdwindle", "layoutmaster", "hyprbordercolor"].includes(entry.when)
            || entry.key?.startsWith("hyprland:")) || WM.compositor === "hyprland"
    }

    function disabledReason(key, when, requires) {
        if (Config.blockWrites) return Translation.tr("A preset is being applied. Wait for the operation to finish.")
        if (key === "interface:Dock/Magnify" && Config.options.dock.position !== "bottom") return Translation.tr("Dock magnification is available only at the bottom edge.")
        const condition = root.conditionReason(when, requires)
        if (condition) return condition
        if (["interface:Transparency/Background", "interface:Transparency/Content"].includes(key)) {
            if (!Config.options.appearance.transparency.enable) return Translation.tr("Enable Transparency to edit the saved manual values.")
            if (Config.options.appearance.transparency.automatic) return Translation.tr("Turn off Automatic transparency to edit the saved manual values.")
        }
        if (key.startsWith("hyprland:opt:") && HyprlandOptions.values[key.slice(13)] === undefined)
            return Translation.tr("This option has not been confirmed by Hyprland. Open the full compositor settings or run the configuration check.")
        return ""
    }
}
