import QtQuick 6.0
import QtQuick.Controls

Switch {
    id: main_switch

    indicator: Rectangle {
        width: 48
        height: main_switch.height - 8
        x: main_switch.leftPadding
        y: main_switch.height / 2 - height / 2
        radius: main_switch.height / 2
        color: main_switch.checked ? "#222222" : "#ffffff"
        border.color: main_switch.checked ? "#222222" : "#cccccc"

        Rectangle {
            x: main_switch.checked ? parent.width - width : 0
            width: parent.height
            height: parent.height
            radius: height / 2
            color: main_switch.down ? "#cccccc" : "#ffffff"
            border.color: main_switch.checked ? (main_switch.down ? "#222222" : "#333333") : "#999999"
        }
    }

    contentItem: Text {
        text: main_switch.text
        font: main_switch.font
        opacity: enabled ? 1.0 : 0.3
        color: main_switch.down ? "#222222" : "#333333"
        verticalAlignment: Text.AlignVCenter
        leftPadding: main_switch.indicator.width + main_switch.spacing
    }
}
