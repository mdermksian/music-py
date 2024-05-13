import sys
import os
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from backend import Backend
from plotter import SineWavePlot

if __name__ == "__main__":
    os.environ["QSG_INFO"] = "1"

    qmlRegisterType(SineWavePlot, "Plotting", 1, 0, "SineWavePlot")
    app = QGuiApplication(sys.argv)

    backend = Backend()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("backend", backend)
    qml_file = os.path.join(os.path.dirname(__file__), "ui", "main.qml")
    engine.load(QUrl.fromLocalFile(qml_file))

    if not engine.rootObjects():
        sys.exit(-1)

    app.aboutToQuit.connect(backend.cleanup)

    sys.exit(app.exec())
