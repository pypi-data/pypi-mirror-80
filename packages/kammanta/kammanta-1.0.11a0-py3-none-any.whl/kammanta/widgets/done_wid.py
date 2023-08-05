import logging
import os
import time
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import kammanta.model
import kammanta.widgets.checklist_cw
import kammanta.widgets.calendar_input_dlg
import kammanta.glob
import kammanta.gtd_info
import kammanta.widgets.ref_file_selection_dlg

TITLE_STR = "Done"


class DoneWidgetInDock(QtWidgets.QWidget):
    clear_clicked_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        vbox_l1 = QtWidgets.QVBoxLayout(self)
        self.setLayout(vbox_l1)
        self.setSizePolicy(
            self.sizePolicy().horizontalPolicy(),
            QtWidgets.QSizePolicy.MinimumExpanding
        )
        # TODO: making the widget non-selectable

        self.main_list_qlw = QtWidgets.QListWidget()
        vbox_l1.addWidget(self.main_list_qlw)
        self.main_list_qlw.setWordWrap(True)
        self.main_list_qlw.setSpacing(2)
        new_font = self.main_list_qlw.font()
        new_font.setPointSize(new_font.pointSize() + 1)
        self.main_list_qlw.setFont(new_font)

        # self.main_list_qlw.addItems(["test 1", "test 2", "test 3"])

        self.update_gui()

    def update_gui(self):
        self.main_list_qlw.clear()
        all_done_strlist = kammanta.model.na_files.get_all_done()
        self.main_list_qlw.addItems(all_done_strlist)



