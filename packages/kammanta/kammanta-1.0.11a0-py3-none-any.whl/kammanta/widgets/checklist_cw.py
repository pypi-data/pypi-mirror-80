import functools
import logging
import os
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import kammanta.model
import kammanta.glob
import kammanta.widgets.path_sel_dlg
import datetime
import kammanta.widgets.focus_dlg


class ChecklistWidget(QtWidgets.QWidget):
    active_focus_dlg = None
    focus_active_signal = QtCore.pyqtSignal(bool)

    def __init__(self, i_parent, i_collection_ptr):
        super().__init__(i_parent)
        self.coll_ptr = i_collection_ptr
        self.updating_gui_bool = False
        self.right_click_menu = None
        self.name_label_dict = {}  # -stores references, for updating the font with strikeout
        self.move_dest_action_list = []

        # Checking for default context/_ selections
        key_str = self.coll_ptr.get_collection_type().name
        default_context_str = kammanta.glob.get_string_from_config(
            kammanta.glob.SETTINGS_SECTION_GENERAL_STR,
            key_str,
            ""
        )
        if default_context_str:
            self.coll_ptr.set_active_item(default_context_str)
            # self.context_selection_qcb.setCurrentText(default_context_str)

        # Creating widgets.. -------------------------------

        title_str = self.coll_ptr.get_main_title()
        self.title_qll = QtWidgets.QPushButton(title_str)
        # , parent=self
        self.title_qll.setFlat(True)
        self.title_qll.setFont(kammanta.glob.get_title_font())
        self.title_qll.clicked.connect(self.on_title_clicked)

        self.description_qll = QtWidgets.QLabel()
        self.description_qll.setWordWrap(True)

        self.item_list_widget = QtWidgets.QListWidget(self)
        # MyListWidget(self)  # -please note: created before context_qcb
        # self.item_list_widget.resized_signal.connect(self.on_resize_signal)
        # self.list_widget.setStyleSheet("QListWidget::Item {border: 1px solid black}")
        self.item_list_widget.currentRowChanged.connect(self.on_item_list_current_row_changed)
        self.item_list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.item_list_widget.setSpacing(0)

        # ..for combobox setup (ex NA, prj) -------------------------------

        self.context_selection_qcb = QtWidgets.QComboBox()
        # - do we need to set the parent?
        # -Please note: there is a method called setParent() that we can use instead of setting the parent here
        self.context_selection_qcb.currentTextChanged.connect(self.on_combobox_file_selection_text_changed)
        # self.coll_selection_qcb.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.context_selection_qcb.setMaximumWidth(200)

        self.options_menu = QtWidgets.QMenu(parent=self)

        self.open_action = QtWidgets.QAction("Open File/Dir")
        # -please note that the actions have to be prefixed by "self.", otherwise they will not be shown!
        self.open_action.triggered.connect(self.open_coll_action_triggered)
        self.options_menu.addAction(self.open_action)
        self.clear_completed_action = QtWidgets.QAction("Clear completed")
        self.clear_completed_action.triggered.connect(self.on_clear_completed_clicked)
        self.options_menu.addAction(self.clear_completed_action)
        self.new_collection_action = QtWidgets.QAction("Add New")
        self.new_collection_action.triggered.connect(self.on_add_new_coll_action_triggered)
        self.options_menu.addAction(self.new_collection_action)
        self.rename_coll_action = QtWidgets.QAction("Rename")
        self.rename_coll_action.triggered.connect(self.on_rename_coll)
        self.options_menu.addAction(self.rename_coll_action)
        self.delete_coll_action = QtWidgets.QAction("Delete")
        self.delete_coll_action.triggered.connect(self.on_delete_coll)
        self.options_menu.addAction(self.delete_coll_action)
        self.set_as_default_coll_action = QtWidgets.QAction("Set as default")
        self.set_as_default_coll_action.triggered.connect(self.on_set_as_default_coll)
        self.options_menu.addAction(self.set_as_default_coll_action)

        self.edit_descr_action = QtWidgets.QAction("Edit description")
        self.edit_descr_action.triggered.connect(self.on_edit_descr)
        self.options_menu.addAction(self.edit_descr_action)

        self.collection_options_qpb = QtWidgets.QPushButton("Options")
        self.collection_options_qpb.setMenu(self.options_menu)

        # ..for listwidget setup (ex agenda) -------------------------------

        self.context_selection_qlw = QtWidgets.QListWidget()
        # - do we need to set the parent?
        self.context_selection_qlw.currentItemChanged.connect(self.on_coll_list_file_item_changed)
        self.clear_completed_qpb = QtWidgets.QPushButton("Clear completed")
        self.clear_completed_qpb.clicked.connect(self.on_clear_completed_clicked)
        self.open_coll_file_qpb = QtWidgets.QPushButton("Open")
        self.open_coll_file_qpb.clicked.connect(self.open_coll_action_triggered)
        self.add_new_coll_qle = QtWidgets.QLineEdit()
        self.add_new_coll_qle.setPlaceholderText("placeholder text ----")
        # -perhaps allow customization of this, for example in settings.ini (globally) or in each context file
        self.add_new_context_qpb = QtWidgets.QPushButton("Add new")
        self.add_new_context_qpb.clicked.connect(self.on_add_new_coll_clicked)
        self.rename_context_qpb = QtWidgets.QPushButton("Rename")
        self.rename_context_qpb.clicked.connect(self.on_rename_coll)
        self.delete_context_qpb = QtWidgets.QPushButton("Delete")
        self.delete_context_qpb.clicked.connect(self.on_delete_coll)
        self.add_new_coll_qle.returnPressed.connect(self.add_new_context_qpb.click)

        # ..shared -------------------------------

        self.focus_qpb = QtWidgets.QPushButton("Focus")
        self.focus_qpb.clicked.connect(self.on_focus_clicked)

        self.rename_item_qpb = QtWidgets.QPushButton("Rename")
        self.rename_item_qpb.clicked.connect(self.on_rename_item)
        self.delete_item_qpb = QtWidgets.QPushButton("Delete")
        self.delete_item_qpb.clicked.connect(self.on_delete_clicked)
        self.copy_text_qpb = QtWidgets.QPushButton("Copy text")
        self.copy_text_qpb.clicked.connect(self.copy_item_text)
        self.set_support_path_qpb = QtWidgets.QPushButton("Set support")
        self.set_support_path_qpb.clicked.connect(self.update_item_support_path)
        self.open_support_path_qpb = QtWidgets.QPushButton("Open support")
        self.open_support_path_qpb.clicked.connect(self.open_item_support)
        self.move_qpb = QtWidgets.QPushButton("Move")
        self.move_menu = QtWidgets.QMenu()
        self.move_qpb.setMenu(self.move_menu)
        self.move_menu.triggered.connect(self.on_move_menu_triggered)

        self.convert_qpb = QtWidgets.QPushButton("Convert")
        self.convert_menu = QtWidgets.QMenu(self)
        self.convert_to_text_file_action = QtWidgets.QAction("... to text file")
        self.convert_to_text_file_action.triggered.connect(self.on_convert_to_text_file_triggered)
        self.convert_menu.addAction(self.convert_to_text_file_action)
        self.convert_to_directory_action = QtWidgets.QAction("... directory")
        self.convert_to_directory_action.triggered.connect(self.on_convert_to_directory_triggered)
        self.convert_menu.addAction(self.convert_to_directory_action)
        self.convert_to_desktop_link_action = QtWidgets.QAction("... .desktop link")
        self.convert_to_desktop_link_action.triggered.connect(self.on_convert_to_desktop_link_triggered)
        self.convert_menu.addAction(self.convert_to_desktop_link_action)
        self.convert_qpb.setMenu(self.convert_menu)

        self.add_new_item_qle = QtWidgets.QLineEdit()
        self.add_new_item_qle.setPlaceholderText("Research, look into, organize, write code")
        # -perhaps allow customization of this, for example in settings.ini (globally) or in each context file
        self.add_new_item_qpb = QtWidgets.QPushButton("Add new")

        coll_type = self.coll_ptr.get_collection_type()
        if coll_type == kammanta.glob.CollTypeEnum.projects:
            self.new_prj_menu = QtWidgets.QMenu()
            self.file_prj_action = QtWidgets.QAction("File")
            self.file_prj_action.triggered.connect(self.on_file_prj_clicked)
            self.new_prj_menu.addAction(self.file_prj_action)
            self.dir_prj_action = QtWidgets.QAction("Directory")
            self.dir_prj_action.triggered.connect(self.on_dir_prj_clicked)
            self.new_prj_menu.addAction(self.dir_prj_action)
            self.link_prj_action = QtWidgets.QAction("Link")
            self.link_prj_action.triggered.connect(self.on_link_prj_clicked)
            self.new_prj_menu.addAction(self.link_prj_action)
            self.add_new_item_qpb.setMenu(self.new_prj_menu)
        else:
            self.add_new_item_qpb.clicked.connect(self.on_add_new_item_clicked)
        self.add_new_item_qle.returnPressed.connect(self.add_new_item_qpb.click)

        self.list_area_qsw = QtWidgets.QStackedWidget()
        self.no_list_message_qll = QtWidgets.QLabel("No list selected, please __________")
        self.list_area_qsw.addWidget(self.no_list_message_qll)
        self.list_area_qsw.addWidget(self.item_list_widget)
        self.list_area_qsw.setCurrentWidget(self.no_list_message_qll)

        # Layouts =========================

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        if coll_type in [kammanta.glob.CollTypeEnum.projects, kammanta.glob.CollTypeEnum.next_actions]:
            top_hbox_l3 = QtWidgets.QHBoxLayout()
            vbox_l2.addLayout(top_hbox_l3)
            top_hbox_l3.addWidget(self.title_qll)
            top_hbox_l3.addStretch(1)
            top_hbox_l3.addWidget(QtWidgets.QLabel("Context:"))
            top_hbox_l3.addWidget(self.context_selection_qcb)
            top_hbox_l3.addWidget(self.collection_options_qpb)
        elif coll_type == kammanta.glob.CollTypeEnum.agendas:
            hbox_l3 = QtWidgets.QHBoxLayout()
            vbox_l2.addLayout(hbox_l3)
            hbox_l3.addWidget(self.title_qll)
            hbox_l3.addStretch(1)
            hbox_l3 = QtWidgets.QHBoxLayout()
            vbox_l2.addLayout(hbox_l3, stretch=1)
            hbox_l3.addWidget(self.context_selection_qlw, stretch=1)
            controls_vbox_l5 = QtWidgets.QVBoxLayout()
            hbox_l3.addLayout(controls_vbox_l5)
            controls_vbox_l5.addStretch(1)
            controls_vbox_l5.addWidget(self.clear_completed_qpb)
            controls_vbox_l5.addWidget(self.open_coll_file_qpb)
            controls_vbox_l5.addWidget(self.add_new_coll_qle)
            controls_vbox_l5.addWidget(self.add_new_context_qpb)
            controls_vbox_l5.addWidget(self.rename_context_qpb)
            controls_vbox_l5.addWidget(self.delete_context_qpb)
            controls_vbox_l5.addStretch(1)
        else:
            logging.debug(self.coll_ptr.get_path())
            logging.debug(kammanta.glob.get_path())
            raise Exception("Case not covered")

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        hbox_l3.addWidget(self.add_new_item_qle)
        hbox_l3.addWidget(self.add_new_item_qpb)

        vbox_l2.addWidget(self.description_qll)

        vbox_l2.addWidget(self.list_area_qsw, stretch=4)  # <--- Main part of the GUI

        controls_top_row_hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(controls_top_row_hbox_l3)
        controls_top_row_hbox_l3.addWidget(self.focus_qpb)
        controls_top_row_hbox_l3.addWidget(self.rename_item_qpb)
        controls_top_row_hbox_l3.addWidget(self.delete_item_qpb)
        controls_top_row_hbox_l3.addWidget(self.copy_text_qpb)

        controls_btm_row_hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(controls_btm_row_hbox_l3)
        controls_btm_row_hbox_l3.addWidget(self.set_support_path_qpb)
        controls_btm_row_hbox_l3.addWidget(self.open_support_path_qpb)
        controls_btm_row_hbox_l3.addWidget(self.move_qpb)
        controls_btm_row_hbox_l3.addWidget(self.convert_qpb)

        # =========================

        self.on_item_list_current_row_changed(-1)

    # overridden
    def keyPressEvent(self, i_qkeyevent: QtGui.QKeyEvent):
        """
        This override doesn't seem to capture standard key presses A-Z, but it does capture
        function (F1-F12) keys, as well as standard keys A-Z *if* they are accompanied by
        a modifier.
        Common functions of the keys F1-F12: https://www.computerhope.com/issues/ch000306.htm
        """
        keyevent_key = i_qkeyevent.key()
        if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            if keyevent_key == QtCore.Qt.Key_C:
                logging.debug("Ctrl + C")
                self.copy_text_qpb.click()
                return
        elif keyevent_key == QtCore.Qt.Key_F2:
            self.rename_item_qpb.click()
            return
        elif keyevent_key == QtCore.Qt.Key_Delete:
            self.delete_item_qpb.click()
            return
        elif keyevent_key == QtCore.Qt.Key_F3:
            self.focus_qpb.click()
            return
        super().keyPressEvent(i_qkeyevent)
        # -if we get here it means that the key has not been captured elsewhere (or possibly
        # that the key has been captured but that we want "double handling" of the key event)

    def on_add_new_item_clicked(self):
        new_item_text_str = self.add_new_item_qle.text()
        self.add_new_item_qle.clear()
        active_context = self.coll_ptr.get_active_item()
        new_obj = active_context.add_new_item(new_item_text_str)
        self.update_gui_and_ids()
        if new_obj:
            support_path_str = new_obj.get_support_path()
            if support_path_str:
                kammanta.glob.launch_string(support_path_str)

    def on_file_prj_clicked(self):
        self._create_new_prj_entity(".txt")

    def on_dir_prj_clicked(self):
        self._create_new_prj_entity("")

    def on_link_prj_clicked(self):
        self._create_new_prj_entity(".desktop")

    def _create_new_prj_entity(self, i_suffix: str):
        new_item_text_str = self.add_new_item_qle.text()
        self.add_new_item_qle.clear()
        active_context = self.coll_ptr.get_active_item()
        QtGui.QGuiApplication.processEvents()
        new_obj = active_context.add_new_item(new_item_text_str + i_suffix)
        self.update_gui_and_ids()
        if new_obj:
            new_path_str = new_obj.get_path()

            name_formatted_str = new_item_text_str + i_suffix
            name_formatted_str = name_formatted_str.strip()

            if os.path.isfile(new_path_str) and new_path_str.endswith(".desktop"):
                (path_str, result_enum) = kammanta.widgets.path_sel_dlg.PathSelDlg.open_dlg_and_get_path(
                    None, kammanta.widgets.path_sel_dlg.PathSelectionEnum.dir, "", ""
                )
                if result_enum != kammanta.widgets.path_sel_dlg.PathSelectionEnum.cancelled:
                    ###### new_rel_path_strlist = new_obj.rel_path_strlist + [name_formatted_str]
                    new_file_obj = kammanta.model.DesktopFile(
                        new_obj.collection_type,
                        new_obj.rel_path_strlist
                    )
                    new_file_obj.update_desktop_file(path_str)
            elif os.path.isfile(new_path_str) and new_path_str.endswith(".txt"):
                contents_str = ""
                with open("kammanta/prj-template.txt", "r") as f:
                    contents_str = f.read()
                with open(new_path_str, "r+") as f:
                    if len(f.read()) == 0:
                        f.write(contents_str)
                    else:
                        pass
            # Opening the support
            support_path_str = new_obj.get_support_path()
            if support_path_str:
                kammanta.glob.launch_string(support_path_str)

    def on_focus_clicked(self):
        active_context = self.coll_ptr.get_active_item()
        active_item = active_context.get_active_item()

        ChecklistWidget.active_focus_dlg = kammanta.widgets.focus_dlg.FocusDlg(active_item)
        # -there can only be one focus
        self.focus_active_signal.emit(True)
        ChecklistWidget.active_focus_dlg.exec_()
        # -modal (stops execution in the rest of the application)
        self.focus_active_signal.emit(False)
        ChecklistWidget.active_focus_dlg = None

    def on_move_menu_triggered(self, i_action: QtWidgets.QAction):
        dest_id_str = i_action.text()
        self.coll_ptr.move_active_granditem(dest_id_str)
        self.update_gui_and_ids()

    def on_convert_to_text_file_triggered(self):
        active_item = self.coll_ptr.get_active_item()
        active_sub_item = active_item.get_active_item()
        active_sub_item_id = active_sub_item.get_id()
        active_item.convert_item_to_file(active_sub_item_id)
        self.update_gui_and_ids()

    def on_convert_to_directory_triggered(self):
        active_item = self.coll_ptr.get_active_item()
        active_sub_item = active_item.get_active_item()
        active_sub_item_id = active_sub_item.get_id()
        active_item.convert_item_to_dir(active_sub_item_id)
        self.update_gui_and_ids()

    def on_convert_to_desktop_link_triggered(self):
        new_dir_path_str = QtWidgets.QFileDialog.getExistingDirectory(self, "Destination directory")
        if new_dir_path_str:
            active_item = self.coll_ptr.get_active_item()
            active_sub_item = active_item.get_active_item()
            active_sub_item_id = active_sub_item.get_id()
            active_item.convert_item_to_link(active_sub_item_id, new_dir_path_str)
            self.update_gui_and_ids()

    def on_title_clicked(self):
        path_str = self.coll_ptr.get_path()
        kammanta.glob.launch_string(path_str)

    def on_add_new_coll_action_triggered(self):
        result_str, result_bool = QtWidgets.QInputDialog.getText(self, "New collection", "new coll")
        if not result_bool:
            return
        coll_type = self.coll_ptr.get_collection_type()
        if coll_type == kammanta.glob.CollTypeEnum.next_actions:
            result_str = kammanta.glob.add_suffix(result_str, kammanta.glob.TEXT_SUFFIX_STR)
        elif coll_type == kammanta.glob.CollTypeEnum.agendas:
            result_str = kammanta.glob.add_suffix(result_str, kammanta.glob.TEXT_SUFFIX_STR)
        elif coll_type == kammanta.glob.CollTypeEnum.projects:
            result_str = kammanta.glob.add_prefix_to_basename(result_str, "projects-")
        self.coll_ptr.add_new_item(result_str)
        self.update_gui_and_ids()
        self.on_combobox_file_selection_text_changed(result_str)

    def on_edit_descr(self):
        active_coll = self.coll_ptr.get_active_item()
        old_descr_str = active_coll.get_description()
        result_str, result_bool = QtWidgets.QInputDialog.getText(
            self, "Edit description",
            "Edit description (to remove description simply clear the text)", text=old_descr_str
        )
        if not result_bool:
            return
        active_coll.set_description(result_str)
        self.update_gui_and_ids()

    def on_rename_coll(self):
        old_core_name_str = self.coll_ptr.get_active_item().get_core_name()
        result_str, result_bool = QtWidgets.QInputDialog.getText(
            self, "Rename collection", "Rename coll", text=old_core_name_str
        )
        if not result_bool:
            return
        self.coll_ptr.get_active_item().set_core_name(result_str)
        self.update_gui_and_ids()

    def open_coll_action_triggered(self):
        file_path_str = self.coll_ptr.get_active_item().get_path()
        kammanta.glob.launch_string(file_path_str)

    def on_item_double_clicked(self, i_lwi: QtWidgets.QListWidgetItem):
        self.open_item_support()

    def copy_item_text(self):
        active_coll = self.coll_ptr.get_active_item()
        if active_coll is None:
            logging.error("No active collection when trying to copy")
        active_item = active_coll.get_active_item()
        if active_item is None:
            logging.error("No active item when trying to copy")
        descr_str = active_item.get_core_name()
        qt_clipboard = QtGui.QGuiApplication.clipboard()
        qt_clipboard.clear(mode=QtGui.QClipboard.Clipboard)
        qt_clipboard.setText(descr_str, mode=QtGui.QClipboard.Clipboard)

    def open_item_support(self):
        active_item = self.coll_ptr.get_active_item()
        if not active_item:
            return
        active_sub_item = active_item.get_active_item()
        if not active_sub_item:
            return
        sp_str = active_sub_item.get_support_path()
        sp_str = sp_str.strip()
        # -removing space at beginning
        if sp_str:
            try:
                kammanta.glob.launch_string(sp_str)
            except Exception:
                QtWidgets.QMessageBox.warning(self, "title", "cannot open")

    def update_item_support_path(self):
        active_sub_item = self.coll_ptr.get_active_item().get_active_item()
        old_support_path_with_name_str = active_sub_item.get_support_path()
        default_path_str = ""
        default_name_str = ""
        initial_enum = kammanta.widgets.path_sel_dlg.PathSelectionEnum.dir
        if old_support_path_with_name_str:
            default_path_str = os.path.dirname(old_support_path_with_name_str)
            default_name_str = os.path.basename(old_support_path_with_name_str)
            if os.path.isfile(old_support_path_with_name_str):
                initial_enum = kammanta.widgets.path_sel_dlg.PathSelectionEnum.file
            elif os.path.isdir(old_support_path_with_name_str):
                initial_enum = kammanta.widgets.path_sel_dlg.PathSelectionEnum.dir
            else:
                default_path_str = kammanta.glob.get_path()
                default_name_str = old_support_path_with_name_str
                initial_enum = kammanta.widgets.path_sel_dlg.PathSelectionEnum.weblink
                # logging.warning("The old path is neither a file nor a directory")
        else:
            if self.coll_ptr.get_collection_type() == kammanta.glob.CollTypeEnum.next_actions:
                initial_enum = kammanta.widgets.path_sel_dlg.PathSelectionEnum.file
                default_path_str = kammanta.glob.create_and_get_path(kammanta.model.NA_DEFAULT_SUPPORT_DIR)
                # gtd.model.get_path(gtd.model.NA_DEFAULT_SUPPORT_DIR)
                for char_str in active_sub_item.get_core_name():
                    if char_str.isalnum():
                        default_name_str += char_str
                    else:
                        default_name_str += "_"
                default_name_str += kammanta.glob.TEXT_SUFFIX_STR
                # default_support_path_str = "".join(c for c in default_support_path_str if c.isalnum())
                # -special chars removed
            else:  # -for projects
                initial_enum = kammanta.widgets.path_sel_dlg.PathSelectionEnum.dir

        (path_str, result_enum) = kammanta.widgets.path_sel_dlg.PathSelDlg.open_dlg_and_get_path(
            None, initial_enum, default_path_str, default_name_str
        )

        if result_enum == kammanta.widgets.path_sel_dlg.PathSelectionEnum.cancelled:
            pass
        else:
            logging.info("path_str = " + path_str)
            active_sub_item.set_support_path(path_str)
        self.update_gui_item_list_and_ids()

    def on_rename_item(self):
        old_line_str = self.coll_ptr.get_active_item().get_active_item().get_core_name()

        input_dialog = QtWidgets.QInputDialog(self)
        input_dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        input_dialog.setLabelText("Renaming")
        input_dialog.setWindowTitle("Renaming")
        # input_dialog.setFixedWidth(700)
        input_dialog.resize(510, input_dialog.height())
        input_dialog.setTextValue(old_line_str)

        ok_bool = input_dialog.exec_()
        new_line_str = input_dialog.textValue()
        if ok_bool:
            active_context = self.coll_ptr.get_active_item()
            active_item = active_context.get_active_item()
            active_item.set_core_name(new_line_str)
            self.update_gui_item_list_and_ids()

    def on_set_as_default_coll(self):
        key_str = self.coll_ptr.get_collection_type().name
        active_context = self.coll_ptr.get_active_item()
        active_context_id_str = active_context.get_id()
        kammanta.glob.add_string_to_config(
            kammanta.glob.SETTINGS_SECTION_GENERAL_STR,
            key_str,
            active_context_id_str
        )

    def on_delete_coll(self):
        active_item = self.coll_ptr.get_active_item()
        if len(active_item.get_all_items()) > 0:
            QtWidgets.QMessageBox.information(
                self, "Cannot delete",
                "You cannot delete this until all items have been removed first"
            )
        else:
            code_for_button_clicked_int = QtWidgets.QMessageBox.question(
                self, "Title", "Are you sure you want to delete this?",
                defaultButton=QtWidgets.QMessageBox.No
            )
            if code_for_button_clicked_int == QtWidgets.QMessageBox.Yes:
                self.coll_ptr.delete_item(active_item.get_id())
                self.update_gui_and_ids()
                active_id_str = self.coll_ptr.get_active_item().get_id()
                # self.on_combobox_file_selection_text_changed(active_id_str, override=True)

    def on_delete_clicked(self):
        code_for_button_clicked_int = QtWidgets.QMessageBox.question(
            self, "Title", "Are you sure you want to delete this?",
            defaultButton=QtWidgets.QMessageBox.No
        )
        if code_for_button_clicked_int == QtWidgets.QMessageBox.Yes:
            active_item = self.coll_ptr.get_active_item().get_active_item()
            self.coll_ptr.get_active_item().delete_item(active_item.get_id())
            self.update_gui_and_ids()

    def on_clear_completed_clicked(self):
        active_context = self.coll_ptr.get_active_item()
        active_context.clear_completed()
        self.update_gui_and_ids()

    def on_combobox_file_selection_text_changed(self, i_new_text: str, override: bool = False):
        if self.updating_gui_bool and not override:
            return
        data_str = self.context_selection_qcb.currentData()
        # -default is QtCore.Qt.UserRole
        self.coll_ptr.set_active_item(data_str)
        self.update_gui_and_ids()

    def on_coll_list_file_item_changed(self, i_new: QtWidgets.QListWidgetItem, i_prev: QtWidgets.QListWidgetItem):
        if self.updating_gui_bool:
            return
        id_str = i_new.data(QtCore.Qt.UserRole)
        self.coll_ptr.set_active_item(id_str)
        self.update_gui_and_ids()

    def on_add_new_coll_clicked(self):
        new_core_name_str = self.add_new_coll_qle.text()
        new_file_name_str = kammanta.glob.add_suffix(new_core_name_str, kammanta.glob.TEXT_SUFFIX_STR)
        self.coll_ptr.add_new_item(new_file_name_str)
        self.update_gui_and_ids()

    def on_item_list_current_row_changed(self, i_current_list_row: int):
        logging.debug(str(i_current_list_row))

        self.focus_qpb.setEnabled(False)
        self.rename_item_qpb.setEnabled(False)
        self.delete_item_qpb.setEnabled(False)
        self.copy_text_qpb.setEnabled(False)
        self.move_qpb.setEnabled(False)
        self.convert_qpb.setEnabled(False)
        self.convert_to_text_file_action.setEnabled(False)
        self.convert_to_directory_action.setEnabled(False)
        self.convert_to_desktop_link_action.setEnabled(False)
        self.open_support_path_qpb.setEnabled(False)
        self.set_support_path_qpb.setEnabled(False)

        current_lwi: QtWidgets.QListWidgetItem = self.item_list_widget.item(i_current_list_row)
        if current_lwi is not None:
            id_str = current_lwi.data(QtCore.Qt.UserRole)
            # self.list_row_changed_signal.emit(id_str)
            # self.row_ptr = self.list_ptr.get_row(id_str)
            active_coll = self.coll_ptr.get_active_item()
            active_coll.set_active_item(id_str)
            active_item = active_coll.get_active_item()
            self.list_area_qsw.setCurrentWidget(self.item_list_widget)
            # self.convert_qpb.setEnabled(True)

            self.focus_qpb.setEnabled(True)
            self.rename_item_qpb.setEnabled(True)
            self.delete_item_qpb.setEnabled(True)
            self.copy_text_qpb.setEnabled(True)
            self.move_qpb.setEnabled(True)

            if active_item.get_type() in kammanta.glob.any_file_enumlist:
                self.convert_to_directory_action.setEnabled(True)
                self.convert_to_desktop_link_action.setEnabled(True)
                self.convert_qpb.setEnabled(True)
            elif active_item.get_type() == kammanta.glob.TypeEnum.dir:
                self.convert_to_text_file_action.setEnabled(True)
                self.convert_to_desktop_link_action.setEnabled(True)
                self.convert_qpb.setEnabled(True)
            elif active_item.get_type() == kammanta.glob.TypeEnum.desktop_file:
                self.convert_to_text_file_action.setEnabled(True)
                self.convert_to_directory_action.setEnabled(True)
                self.set_support_path_qpb.setEnabled(True)
                self.convert_qpb.setEnabled(True)
            elif active_item.get_type() == kammanta.glob.TypeEnum.line:
                self.set_support_path_qpb.setEnabled(True)

            if active_item.get_support_path():
                self.open_support_path_qpb.setEnabled(True)

    def on_item_checkbox_clicked(self, i_id: str, i_checked: bool):
        # for rename: self.collection_ptr.get_active_item().get_active_item().set_core_name(new_line_str)
        logging.debug("on_checkbox_clicked id = " + i_id)
        active_context = self.coll_ptr.get_active_item()
        active_context.set_active_item(i_id)
        item = active_context.get_active_item()
        item.set_completed(i_checked)
        support_path_str = item.get_support_path()
        if i_checked and support_path_str:
            kammanta.glob.launch_string(support_path_str)
        self.update_gui_and_ids()

    def _update_context_gui_and_ids(self):
        # -idea: updating only one of the contexts
        coll_item_list = self.coll_ptr.get_all_items()
        active_coll = self.coll_ptr.get_active_item()

        # for the list widget
        active_qlwi = None
        self.context_selection_qlw.clear()
        for coll_item in coll_item_list:
            nr_of_remaining_items_in_coll_int = 0
            for item in coll_item.get_all_items():
                if not item.is_completed():
                    nr_of_remaining_items_in_coll_int += 1
            entry_str = coll_item.get_name() + " (" + str(nr_of_remaining_items_in_coll_int) + ")"
            qlwi = QtWidgets.QListWidgetItem(entry_str)
            qlwi.setData(QtCore.Qt.UserRole, coll_item.get_id())
            self.context_selection_qlw.addItem(qlwi)
            if active_coll is not None and active_coll.get_id() == coll_item.get_id():
                active_qlwi = qlwi
            # coll_item_path_str = coll_item.get_path()
            # kammanta.glob.FswSingleton.get().addPath(coll_item_path_str)
        if active_qlwi is not None:
            self.context_selection_qlw.setCurrentItem(active_qlwi)

        # for the combo box
        # if self.file_selection_qlw.currentRow() != -1:
        #   current_file_name_str = self.file_selection_qlw.coll_item(self.file_selection_qlw.currentRow())
        active_coll_text_str = ""
        self.context_selection_qcb.clear()
        for coll_item in coll_item_list:
            nr_of_remaining_items_in_coll_int = 0
            for item in coll_item.get_all_items():
                if not item.is_completed():
                    nr_of_remaining_items_in_coll_int += 1
            entry_str = coll_item.get_name() + " (" + str(nr_of_remaining_items_in_coll_int) + ")"
            # entry_str = coll_item.get_name()
            self.context_selection_qcb.addItem(entry_str, userData=coll_item.get_id())
            # -please note *userData=*, this is like setData() for QListWidgets
            if active_coll is not None and active_coll.get_id() == coll_item.get_id():
                active_coll_text_str = entry_str  # <----------
        if active_coll is None and len(coll_item_list) > 0:
            # This is a complicated operation to make sure that the user will see the contents
            # of a context after having delted another
            active_coll_item = coll_item_list[0]
            active_coll_item_id_str = active_coll_item.get_id()
            self.coll_ptr.set_active_item(active_coll_item_id_str)
            index_int = self.context_selection_qcb.findData(active_coll_item_id_str)
            active_coll_text_str = self.context_selection_qcb.itemText(index_int)
        if active_coll_text_str:
            # self.updating_gui_bool = False
            self.context_selection_qcb.setCurrentText(active_coll_text_str)
            # self.updating_gui_bool = True

    def _update_item_strikeout(self, i_id: str):
        # Updating just the single row, and not the entire list (this avoids the list scrolling to the top)
        context = self.coll_ptr.get_active_item()
        item = context.get_item(i_id)
        name_qll = self.name_label_dict[i_id]
        new_font = name_qll.font()
        if item.is_completed():
            new_font.setStrikeOut(True)
        else:
            new_font.setStrikeOut(False)
        name_qll.setFont(new_font)

    def set_active_item(self, i_item_id: str):
        # -To be called from the outside
        # TODO: Not implemented yet
        pass
        # self._update_context_gui_and_ids()

    def update_gui_and_ids(self):
        if self.updating_gui_bool:
            return
        self.updating_gui_bool = True

        self._update_context_gui_and_ids()

        self.move_menu.clear()
        context_list = self.coll_ptr.get_all_items()
        self.move_dest_action_list = []
        for context in context_list:
            id_str = context.get_id()
            qaction = QtWidgets.QAction(id_str)
            self.move_dest_action_list.append(qaction)
            self.move_menu.addAction(qaction)

        active_context = self.coll_ptr.get_active_item()
        validator = QtGui.QRegExpValidator()
        if active_context:
            self.list_area_qsw.setCurrentWidget(self.item_list_widget)
            # self.convert_qpb.setEnabled(True)
            descr_str = active_context.get_description()
            if descr_str:
                self.description_qll.setVisible(True)
                self.description_qll.setText(descr_str)
            else:
                self.description_qll.setVisible(False)
            self.update_gui_item_list_and_ids()
            regexp_validator_str = active_context.get_child_regexp_text()
            if regexp_validator_str:
                q_reg_exp = QtCore.QRegExp(regexp_validator_str)
                validator.setRegExp(q_reg_exp)
        else:
            self.list_area_qsw.setCurrentWidget(self.no_list_message_qll)
            # self.convert_qpb.setEnabled(False)

        self.add_new_item_qle.setValidator(validator)

        self.updating_gui_bool = False

    @staticmethod
    def _get_dir_support_info(i_support_path: str) -> str:
        (nr_of_files_int, latest_edit_time_ts_int) = kammanta.glob.get_nr_items_and_last_mod_time(i_support_path)
        newest_dt = datetime.date.fromtimestamp(latest_edit_time_ts_int)
        newest_str = str(newest_dt)
        nr_of_files_str = "many!"
        if nr_of_files_int != -1:
            nr_of_files_str = str(nr_of_files_int)
        directory_info_str = f" [files: {nr_of_files_str}] [edited: {newest_str}]"
        return directory_info_str

    @staticmethod
    def _get_file_support_info(i_support_path: str) -> str:
        size_in_bytes_int = os.path.getsize(i_support_path)
        (nr_of_files_int, latest_edit_time_ts_int) = kammanta.glob.get_nr_items_and_last_mod_time(i_support_path)
        newest_dt = datetime.date.fromtimestamp(latest_edit_time_ts_int)
        newest_str = str(newest_dt)
        file_info_str = f" [file size: {str(size_in_bytes_int)}] [edited: {newest_str}]"
        return file_info_str

    def update_gui_item_list_and_ids(self):
        self.updating_gui_bool = True

        active_list = self.coll_ptr.get_active_item()
        if active_list is None:
            logging.debug("[update_gui_item_list_and_ids] warning: there is no active list, exiting method")
            return

        self.item_list_widget.clear()

        # ================== TEXT DATA ==================

        if self.coll_ptr.get_collection_type() == kammanta.glob.CollTypeEnum.projects:
            list_items = active_list.get_all_items(False)
        else:
            list_items = active_list.get_all_items()
        for item in list_items:
            base_fd_type_str = ""
            show_info_bl = False
            show_path_bl = False
            item_type_enum = item.get_type()
            # Old: if item.get_collection_type() == kammanta.glob.CollTypeEnum.projects:
            if active_list.get_type() == kammanta.glob.TypeEnum.dir:
                if item_type_enum == kammanta.glob.TypeEnum.dir:
                    base_fd_type_str = "[dir]"
                    show_info_bl = True
                elif item_type_enum == kammanta.glob.TypeEnum.desktop_file:
                    base_fd_type_str = "[link]"
                    show_info_bl = True
                    show_path_bl = True
                elif item_type_enum in kammanta.glob.any_file_enumlist:
                    suffix_str = kammanta.glob.get_dsuffix(item.get_support_path())
                    base_fd_type_str = f"[{suffix_str} file] "
                    show_info_bl = True
            else:
                if item.get_support_path():
                    base_fd_type_str = "[str]"
                    show_info_bl = True
                    show_path_bl = True

            support_type_str = ""
            fd_support_info_str = ""
            support_path_str = item.get_support_path()
            support_type_enum = kammanta.glob.get_type(support_path_str)
            if support_type_enum == kammanta.glob.TypeEnum.web_link:
                support_type_str = "[web] "
            elif support_type_enum == kammanta.glob.TypeEnum.dir:
                support_type_str = "[dir] "
                fd_support_info_str = self._get_dir_support_info(support_path_str)
            elif support_type_enum in kammanta.glob.any_file_enumlist:
                suffix_str = kammanta.glob.get_dsuffix(support_path_str)
                support_type_str = f"[{suffix_str} file] "
                fd_support_info_str = self._get_file_support_info(support_path_str)
            elif item.get_collection_type() == kammanta.glob.CollTypeEnum.projects:
                support_type_str = "<b>support error! file/dir/other doesn't exist</b>"

            name_str = item.get_core_name()
            extra_info_str = base_fd_type_str + fd_support_info_str
            # support_text_str = support_type_str + support_path_str

            # ================== LAYOUT ==================

            # Alt: Possibly using a standard item with checkbox,
            # and using html to the give a smaller font size for the support path
            # This would make it easier (fewer lines of code) and avoid differences in the height hint
            # https://ubuntuforums.org/showthread.php?t=1737380

            lwi = QtWidgets.QListWidgetItem(parent=self.item_list_widget)
            lwi_widget = QtWidgets.QWidget(parent=self.item_list_widget)
            # -we cannot give lwi as the parent since QListWidgetItem is not a subclass of QWidget

            lwi_hbox_2 = QtWidgets.QHBoxLayout()
            # lwi_hbox_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)  # <- Important
            lwi_hbox_2.setContentsMargins(8, 0, 0, 0)  # <- Important
            lwi_hbox_2.setSpacing(0)  # -this works
            lwi_widget.setLayout(lwi_hbox_2)

            # Checkbox
            checkbox_qcb = QtWidgets.QCheckBox()
            lwi_hbox_2.addWidget(checkbox_qcb)
            # checkbox_qcb.setContentsMargins(2, 0, 20, 0)
            checkbox_qcb.setChecked(item.is_completed())  # -important to do this before clicked.connect
            partial_checkbox_func = functools.partial(self.on_item_checkbox_clicked, item.get_id())
            # -this works, very nice! GOOD TO USE AGAIN IN THE FUTURE
            checkbox_qcb.clicked.connect(partial_checkbox_func)

            lwi_vbox_3 = QtWidgets.QVBoxLayout()
            lwi_vbox_3.setContentsMargins(8, 4, 0, 4)  # <- Important
            lwi_hbox_2.addLayout(lwi_vbox_3)

            # Item name
            name_qll = WrapLabel(lwi_widget, 2)
            # -giving lwi_widget as the parent works, but using self gives us a strange error
            # where painting is done above the list(!)
            lwi_vbox_3.addWidget(name_qll)
            name_qll.setText(name_str)
            self.name_label_dict[item.get_id()] = name_qll
            self._update_item_strikeout(item.get_id())
            # Item info
            info_qll = WrapLabel(lwi_widget, -2)
            if show_info_bl:
                info_qll.setText(extra_info_str)
                lwi_vbox_3.addWidget(info_qll)
            # Item path
            path_qll = WrapLabel(lwi_widget, -2)
            if show_path_bl:
                path_qll.setText(support_path_str)
                lwi_vbox_3.addWidget(path_qll)

            # ----- Manual calculation of size hint -----
            margins_te = self.item_list_widget.getContentsMargins()
            cb_width_int = checkbox_qcb.sizeHint().width()
            margin_left_int = margins_te[0]
            margin_right_int = margins_te[2]
            # TODO: more horizontal margins here
            # QtGui.QGuiApplication.processEvents()
            list_widget_width_int = self.item_list_widget.width()
            # list_widget_width_int = self.item_list_widget.lineWidth()
            # logging.debug(f"{list_widget_width_int=}")
            scrollbar_width_int = self.style().pixelMetric(QtWidgets.QStyle.PM_ScrollBarExtent)
            horizontal_size_hint_int = (
                list_widget_width_int
                - cb_width_int
                - margin_left_int
                - margin_right_int
                - scrollbar_width_int
            )
            vertical_size_hint_int = name_qll.get_my_size_hint_height(horizontal_size_hint_int)
            if show_info_bl:
                vertical_size_hint_int += info_qll.get_my_size_hint_height(horizontal_size_hint_int)
            if show_path_bl:
                vertical_size_hint_int += path_qll.get_my_size_hint_height(horizontal_size_hint_int)
            vertical_size_hint_int += lwi_hbox_2.contentsMargins().top()
            vertical_size_hint_int += lwi_hbox_2.contentsMargins().bottom()
            vertical_size_hint_int += lwi_vbox_3.contentsMargins().top()
            vertical_size_hint_int += lwi_vbox_3.contentsMargins().bottom()
            manual_size_hint_qsize = QtCore.QSize(horizontal_size_hint_int, vertical_size_hint_int)
            lwi.setSizeHint(manual_size_hint_qsize)
            # -----

            self.item_list_widget.addItem(lwi)  # -important that this is done before setItemWidget
            self.item_list_widget.setItemWidget(lwi, lwi_widget)
            lwi.setData(QtCore.Qt.UserRole, item.get_id())

            if kammanta.glob.testing_bool:
                name_qll.setStyleSheet("QLabel {background-color: #fcf803;}")
                info_qll.setStyleSheet("QLabel {background-color: #fcd703;}")
                path_qll.setStyleSheet("QLabel {background-color: #fcba03;}")
            # if active_list_item is not None and active_list_item.get_id() == item.get_id():
            # active_qlwi = lwi
        self.updating_gui_bool = False


