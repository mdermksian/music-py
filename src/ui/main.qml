import QtQuick 6.0
import QtQuick.Controls 6.0
import Plotting 1.0
import "../ui"

ApplicationWindow {
    visible: true
    width: 1800
    height: 800
    title: "PySide6 QML Example"

    color: "#333333"

    FontLoader {
        id: figtree
        source: "./fonts/Figtree-VariableFont_wght.ttf"
    }

    Keyboard {
        id: keyboard
        anchors {
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }
        height: width / 10
    }

    QuickSettingsBar {
        id: quick_settings_bar
        height: 30
        anchors {
            left: parent.left
            right: parent.right
            bottom: keyboard.top
        }
    }

    SineWavePlot {
        id: plot
        frequencies: backend.active_frequencies
        anchors {
            bottom: quick_settings_bar.top
            top: parent.top
            left: parent.left
            right: parent.right
        }
    }
}