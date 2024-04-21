import QtQuick 6.0
import QtQuick.Layouts
import QtQuick.Controls

Rectangle {
    color: "#EEEEEE"


    RowLayout {
        anchors.fill: parent
        spacing: 10

        SettingsSwitch {
            text: "Hold"
            checked: backend.settings.hold
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignVCenter
            onClicked: {
                backend.settings.toggle_hold()
            }
        }
    }
}