import QtQuick
import QtQuick.Layouts
import qs
import qs.services
import qs.modules.common
import qs.modules.common.widgets

DashboardCard {
    id: root

    property string title: ""
    property string icon: "view_week"
    property var tileShape: MaterialShape.Shape.Gem

    readonly property var barConfig: Config.options.bar
    readonly property bool vertical: barConfig.vertical
    readonly property var leftList: Array.from(barConfig.layouts.leftLayout)
    readonly property var middleList: Array.from(barConfig.layouts.middleLayout)
    readonly property var rightList: Array.from(barConfig.layouts.rightLayout)
    readonly property var usedIds: leftList.concat(middleList, rightList)

    readonly property var lanes: [
        { id: "left", title: vertical ? Translation.tr("Top") : Translation.tr("Left"), icon: vertical ? "align_vertical_top" : "align_horizontal_left", list: leftList },
        { id: "middle", title: Translation.tr("Center"), icon: vertical ? "align_vertical_center" : "align_horizontal_center", list: middleList },
        { id: "right", title: vertical ? Translation.tr("Bottom") : Translation.tr("Right"), icon: vertical ? "align_vertical_bottom" : "align_horizontal_right", list: rightList }
    ]

    readonly property var trayIds: widgets.all.filter(w => !usedIds.includes(w.id) || widgets.multipleAllowed.includes(w.id)).map(w => w.id)
    property var selection: null
    readonly property var selectedInfo: selection ? widgets.byId(selection.id) : null
    readonly property var selectedEntries: {
        if (!selection) return [];
        if (selection.id === "clockWidget") return settingsCatalog.sections.reduce((all, section) => all.concat(section.cards.filter(card => ["general:Format", "general:Show date"].includes(card.key))), []);
        return settingsCatalog.sections.filter(section => section.requires === selection.id).reduce((all, section) => all.concat(section.cards.map(card => Object.assign({ requires: section.requires, when: section.when ?? "" }, card))), []);
    }
    DashboardSettingsCatalog { id: settingsCatalog }

    function selectItem(id, lane, index) { selection = { id: id, lane: lane, index: index }; }
    function actOnSelection(target, offset) {
        const item = selection;
        if (!item) return;
        const position = target === "tray" ? 0 : target === item.lane ? item.index + offset : BarLayout.lists[target].length;
        if (BarLayout.transfer(item.lane, item.index, target, position, item.id)) {
            selection = target === "tray" ? null : { id: item.id, lane: target, index: position };
        }
    }
    function openSelectedSettings() {
        const section = settingsCatalog.sections.find(s => s.requires === selection?.id);
        GlobalStates.openSettingsAt("bar", "", section?.title ?? Translation.tr("Bar layout"));
    }

    property var drag: null
    property string hoverLane: ""
    property int hoverIndex: 0
    property real dragWidth: 90
    property real pointerX: 0
    property real pointerY: 0

    tint: Appearance.colors.colLayer1

    DashboardBarWidgets {
        id: widgets
    }

    readonly property var catalog: widgets

    ListModel { id: leftModel }
    ListModel { id: middleModel }
    ListModel { id: rightModel }

    function modelFor(laneId) {
        return laneId === "left" ? leftModel : laneId === "middle" ? middleModel : rightModel;
    }

    function baseItems(laneId) {
        const list = laneId === "left" ? leftList : laneId === "middle" ? middleList : rightList;
        const seen = {};
        return list.map((wid, i) => {
            seen[wid] = (seen[wid] ?? 0) + 1;
            return { key: wid + "#" + seen[wid], wid: wid, gap: false, realIndex: i };
        });
    }

    function desiredItems(laneId) {
        const items = baseItems(laneId);
        if (drag !== null && hoverLane === laneId) {
            let insertAt = items.length;
            let count = 0;
            for (let i = 0; i < items.length; i++) {
                if (drag.from === laneId && drag.fromIndex === items[i].realIndex) continue;
                if (count === hoverIndex) {
                    insertAt = i;
                    break;
                }
                count++;
            }
            items.splice(insertAt, 0, { key: "__gap__", wid: "", gap: true, realIndex: -1 });
        }
        return items;
    }

    function syncModel(model, target) {
        const wanted = new Set(target.map(t => t.key));
        for (let i = model.count - 1; i >= 0; i--) {
            if (!wanted.has(model.get(i).key)) model.remove(i);
        }
        for (let t = 0; t < target.length; t++) {
            const item = target[t];
            if (t < model.count && model.get(t).key === item.key) {
                const current = model.get(t);
                if (current.realIndex !== item.realIndex || current.gap !== item.gap) model.set(t, item);
                continue;
            }
            let found = -1;
            for (let j = t + 1; j < model.count; j++) {
                if (model.get(j).key === item.key) {
                    found = j;
                    break;
                }
            }
            if (found >= 0) {
                model.move(found, t, 1);
                model.set(t, item);
            } else {
                model.insert(t, item);
            }
        }
    }

    property var lastSynced: ({ left: "", middle: "", right: "" })

    function refreshLanes() {
        ["left", "middle", "right"].forEach(laneId => {
            const desired = desiredItems(laneId);
            const signature = JSON.stringify(desired);
            if (lastSynced[laneId] === signature) return;
            lastSynced[laneId] = signature;
            syncModel(modelFor(laneId), desired);
        });
    }

    onLeftListChanged: refreshLanes()
    onMiddleListChanged: refreshLanes()
    onRightListChanged: refreshLanes()
    onHoverLaneChanged: refreshLanes()
    onHoverIndexChanged: refreshLanes()
    onDragChanged: refreshLanes()
    Component.onCompleted: refreshLanes()

    function laneItem(laneId) {
        for (let i = 0; i < laneRepeater.count; i++) {
            const lane = laneRepeater.itemAt(i);
            if (lane && lane.laneId === laneId) return lane;
        }
        return null;
    }

    function containsPoint(item, x, y) {
        if (!item) return false;
        const p = root.mapFromItem(item, 0, 0);
        return x >= p.x && x <= p.x + item.width && y >= p.y && y <= p.y + item.height;
    }

    function insertIndex(lane, x, y) {
        let before = 0;
        for (let i = 0; i < lane.chipRepeater.count; i++) {
            const chip = lane.chipRepeater.itemAt(i);
            if (!chip || chip.isGap || chip.beingDragged) continue;
            const c = root.mapFromItem(chip, chip.width / 2, chip.height / 2);
            const half = chip.height / 2;
            if (c.y < y - half || (Math.abs(c.y - y) <= half && c.x < x)) before++;
        }
        return before;
    }

    function updateHover() {
        let found = "";
        for (let i = 0; i < laneRepeater.count; i++) {
            const lane = laneRepeater.itemAt(i);
            if (containsPoint(lane, pointerX, pointerY)) {
                found = lane.laneId;
                hoverIndex = insertIndex(lane, pointerX, pointerY);
                break;
            }
        }
        if (found === "" && containsPoint(trayArea, pointerX, pointerY)) found = "tray";
        hoverLane = found;
    }

    function beginDrag(widgetId, from, fromIndex, point, width) {
        dragWidth = width;
        drag = { id: widgetId, from: from, fromIndex: fromIndex };
        pointerX = point.x;
        pointerY = point.y;
        updateHover();
    }

    function moveDrag(point) {
        pointerX = point.x;
        pointerY = point.y;
        updateHover();
    }

    function finishDrag() {
        const info = drag;
        const target = hoverLane;
        const index = hoverIndex;
        drag = null;
        hoverLane = "";
        if (!info || target === "") return;

        if (BarLayout.transfer(info.from, info.fromIndex, target, index, info.id))
            selection = target === "tray" ? null : { id: info.id, lane: target, index: index };
    }

    Connections {
        target: BarLayout
        function onSignatureChanged() {
            Qt.callLater(() => {
                const item = root.selection;
                if (item && item.lane !== "tray" && BarLayout.lists[item.lane]?.[item.index] !== item.id)
                    root.selection = null;
            });
        }
    }

    property bool confirmClear: false

    Timer {
        id: confirmClearTimer
        interval: 2500
        onTriggered: root.confirmClear = false
    }

    function clearAll() {
        confirmClear = false;
        if (BarLayout.clear()) selection = null;
    }

    function removeWidget(laneId, index) {
        const id = BarLayout.lists[laneId]?.[index];
        if (id !== undefined && BarLayout.transfer(laneId, index, "tray", 0, id)) selection = null;
    }

    component EditorButton: RippleButton {
        objectName: "barAction"
        Accessible.name: buttonText
        activeFocusOnTab: true
        horizontalPadding: 10
        verticalPadding: 6
    }

    component Chip: Rectangle {
        id: chip
        property var card: null
        property string widgetId: ""
        property string lane: ""
        property int slot: 0
        property bool isGap: false
        readonly property var info: card.catalog.byId(widgetId)
        readonly property bool beingDragged: card.drag !== null && card.drag.id === widgetId && card.drag.from === lane && card.drag.fromIndex === slot

        implicitHeight: 34
        implicitWidth: isGap ? card.dragWidth : beingDragged ? 0 : Math.min(chipLabel.implicitWidth + 46, Math.max(90, card.width / 3 - 42))
        radius: height / 2
        color: isGap ? "transparent" : lane === "tray" ? Qt.rgba(1, 1, 1, 0.1) : Appearance.colors.colSecondaryContainer
        border.color: Appearance.colors.colPrimary
        opacity: beingDragged ? 0 : isGap ? 0.7 : 1
        clip: true
        activeFocusOnTab: !isGap && lane !== "ghost"
        Accessible.role: Accessible.Button
        Accessible.name: info.name
        Accessible.description: Translation.tr("Select to add, move or configure this item.")
        border.width: activeFocus || (card.selection?.id === widgetId && card.selection?.lane === lane && card.selection?.index === slot) ? 2 : isGap ? 2 : 0
        Keys.onReturnPressed: card.selectItem(widgetId, lane, slot)
        Keys.onEnterPressed: card.selectItem(widgetId, lane, slot)
        Keys.onSpacePressed: card.selectItem(widgetId, lane, slot)

        Behavior on implicitWidth {
            NumberAnimation { duration: 160; easing.type: Easing.OutCubic }
        }

        RowLayout {
            id: chipRow
            anchors.centerIn: parent
            width: parent.width - 24
            spacing: 6
            visible: !chip.isGap

            MaterialSymbol {
                text: chip.info.icon
                iconSize: 16
                color: Appearance.colors.colOnSecondaryContainer
            }
            StyledText {
                id: chipLabel
                Layout.fillWidth: true
                elide: Text.ElideRight
                text: chip.info.name
                font.pixelSize: Appearance.font.pixelSize.small
                color: Appearance.colors.colOnSecondaryContainer
            }
        }

        MouseArea {
            anchors.fill: parent
            enabled: !chip.isGap
            acceptedButtons: Qt.LeftButton | Qt.RightButton
            cursorShape: pressed ? Qt.ClosedHandCursor : Qt.OpenHandCursor
            preventStealing: true
            property real startX: 0
            property real startY: 0
            onPressed: mouse => {
                if (mouse.button === Qt.RightButton) {
                    if (chip.lane !== "tray") card.removeWidget(chip.lane, chip.slot);
                    return;
                }
                chip.forceActiveFocus();
                startX = mouse.x; startY = mouse.y;
            }
            onPositionChanged: mouse => {
                if (!pressed) return;
                if (!card.drag && Math.hypot(mouse.x - startX, mouse.y - startY) > 8)
                    card.beginDrag(chip.widgetId, chip.lane, chip.slot, chip.mapToItem(card, mouse.x, mouse.y), chip.width);
                else if (card.drag) card.moveDrag(chip.mapToItem(card, mouse.x, mouse.y));
            }
            onReleased: mouse => {
                if (mouse.button !== Qt.LeftButton) return;
                if (card.drag) card.finishDrag();
                else card.selectItem(chip.widgetId, chip.lane, chip.slot);
            }
            onCanceled: { card.drag = null; card.hoverLane = ""; }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12

        RowLayout {
            Layout.fillWidth: true
            spacing: 12

            MaterialShapeWrappedMaterialSymbol {
                shape: root.tileShape
                text: root.icon
                iconSize: 24
                fill: 1
                padding: 10
                color: Appearance.colors.colPrimary
                colSymbol: Appearance.colors.colOnPrimary
            }

            ColumnLayout {
                Layout.fillWidth: true
                spacing: 0

                StyledText {
                    Layout.fillWidth: true
                    elide: Text.ElideRight
                    text: root.title
                    font.pixelSize: Appearance.font.pixelSize.larger
                    font.weight: Font.DemiBold
                    color: Appearance.colors.colOnLayer1
                }
                StyledText {
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                    text: Translation.tr("Select an item to add, move or configure it. Dragging is optional.")
                    font.pixelSize: Appearance.font.pixelSize.smaller
                    color: Appearance.colors.colSubtext
                }
            }

            Item { Layout.fillWidth: true }

            RippleButton {
                Layout.alignment: Qt.AlignTop
                implicitHeight: 36
                horizontalPadding: 14
                buttonRadius: 18
                enabled: root.usedIds.length > 0
                colBackground: root.confirmClear ? Appearance.colors.colPrimary : Appearance.colors.colSecondaryContainer
                colBackgroundHover: root.confirmClear ? Appearance.colors.colPrimaryHover : Appearance.colors.colSecondaryContainerHover
                colRipple: root.confirmClear ? Appearance.colors.colPrimaryActive : Appearance.colors.colSecondaryContainerActive
                onClicked: Qt.callLater(() => {
                    if (root.confirmClear) root.clearAll();
                    else {
                        root.confirmClear = true;
                        confirmClearTimer.restart();
                    }
                })
                contentItem: RowLayout {
                    spacing: 6
                    MaterialSymbol {
                        text: root.confirmClear ? "check" : "layers_clear"
                        iconSize: 18
                        color: root.confirmClear ? Appearance.colors.colOnPrimary : Appearance.colors.colOnSecondaryContainer
                    }
                    StyledText {
                        text: root.confirmClear ? Translation.tr("Tap again to clear") : Translation.tr("Clear all")
                        font.pixelSize: Appearance.font.pixelSize.small
                        color: root.confirmClear ? Appearance.colors.colOnPrimary : Appearance.colors.colOnSecondaryContainer
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 10

            Repeater {
                id: laneRepeater
                model: root.lanes

                delegate: Rectangle {
                    id: laneBox
                    required property var modelData

                    readonly property string laneId: modelData.id
                    property alias chipRepeater: chips
                    readonly property bool hovered: root.drag !== null && root.hoverLane === laneBox.laneId

                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredWidth: 1
                    radius: 20
                    color: hovered ? Qt.rgba(1, 1, 1, 0.12) : Qt.rgba(1, 1, 1, 0.06)
                    border.width: hovered ? 2 : 0
                    border.color: Appearance.colors.colPrimary

                    Behavior on color {
                        ColorAnimation { duration: 150 }
                    }

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 12
                        spacing: 8

                        RowLayout {
                            spacing: 6

                            MaterialSymbol {
                                text: laneBox.modelData.icon
                                iconSize: 16
                                color: Appearance.colors.colSubtext
                            }
                            StyledText {
                                text: laneBox.modelData.title.toUpperCase()
                                font.pixelSize: Appearance.font.pixelSize.smaller
                                font.weight: Font.Bold
                                font.letterSpacing: 1.2
                                color: Appearance.colors.colSubtext
                            }
                        }

                        Flickable {
                            id: laneItemsFlick
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            clip: true
                            contentWidth: width
                            contentHeight: flow.implicitHeight
                            boundsBehavior: Flickable.StopAtBounds

                            TouchpadScrollArea { flickable: laneItemsFlick }

                            Flow {
                                id: flow
                                width: parent.width
                                spacing: 6

                                move: Transition {
                                    NumberAnimation { properties: "x,y"; duration: 200; easing.type: Easing.OutBack; easing.overshoot: 1.2 }
                                }

                                Repeater {
                                    id: chips
                                    model: root.modelFor(laneBox.laneId)

                                    delegate: Chip {
                                        required property string wid
                                        required property bool gap
                                        required property int realIndex

                                        card: root
                                        widgetId: wid
                                        isGap: gap
                                        lane: laneBox.laneId
                                        slot: realIndex
                                    }
                                }
                            }
                        }
                    }

                    StyledText {
                        anchors.centerIn: parent
                        visible: laneBox.modelData.list.length === 0 && !(root.drag !== null && root.hoverLane === laneBox.laneId)
                        text: Translation.tr("Drop here")
                        font.pixelSize: Appearance.font.pixelSize.small
                        color: Appearance.colors.colSubtext
                        opacity: 0.6
                    }
                }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 6
            StyledText {
                Layout.fillWidth: true
                text: root.selection ? root.selectedInfo?.name ?? "" : Translation.tr("Select an item above or in the catalog below.")
                font.weight: Font.DemiBold
                wrapMode: Text.WordWrap
            }
            Flow {
                Layout.fillWidth: true
                spacing: 4
                visible: root.selection !== null
                Repeater {
                    model: root.lanes
                    delegate: Column {
                        required property var modelData
                        readonly property string reason: root.selection ? BarLayout.reason(root.selection.id, modelData.id, root.selection.lane === "tray") : ""
                        EditorButton {
                            buttonText: (root.selection?.lane === "tray" ? Translation.tr("Add to") : Translation.tr("Move to")) + " " + modelData.title
                            enabled: parent.reason === "" && root.selection?.lane !== modelData.id && !Config.blockWrites
                            onClicked: root.actOnSelection(parent.modelData.id, 0)
                            StyledToolTip { text: parent.parent.reason; extraVisibleCondition: parent.hovered || parent.activeFocus; maximumContentWidth: 320 }
                        }
                    }
                }
                EditorButton { buttonText: Translation.tr("Move earlier"); enabled: root.selection?.lane !== "tray" && (root.selection?.index ?? 0) > 0 && !Config.blockWrites; onClicked: root.actOnSelection(root.selection.lane, -1) }
                EditorButton { buttonText: Translation.tr("Move later"); enabled: root.selection?.lane !== "tray" && (root.selection?.index ?? 0) < (BarLayout.lists[root.selection?.lane]?.length ?? 0) - 1 && !Config.blockWrites; onClicked: root.actOnSelection(root.selection.lane, 1) }
                EditorButton { buttonText: Translation.tr("Remove from bar"); enabled: root.selection !== null && root.selection.lane !== "tray" && !Config.blockWrites; onClicked: root.actOnSelection("tray", 0) }
                EditorButton { buttonText: Translation.tr("Open all options"); enabled: root.selection?.lane !== "tray"; onClicked: root.openSelectedSettings() }
            }
            StyledText {
                Layout.fillWidth: true
                visible: root.selection !== null
                text: root.selection ? widgets.description(root.selection.id) : ""
                textFormat: Text.PlainText
                wrapMode: Text.WordWrap
                color: Appearance.colors.colSubtext
                font.pixelSize: Appearance.font.pixelSize.smaller
            }
            StyledText {
                Layout.fillWidth: true
                visible: root.selection?.lane === "tray" && text !== ""
                text: root.selection ? root.lanes.map(lane => BarLayout.reason(root.selection.id, lane.id, true)).filter((value, index, all) => value && all.indexOf(value) === index).join("\n") : ""
                textFormat: Text.PlainText
                wrapMode: Text.WordWrap
                color: Appearance.colors.colSubtext
                font.pixelSize: Appearance.font.pixelSize.smaller
            }
            StyledText {
                Layout.fillWidth: true
                text: BarLayout.message
                visible: text !== ""
                wrapMode: Text.WordWrap
                textFormat: Text.PlainText
                font.pixelSize: Appearance.font.pixelSize.smaller
                color: Appearance.colors.colSubtext
            }
            EditorButton { buttonText: Translation.tr("Undo layout change"); enabled: BarLayout.canUndo; onClicked: { if (BarLayout.undo()) root.selection = null; } }
            StyledFlickable {
                Layout.fillWidth: true
                Layout.preferredHeight: root.selectedEntries.length && root.selection?.lane !== "tray" ? 180 : 0
                visible: Layout.preferredHeight > 0
                contentHeight: inlineControls.implicitHeight
                clip: true
                SettingsInlineControls {
                    id: inlineControls
                    width: parent.width
                    entries: root.selectedEntries
                    catalog: settingsCatalog
                    onOpenFullSettings: root.openSelectedSettings()
                }
            }
        }

        Rectangle {
            id: trayArea
            Layout.fillWidth: true
            Layout.preferredHeight: Math.min(trayFlow.implicitHeight + 48, 190)
            radius: 20
            color: root.drag !== null && root.hoverLane === "tray" ? Qt.rgba(1, 1, 1, 0.12) : Qt.rgba(1, 1, 1, 0.04)
            border.width: root.drag !== null && root.hoverLane === "tray" ? 2 : 1
            border.color: root.drag !== null && root.hoverLane === "tray" ? Appearance.colors.colError : Appearance.colors.colOutlineVariant

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 8

                StyledText {
                    text: Translation.tr("AVAILABLE")
                    font.pixelSize: Appearance.font.pixelSize.smaller
                    font.weight: Font.Bold
                    font.letterSpacing: 1.2
                    color: Appearance.colors.colSubtext
                }

                Flickable {
                    id: trayItemsFlick
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    contentWidth: width
                    contentHeight: trayFlow.implicitHeight
                    boundsBehavior: Flickable.StopAtBounds

                    TouchpadScrollArea { flickable: trayItemsFlick }

                    Flow {
                        id: trayFlow
                        width: parent.width
                        spacing: 6

                        Repeater {
                            model: root.trayIds

                            delegate: Chip {
                                required property string modelData
                                required property int index

                                card: root
                                widgetId: modelData
                                lane: "tray"
                                slot: index
                            }
                        }
                    }
                }
            }
        }
    }

    Chip {
        id: ghost
        card: root
        visible: root.drag !== null
        widgetId: root.drag ? root.drag.id : ""
        lane: "ghost"
        z: 100
        x: root.pointerX - width / 2
        y: root.pointerY - height / 2
        opacity: 0.95
        scale: 1.06
        enabled: false
        border.width: 2
        border.color: Appearance.colors.colPrimary
    }
}
