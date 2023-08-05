import logging
import datetime
import functools
import os
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
#### from PyQt5 import QtWebEngineWidgets
# example: https://github.com/smoqadam/PyFladesk/blob/master/pyfladesk/__init__.py
import kammanta.model
import kammanta.glob
import kammanta.widgets.calendar_input_dlg

NOTE_BTN_ID_INT = 1
FILE_BTN_ID_INT = 2


class FileListCw(QtWidgets.QWidget):
    row_selected_signal = QtCore.pyqtSignal(str)  # -id (as string)

    def __init__(self, i_collection_ptr, i_mini_layout: bool):
        super().__init__()
        self.move_context_menu = None
        self.collection_ptr = i_collection_ptr
        self.mini_layout_bool = i_mini_layout

        self.text_widget_list = []
        # -keeping the widgets in memory

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        if not self.mini_layout_bool:
            title_str = self.collection_ptr.get_main_title()
            self.title_qll = QtWidgets.QPushButton(title_str)
            vbox_l2.addWidget(self.title_qll, alignment=QtCore.Qt.AlignLeft)
            self.title_qll.setFlat(True)
            new_font = self.title_qll.font()
            new_font.setPointSize(13)
            self.title_qll.setFont(new_font)
            self.title_qll.clicked.connect(self.on_title_clicked)

        # List of notes and files
        self.notes_qlw = QtWidgets.QListWidget()
        vbox_l2.addWidget(self.notes_qlw)
        self.notes_qlw.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.notes_qlw.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.update_gui()

    def on_title_clicked(self):
        path_str = self.collection_ptr.get_path()
        kammanta.glob.launch_string(path_str)

    # overridden
    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.update_gui()

    def add_dfs_to_fsw(self):
        """
        Adding dirs and files to filesystemwatcher
        """
        all_fds_list = self.collection_ptr.get_all_items()
        fsw = kammanta.glob.FswSingleton.get()
        for fd_obj in all_fds_list:
            fd_path_str = fd_obj.get_path()
            fsw.addPath(fd_path_str)

    def update_gui(self):
        self.notes_qlw.clear()
        self.add_dfs_to_fsw()
        all_fds_list = self.collection_ptr.get_all_items(i_sort_by_name=False)
        # -TODO: Maybe storing the sort type in the collection itself?
        #  One downside with this is that we then cannot change the ordering dynamically
        # -this is done because the wrap doesn't work for smaller sizes. It may be because the size hint
        #  that we get from the qlabel (or the QWidget holding the cell contents) has a minimum width that
        #  it gives us (a similar thing has happened before)
        for fd_obj in all_fds_list:
            text_qll = QtWidgets.QLabel()
            text_qll.setWordWrap(True)
            # -bug: this label doesn't wrap if the text area becomes less than 230-300 px.
            # Unknown why
            # -bug: if the text is in markdown the wrap works very poorly, it's done much too far
            # to the right

            text_qll.setContentsMargins(5, 5, 3, 3)
            if fd_obj.get_type() == kammanta.glob.TypeEnum.note_file:
                text_qll.setOpenExternalLinks(True)
                text_qll.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
                # -please note that for a link to be clickable it needs to be in html format,
                #  in other words you cannot just enter an url without using the <a> tag
                # text_qll.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
                # text_qll.setTextFormat(QtCore.Qt.MarkdownText)
                # -an advantage with this is that it solves the problem discussed in the comment above,
                #  that is: It makes links that are given in plain text clickable!
                text_qll.setText(fd_obj.get_text_contents())
            else:
                text_qll.setText(fd_obj.get_name())
                new_font = QtGui.QFont("Courier")
                # new_font.setStyleHint(QtGui.QFont.Courier)
                text_qll.setFont(new_font)

            open_qpb = QtWidgets.QPushButton("Open")
            open_qpb.setFixedWidth(60)
            open_qpb.setFlat(True)
            open_qpb.setAutoFillBackground(True)
            partial_open_clicked_func = functools.partial(self.on_open_clicked, fd_obj.get_name())
            open_qpb.clicked.connect(partial_open_clicked_func)

            delete_qpb = QtWidgets.QPushButton("Del")
            delete_qpb.setFixedWidth(45)
            delete_qpb.setFlat(True)
            delete_qpb.setAutoFillBackground(True)
            partial_remove_clicked_func = functools.partial(self.on_delete_clicked, fd_obj.get_name())
            # -this works, very nice! GOOD TO USE AGAIN IN THE FUTURE
            # -Please note that we don't need to use setData!
            delete_qpb.clicked.connect(partial_remove_clicked_func)

            process_qpb = QtWidgets.QPushButton("Process >")
            partial_process_clicked_func = functools.partial(self.on_process_clicked, fd_obj.get_name())
            # -this works, very nice! GOOD TO USE AGAIN IN THE FUTURE
            # -please note that we don't need to use setData!
            process_qpb.clicked.connect(partial_process_clicked_func)
            widget_l1 = QtWidgets.QWidget()
            # widget_l1.setContentsMargins(0, 0, 0, 0)
            ############## widget_l1.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
            vbox_l1 = QtWidgets.QVBoxLayout()
            widget_l1.setLayout(vbox_l1)
            vbox_l1.setContentsMargins(0, 0, 0, 0)

            vbox_l1.addWidget(text_qll)

            controls_hbox_l2 = QtWidgets.QHBoxLayout()
            controls_hbox_l2.setContentsMargins(0, 0, 0, 0)
            vbox_l1.addLayout(controls_hbox_l2)
            controls_hbox_l2.addWidget(open_qpb)
            controls_hbox_l2.addWidget(delete_qpb)
            controls_hbox_l2.addWidget(process_qpb)
            controls_hbox_l2.addStretch(1)

            lwi = QtWidgets.QListWidgetItem()
            lwi.setSizeHint(widget_l1.sizeHint())
            self.notes_qlw.addItem(lwi)
            self.notes_qlw.setItemWidget(lwi, widget_l1)

    def on_process_clicked(self, i_id: str):
        self.row_selected_signal.emit(i_id)

    def on_delete_clicked(self, i_id: str):
        # inbox_file_obj = gtd.model.inbox_dir.get_item(i_id)
        self.collection_ptr.delete_item(i_id)
        # inbox_file_obj.delete()
        self.update_gui()

    def on_open_clicked(self, i_id: str):
        file_obj = self.collection_ptr.get_item(i_id)
        file_path_str = file_obj.get_path()
        kammanta.glob.launch_string(file_path_str)


"""
class CustomPushButton(QtWidgets.QPushButton):
    def __init__(self, i_title: str, i_click_handler_func):
        super().__init__()

        move_to_tickler_qpb = QtWidgets.QPushButton(i_title)
        partial_remove_clicked_func = functools.partial(
            self.on_move_to_tickler_clicked, fd_obj.get_name()
        )
        move_to_tickler_qpb.clicked.connect(self.on_move_to_tickler_clicked)
        move_to_tickler_qpb.setAutoFillBackground(True)
        move_to_tickler_qpb.setFlat(True)
"""

