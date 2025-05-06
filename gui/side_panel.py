from PyQt6.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal, QObject
import os

class SidePanel(QFrame):
    dark_mode_toggled = pyqtSignal(bool)  # Signal to notify about dark mode toggle

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dark_mode_enabled = False

        self.setFrameShape(QFrame.Shape.Box)
        self.setFixedWidth(250)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.side_panel_layout = QVBoxLayout()

        self.wt_widget = QWidget()
        self.mt_widget = QWidget()
        self.wt_widget_layout = QHBoxLayout()
        self.mt_widget_layout = QHBoxLayout()
        self.wt_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.mt_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.side_panel_layout.addWidget(self.wt_widget)
        self.side_panel_layout.addWidget(self.mt_widget)

        self.toggle_button = QPushButton("🌓 Toggle Dark Mode")
        self.toggle_button.clicked.connect(self.handle_toggle)

        self.side_panel_layout.addWidget(self.toggle_button)
        self.setLayout(self.side_panel_layout)

    
    def handle_toggle(self):
            self.dark_mode_enabled = not self.dark_mode_enabled
            self.dark_mode_toggled.emit(self.dark_mode_enabled)

