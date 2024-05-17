import QtQuick 6.0

Rectangle {
    id: keyboard_container
    height: 40
    color: "blue"

    function clickHandler(mouse_event, key) {}

    ListModel {
        id: keyboard_keys_model
    }

    Repeater {
        id: keyboard_view
        model: keyboard_keys_model
        anchors.fill: parent
        delegate: Rectangle {
            property bool active: false
            color: model.color
            anchors.top: keyboard_view.top
            anchors.bottom: model.color == "white" ? keyboard_view.bottom : keyboard_view.verticalCenter
            width: model.color == "white" ? keyboard_view.width / 52 : keyboard_view.width / 80
            border.color: "black"
            border.width: 1
            z: model.color == "white" ? 1 : 2
            Rectangle {
                anchors.bottom: parent.bottom
                anchors.right: parent.right
                anchors.left: parent.left
                visible: backend && backend.active_keys.includes(model.key)
                height: backend && backend.active_keys.includes(model.key) ? backend.get_active_value(model.key, "intensity") * parent.height : 0
                color: "blue"
            }
            MouseArea {
                anchors.fill: parent
                onClicked: (mouse_event) => {
                    var location = 1 - mouse_event.y / height
                    keyboard_container.clickHandler(location, model.key)
                }
            }

            Component.onCompleted: {
                if(index > 0) {
                    if(model.color == "white") {
                        let search_ind = index - 1
                        while (keyboard_keys_model.get(search_ind).color != "white") {
                            search_ind--
                        }
                        const previousItem = keyboard_view.itemAt(search_ind)
                        const previousItemRight = previousItem ? previousItem.right : 0
                        anchors.left = previousItemRight
                    } else {
                        const previousItem = keyboard_view.itemAt(index - 1)
                        const previousItemRight = previousItem ? previousItem.right : 0
                        anchors.horizontalCenter = previousItemRight
                    }
                }
            }
        }
    }

    Component.onCompleted: {
        keyboard_keys_model.clear()
        for (let i = 0; i < backend.keyboard.keys.length; ++i) {
            keyboard_keys_model.append({
                key: backend.keyboard.keys[i],
                freqency: backend.keyboard.frequencies[i],
                color: backend.keyboard.keys[i].includes("#") ? "black" : "white"
            })
        }
    }
}
