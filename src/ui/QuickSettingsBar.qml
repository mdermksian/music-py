import QtQuick 6.0
import QtQuick.Layouts
import QtQuick.Controls

Rectangle {
    color: "#EEEEEE"

    RowLayout {
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        spacing: 10

        SettingsSwitch {
            text: "Hold"
            focusPolicy: Qt.NoFocus
            checked: backend.hold
            Layout.fillHeight: true
            onClicked: {
                backend.toggle_hold()
            }
        }

        SettingsSwitch {
            text: "Adjustable Volume"
            focusPolicy: Qt.NoFocus
            checked: backend.adjustable_volume
            Layout.fillHeight: true
            onClicked: {
                backend.toggle_adjustable_volume()
            }
        }
    }
}
