import logging
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import kammanta.model
import kammanta.glob
import kammanta.widgets.path_sel_dlg
import kammanta.do_timer


class FocusDlg(QtWidgets.QDialog):
    def __init__(self, i_focus_item):
        # -giving type hint for focus_item here?
        # Please note: LxQt shows the minimize button even though we have a dialog
        # Documentation: https://doc.qt.io/qt-5/qt.html#WindowType-enum
        # self.setWindowFlags(QtCore.Qt.Popup)
        # self.setWindowFlag(QtCore.Qt.Popup)

        super().__init__()
        # , *args, **kwargs

        logging.info("init for FocusDlg")

        self.focus_item_ref = i_focus_item

        self.setMinimumWidth(500)
        self.setMinimumHeight(300)

        # self.setSizeGripEnabled(True)
        self.setWindowTitle("Focus")


        vbox_l1 = QtWidgets.QVBoxLayout(self)

        self.item_name_qll = QtWidgets.QLabel()
        self.item_name_qll.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )
        self.item_name_qll.setWordWrap(True)
        self.item_name_qll.setText(self.focus_item_ref.get_core_name())
        self.item_name_qll.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        name_font = QtGui.QFont()
        name_font.setPointSize(20)
        self.item_name_qll.setFont(name_font)
        vbox_l1.addWidget(self.item_name_qll, stretch=1)
        # alignment=QtCore.Qt.AlignCenter,

        # Support

        self.open_support_qpb = QtWidgets.QPushButton("Open support")
        vbox_l1.addWidget(self.open_support_qpb)
        self.open_support_qpb.clicked.connect(self.on_open_support_clicked)
        open_support_font = QtGui.QFont()
        open_support_font.setPointSize(18)
        self.open_support_qpb.setFont(open_support_font)

        # Timer
        # Idea: setting another icon in the systray during focus?
        # Also, instead of opening the application on left click (activated) we can open the dialog

        self.timer = kammanta.do_timer.DoTimer()
        self.timer.start()
        self.timer.update_signal.connect(self.update_gui)

        self.timer_qll = QtWidgets.QLabel()
        # self.timer.get_formatted_time()
        vbox_l1.addWidget(self.timer_qll)
        timer_font = QtGui.QFont()
        timer_font.setPointSize(64)
        self.timer_qll.setFont(timer_font)

        hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(hbox_l2)

        self.done_qpb = QtWidgets.QPushButton("Done")
        hbox_l2.addWidget(self.done_qpb)
        self.done_qpb.clicked.connect(self.on_done_clicked)
        done_font = QtGui.QFont()
        done_font.setPointSize(24)
        done_font.setBold(True)
        self.done_qpb.setFont(done_font)

        self.close_qpb = QtWidgets.QPushButton("Close")
        hbox_l2.addWidget(self.close_qpb)
        self.close_qpb.clicked.connect(self.on_close_clicked)
        close_font = QtGui.QFont()
        close_font.setPointSize(24)
        self.close_qpb.setFont(close_font)

        self.started_qpb = QtWidgets.QPushButton("Set as started")
        hbox_l2.addWidget(self.started_qpb)
        self.started_qpb.clicked.connect(self.on_started_clicked)
        started_font = QtGui.QFont()
        started_font.setPointSize(24)
        self.started_qpb.setFont(started_font)


        self.update_gui()

    def on_done_clicked(self):
        self.focus_item_ref.set_completed(True)
        self.close()

    def on_close_clicked(self):
        self.close()

    def on_started_clicked(self):
        old_name_str = self.focus_item_ref.get_core_name()
        new_name_str = kammanta.glob.add_prefix(old_name_str, kammanta.glob.STARTED_PREFIX_STR)
        self.focus_item_ref.set_core_name(new_name_str)
        self.close()

    def on_open_support_clicked(self):
        sp_str = self.focus_item_ref.get_support_path()
        sp_str = sp_str.strip()
        # -removing space at beginning
        if sp_str:
            try:
                kammanta.glob.launch_string(sp_str)
            except Exception:
                QtWidgets.QMessageBox.warning(self, "title", "cannot open, if file it may not exist")

    def update_gui(self):
        sp_str = self.focus_item_ref.get_support_path()
        if sp_str:
            self.open_support_qpb.setEnabled(True)
        else:
            self.open_support_qpb.setEnabled(False)

        elapsed_time_str = self.timer.get_formatted_time()
        self.timer_qll.setText(elapsed_time_str)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.timer.stop()
        super().closeEvent(a0)

    def restore_and_activate(self):
        self.show()
        self.raise_()
        if self.isMaximized():
            self.showMaximized()
        else:
            self.showNormal()
        self.activateWindow()
        self.setFocus()


"""
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)

    # Existing file
    FocusDlg.open_dlg(
        "Title test", "# Content test\n\nParagraph text\n\n* List item 1\n* another line",
    )

    sys.exit()
"""

