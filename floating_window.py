import sys
import subprocess
import threading
from PyQt5.QtCore import Qt, QUrl, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class StreamlitRunner(threading.Thread):
    def run(self):
        subprocess.run(["streamlit", "run", "streamlit_app.py"])

class FloatingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.run_streamlit_app()
        self.oldPos = self.pos()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        self.load_streamlit_app()

    def run_streamlit_app(self):
        self.streamlit_thread = StreamlitRunner()
        self.streamlit_thread.start()

    def load_streamlit_app(self):
        # Load the local Streamlit app
        self.browser.setUrl(QUrl("http://localhost:8501"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
            event.accept()

    def closeEvent(self, event):
     
        self.streamlit_thread.join()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FloatingWindow()
    window.show()
    sys.exit(app.exec_())
