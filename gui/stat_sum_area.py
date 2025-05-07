from PyQt6.QtWidgets import QFrame, QHBoxLayout, QTableWidgetItem, QTableWidget, QAbstractItemView, QHeaderView, QWidget, QSizePolicy
from PyQt6.QtCore import Qt, QPoint
from .graph_area import Graph_Area
from logic import get_gc_content, get_base_proportion, find_repeats, get_mutation_types

class StatSummary(QWidget):
    def __init__(self, main_window, sequence_wt, sequence_mt, mutation, seqid_wt, seqid_mt):
        super().__init__()

        self.inner_widget_layout = QHBoxLayout()
        self.inner_widget_layout.setContentsMargins(5, 5, 5, 5)

        #summary = QFrame()
        #summary.setFixedWidth(1000)
        #summary.setMinimumWidth(800)
        #summary.setFrameShape(QFrame.Shape.Box)
        #summary.setFrameShadow(QFrame.Shadow.Sunken)
        summary_layout = QHBoxLayout()
        summary_layout.setContentsMargins(10,10,10,10)
        summary_layout.setSpacing(5)

        table = QTableWidget()
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        #table.setFixedWidth(340)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        table.setRowCount(14)
        table.setColumnCount(3)

        cell_height = table.verticalHeader().defaultSectionSize()
        header_height = table.horizontalHeader().height()

        #table.setFixedHeight(2 + header_height + cell_height * 14)

        # length
        table.setItem(0, 0, QTableWidgetItem("GC Content"))
        table.setItem(0, 1, QTableWidgetItem(get_gc_content(sequence_wt)))
        table.setItem(0, 2, QTableWidgetItem(get_gc_content(sequence_mt)))

        # gc content
        table.setItem(1, 0, QTableWidgetItem("Length"))
        table.setItem(1, 1, QTableWidgetItem(str(len(sequence_wt.replace('-', '')))))
        table.setItem(1, 2, QTableWidgetItem(str(len(sequence_mt.replace('-', '')))))

        # base proportions
        table.setItem(2, 0, QTableWidgetItem("A"))
        table.setItem(2, 1, QTableWidgetItem(get_base_proportion(sequence_wt, 'A')))
        table.setItem(2, 2, QTableWidgetItem(get_base_proportion(sequence_mt, 'A')))
        table.setItem(3, 0, QTableWidgetItem("T"))
        table.setItem(3, 1, QTableWidgetItem(get_base_proportion(sequence_wt, 'T')))
        table.setItem(3, 2, QTableWidgetItem(get_base_proportion(sequence_mt, 'T')))
        table.setItem(4, 0, QTableWidgetItem("G"))
        table.setItem(4, 1, QTableWidgetItem(get_base_proportion(sequence_wt, 'G')))
        table.setItem(4, 2, QTableWidgetItem(get_base_proportion(sequence_mt, 'G')))
        table.setItem(5, 0, QTableWidgetItem("C"))
        table.setItem(5, 1, QTableWidgetItem(get_base_proportion(sequence_wt, 'C')))
        table.setItem(5, 2, QTableWidgetItem(get_base_proportion(sequence_mt, 'C')))

        # repeat content
        table.setItem(6, 0, QTableWidgetItem("Repeat Content"))
        table.setItem(6, 1, QTableWidgetItem(find_repeats(sequence_wt)))
        table.setItem(6, 2, QTableWidgetItem(find_repeats(sequence_mt)))

        # mutation types
        if mutation:
            mutation_types = get_mutation_types(sequence_wt, sequence_mt)
            table.setItem(7, 0, QTableWidgetItem("Deletions"))
            table.setItem(7, 2, QTableWidgetItem(str(mutation_types['deletion'])))
            table.setItem(8, 0, QTableWidgetItem("Substitutions"))
            table.setItem(8, 2, QTableWidgetItem(str(mutation_types['substitution'])))

        # colnames
        table.setHorizontalHeaderLabels(['Summary', 'Reference', 'Mutated Type'])
        table.verticalHeader().setVisible(False)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        table.setAlternatingRowColors(True)

        self.graph = Graph_Area(main_window, sequence_wt, sequence_mt, mutation, seqid_wt, seqid_mt)

        table.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.graph.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        summary_layout.addWidget(table, stretch=2)
        #summary_layout.addStretch(1)
        summary_layout.addWidget(self.graph, stretch=3)
        #summary.setLayout(summary_layout)

        #self.inner_widget_layout.addWidget(summary)
        #self.inner_widget_layout.addStretch(1)
        self.setLayout(summary_layout)