class WrapLabel(QtWidgets.QLabel):
    pressed_signal = QtCore.pyqtSignal()

    def __init__(self, i_parent, i_size_diff: int):
        super().__init__()
        # parent=i_parent

        self.setWordWrap(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, self.sizePolicy().verticalPolicy())

        self.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.setOpenExternalLinks(True)

        new_font = self.font()
        old_font_size_int = new_font.pointSize()
        new_font.setPointSize(old_font_size_int + i_size_diff)
        self.setFont(new_font)

    def get_my_size_hint_height(self, i_width: int) -> int:
        # inspiration: https://stackoverflow.com/questions/36331651/dynamic-text-size-qlabel
        fm = self.fontMetrics()
        text_str = self.text()
        sizehint_width_int = super().width()  # -this gives us a bad result, not sure why. Ex: 169, 172, 128, 23
        label_width_int = i_width
        max_rect = QtCore.QRect(0, 0, label_width_int, 1000)
        br = fm.boundingRect(max_rect, QtCore.Qt.TextWordWrap, text_str)
        font_br_size = br.size()
        # fm_size = fm.size(QtCore.Qt.TextWordWrap, text_str)  # -this doesn't work, unknown why
        font_heigth_int = font_br_size.height()
        total_height_int = font_heigth_int + self.contentsMargins().top() + self.contentsMargins().bottom()
        return total_height_int

    # overridden
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.pressed_signal.emit()
        super().mousePressEvent(ev)
