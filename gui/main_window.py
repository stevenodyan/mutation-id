import sys

from PyQt6.QtCore import QSize, Qt, QCoreApplication, QThread, pyqtSignal
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMessageBox, 
                            QFileDialog, QHBoxLayout, QPushButton,
                            QWidget, QFrame, QVBoxLayout, QGroupBox, QTextEdit, QProgressBar, QLabel, QTabWidget, QSplitter, QStatusBar, QTableWidget, QTableWidgetItem, QCheckBox)
from PyQt6.QtGui import QAction, QIcon, QMovie

class AlignmentThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def run(self):
        for i in range(101):
            self.progress.emit(i)
            QThread.msleep(50)
        self.finished.emit()
# from logic import file_loader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # main window and layout
        self.setWindowTitle("Mutation id")
        self.setMinimumSize(1150, 650)
        self.dark_mode = False
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()

        #Status Bar
        self.statusBar().showMessage("Ready")

        #Tab Widget for Sections
        self.tabs = QTabWidget()
        load_tab = QWidget()
        align_tab = QWidget()
        self.tabs.addTab(load_tab, "Load Sequences")
        self.tabs.addTab(align_tab, "Alignment")

        # side panel layout
        side_panel = QFrame()
        side_panel.setFrameShape(QFrame.Shape.StyledPanel)
        side_panel.setFixedWidth(250)
        side_panel_layout = QVBoxLayout()

        #Group Box for Loading Sequences
        load_group = QGroupBox("Load Sequences")
        load_group_layout = QVBoxLayout()

        self.load_wt_button = QPushButton("Load Wild Type FASTA")
        self.load_mutation_button = QPushButton("Load Mutated Sequence FASTA")
        self.load_wt_button.setToolTip("Click to load a Wild Type FASTA file")
        self.load_mutation_button.setToolTip("Click to load a Mutated FASTA file")
        self.load_wt_button.clicked.connect(lambda: self.load_fasta_file("WT"))
        self.load_mutation_button.clicked.connect(lambda: self.load_fasta_file("Mutant"))

        load_group_layout.addWidget(self.load_wt_button)
        load_group_layout.addWidget(self.load_mutation_button)
        load_group.setLayout(load_group_layout)

        side_panel_layout.addWidget(load_group)
        side_panel_layout.addStretch(1)
        
        side_panel.setLayout(side_panel_layout)
        #Collapsible Side Panel
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(side_panel)
        splitter.addWidget(self.tabs)
        splitter.setStretchFactor(1, 5)
        main_layout.addWidget(splitter)

        # central area layout
        central_area = QFrame()
        central_area_layout = QVBoxLayout()

        central_area.setLayout(central_area_layout)
        main_layout.addWidget(central_area, stretch=1)

        # set main layout
        main_layout.addWidget(self.tabs, stretch=1)
        central_widget.setLayout(main_layout)

        #Load Tab Layout
        load_tab_layout = QVBoxLayout()
        self.wt_textbox = QTextEdit()
        self.wt_textbox.setReadOnly(True)
        self.mutant_textbox = QTextEdit()
        self.mutant_textbox.setReadOnly(True)

        load_tab_layout.addWidget(QLabel("Wild Type Sequence:"))
        load_tab_layout.addWidget(self.wt_textbox)
        load_tab_layout.addWidget(QLabel("Mutated Sequence:"))
        load_tab_layout.addWidget(self.mutant_textbox)
        load_tab.setLayout(load_tab_layout)

        #Alignment Tab Layout
        align_tab_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.loading_label = QLabel()
        self.loading_label.hide()
        align_tab_layout.addWidget(QLabel("Alignment Progress:"))
        align_tab_layout.addWidget(self.progress_bar)
        align_tab_layout.addWidget(self.loading_label)
        align_tab.setLayout(align_tab_layout)

        # menu bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        run_menu = menu_bar.addMenu("Run")

        load_wt_action = QAction("Load WT FASTA", self)
        load_wt_action.triggered.connect(lambda: self.load_fasta_file("WT"))

        load_mutation_action = QAction("Load Mutated FASTA", self)
        load_mutation_action.triggered.connect(lambda: self.load_fasta_file("Mutant"))

        alignment_action = QAction("Run Alignment", self)
        alignment_action.triggered.connect(self.run_alignment)
        theme_action = QAction("Toggle Dark Mode", self)
        theme_action.triggered.connect(self.toggle_theme)

        file_menu.addAction(load_wt_action)
        file_menu.addAction(load_mutation_action)
        run_menu.addAction(alignment_action)
        menu_bar.addAction(theme_action)


        #Apply Styles
        self.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 14px;
                border-radius: 8px;
                padding: 8px;
                border: 2px solid transparent;
            }
            QPushButton:hover {
                background-color: #2980b9;
                border: 2px solid #1f618d;
            }
            QTextEdit {
                background-color: #ecf0f1;
                font-size: 14px;
                border-radius: 5px;
                padding: 5px;
            }
            QProgressBar {
                border: 2px solid #2980b9;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                width: 10px;
            }
        """)

    def toggle_theme(self):
        if self.dark_mode:
            self.setStyleSheet("")
            self.dark_mode = False
        else:
            self.setStyleSheet("""
                QWidget { background-color: #2c3e50; color: white;}
                QPushButton { background-color: #34495e; color: white; border-radius: 5px; padding: 5px;}
                QTextEdit { background-color: #95a5a6; color: black;}
            """)
            self.dark_mode = True

    def load_fasta_file(self, sequence_type):
        pathname, _ = QFileDialog.getOpenFileName(self, "Open File", "", "FASTA Files (*.fasta)")
        if not pathname:
            return
        
        
        try:
            with open(pathname, 'r') as file:
                sequence = file.read()

            if not sequence.startswith(">"):
                QMessageBox.warning(self, "Invalid File", "The selected file is not a valid FASTA file.")
                return

            if sequence_type == "WT":
                self.wt_textbox.setText(sequence)
            else:
                self.mutant_textbox.setText(sequence)
            
            self.statusBar().showMessage(f"Loaded {sequence_type} sequence successfully")
                

        except FileNotFoundError:
            QMessageBox.critical(self, "File Error", "The selected file could not be found")
        except IOError as e:
            QMessageBox.critical(self, "File Error", f"An error occured while reading the file {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occured {e}")

    def run_alignment(self):
         self.loading_label.show()
         self.progress_bar.setValue(0)
         self.thread = AlignmentThread()
         self.thread.progress.connect(self.progress_bar.setValue)
         self.thread.finished.connect(self.alignment_done)
         self.thread.start()

    def alignment_done(self):
        self.loading_label.hide()
        QMessageBox.information(self, "Success", "Alignment Completed!")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()