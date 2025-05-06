# need a state variable that changes every time
# you add a sequence using the file loader
# it needs to go from 0 to 1 to 2 and then decrease
# as such when user deletes a sequence
import os
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QHBoxLayout
from .welcome_view import WelcomeView
from .side_panel import SidePanel

DARK_THEME = """
QWidget {
    background-color: #2E2E2E;
    color: #F0F0F0;
}

QPushButton {
    background-color: #444;
    color: white;
    border: 1px solid #666;
    border-radius: 4px;
    padding: 5px;
}
QPushButton:hover {
    background-color: #555;
}

QTableWidget {
    background-color: #3B3B3B;
    alternate-background-color: #2E2E2E;
    gridline-color: #666;
    color: white;
}

QHeaderView::section {
    background-color: #444;
    color: white;
    border: 1px solid #666;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        


        # main window and layout
        self.setWindowTitle("mutation id")
        self.setMinimumSize(1312, 650)
        #Dark Mode
        #container = QWidget()
        #layout = QHBoxLayout(container)
        # stacked widget for switching between views
        self.main_widget = QStackedWidget()
        self.setCentralWidget(self.main_widget)

        # Set up side panel (Note:connected for dark mode toggle)
        #self.side_panel = SidePanel()
        #self.side_panel.dark_mode_toggled.connect(self.toggle_dark_mode)

        # view on entry of program
        welcome_view = WelcomeView(self)

        # add view to stacked widget
        self.main_widget.addWidget(welcome_view)

        # Layout: Add both side panel and main widget to a container
        
        #layout.addWidget(self.side_panel)
        #layout.addWidget(self.main_widget)
        #self.setCentralWidget(container)

            
        #def toggle_dark_mode(self, enabled):
            #if enabled:
                #self.setStyleSheet(DARK_THEME)
            #else:
                #self.setStyleSheet("")



       


        # menu bar
        # menu_bar = self.menuBar()
        # file_menu = menu_bar.addMenu("File")
        # run_menu = menu_bar.addMenu("Run")
        # load_wt_action = QAction("Load WT FASTA", self)
        # load_wt_action.triggered.connect(lambda: init_sequence_view(self))
        # load_mutation_action = QAction("Load Mutated FASTA", self)
        # load_mutation_action.triggered.connect(lambda: init_sequence_view(self))
        # #alignment_action = QAction("Run Alignment", self)
        # # alignment_action.triggered.connect(self.run_alignment)
        # file_menu.addAction(load_wt_action)
        # file_menu.addAction(load_mutation_action)
        # # run_menu.addAction(alignment_action)