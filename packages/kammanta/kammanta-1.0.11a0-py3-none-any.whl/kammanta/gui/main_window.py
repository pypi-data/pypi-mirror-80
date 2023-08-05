import shutil
import os
import datetime
import textwrap
import logging
import functools
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import kammanta.model
import kammanta.glob
import kammanta.gui.nas_prjs_tc
import kammanta.gui.inbox_tickler_tc
import kammanta.gui.focus_direction_tc
import kammanta.gui.reference_search_tc
import kammanta.gui.contacts_agendas_tc
import kammanta.shared_timer
import kammanta.widgets.file_list_cw
import kammanta.widgets.md_display_dlg
import kammanta.widgets.processing_wid
import kammanta.widgets.done_wid
import kammanta.gtd_info
import kammanta.widgets.md_input_dlg
import kammanta.widgets.checklist_cw

NOTIFICATION_CHAR_LIMIT_INT = 350


class MyMainWindow(QtWidgets.QMainWindow):
    class ClosableDockWidget(QtWidgets.QDockWidget):
        close_signal = QtCore.pyqtSignal()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.setFeatures(
                QtWidgets.QDockWidget.DockWidgetMovable|
                QtWidgets.QDockWidget.DockWidgetClosable
            )

        def showEvent(self, a0: QtGui.QShowEvent) -> None:
            super().showEvent(a0)

        # overridden
        def closeEvent(self, event: QtGui.QCloseEvent) -> None:
            self.close_signal.emit()
            super().closeEvent(event)

    def __init__(self):
        super().__init__()
        self.updating_gui_bool = True

        self.fnd_dock_dict = {}
        self.left_dock_visible_list = []

        """
        screen_obj = QtGui.QGuiApplication.primaryScreen()
        screen_qrect = screen_obj.availableGeometry()
        width_int = screen_qrect.width()
        """
        self.showMaximized()
        self.setGeometry(10, 10, 1270, 900)
        self.setWindowTitle(kammanta.glob.APPLICATION_TITLE_STR)

        icon_path_str = kammanta.glob.get_icon_path(False)
        self.setWindowIcon(QtGui.QIcon(icon_path_str))

        # Widgets inside tabs

        # self.main_qsw_w0 = QtWidgets.QStackedWidget(self)
        # self.setCentralWidget(self.main_qsw_w0)
        # self.main_qsw_w0.addWidget(self.main_qtw_w1)
        # self.main_qsw_w0.setCurrentWidget(self.main_qtw_w1)

        self.main_qtw_w1 = QtWidgets.QTabWidget(self)
        self.setCentralWidget(self.main_qtw_w1)
        self.main_qtw_w1.currentChanged.connect(self.on_tab_changed)

        self.inbox_tickler = kammanta.gui.inbox_tickler_tc.InboxTicklerMain(self)
        # -TODO: when there is a way to test the memory and reference-loss issue with qt
        #  it would be interesting to try to remove the parent reference here
        self.main_qtw_w1.addTab(self.inbox_tickler, kammanta.gui.inbox_tickler_tc.TITLE_STR)
        self.inbox_tickler.row_clicked_signal.connect(self.on_inbox_row_clicked)

        self.na_prj_w2 = kammanta.gui.nas_prjs_tc.NAsPrjs(self)
        self.main_qtw_w1.addTab(self.na_prj_w2, kammanta.gui.nas_prjs_tc.TITLE_STR)
        self.na_prj_w2.focus_active_signal.connect(self.on_focus_state_changed)

        self.contacts_agendas = kammanta.gui.contacts_agendas_tc.ContactsAgendas(self)
        self.main_qtw_w1.addTab(self.contacts_agendas, kammanta.gui.contacts_agendas_tc.TITLE_STR)

        self.focus_direction = kammanta.gui.focus_direction_tc.FocusDirection(self)
        self.main_qtw_w1.addTab(self.focus_direction, kammanta.gui.focus_direction_tc.TITLE_STR)
        self.focus_direction.aoi_cw4.text_edited_signal.connect(self.on_fnd_text_edited)
        self.focus_direction.goals_cw4.text_edited_signal.connect(self.on_fnd_text_edited)
        self.focus_direction.visions_cw4.text_edited_signal.connect(self.on_fnd_text_edited)
        self.focus_direction.purpose_and_principles_cw4.text_edited_signal.connect(self.on_fnd_text_edited)

        self.reference_search = kammanta.gui.reference_search_tc.ReferenceSearch(self)
        self.main_qtw_w1.addTab(self.reference_search, kammanta.gui.reference_search_tc.TITLE_STR)

        # Corner widgets

        self.ext_holder_widget = QtWidgets.QWidget()
        ext_hbox = QtWidgets.QHBoxLayout()
        self.ext_holder_widget.setLayout(ext_hbox)
        ext_hbox.setContentsMargins(0, 0, 0, 0)
        self.main_qtw_w1.setCornerWidget(self.ext_holder_widget)

        self.ext_email_qpb = QtWidgets.QPushButton("Email")
        ext_hbox.addWidget(self.ext_email_qpb)
        self.ext_email_qpb.clicked.connect(self.open_email_client)
        self.ext_email_qpb.setStyleSheet(kammanta.glob.EXT_BTN_STYLE_SHEET_STR)
        # -using self.ext_email_qpb.setFont() gives a smaller text size
        #  (unknown why, but it may have something to do with the corner widget layout)

        self.ext_cal_qpb = QtWidgets.QPushButton("Calendar")
        ext_hbox.addWidget(self.ext_cal_qpb)
        self.ext_cal_qpb.clicked.connect(self.open_calendar)
        self.ext_cal_qpb.setStyleSheet(kammanta.glob.EXT_BTN_STYLE_SHEET_STR)

        # Dock widgets

        self.search_dock = MyMainWindow.ClosableDockWidget("Search")
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.search_dock)
        self.search_dock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea)
        self.search_container = kammanta.gui.reference_search_tc.SearchDockContainer()
        self.search_dock.setWidget(self.search_container)
        self.search_container.search_clicked_signal.connect(self.on_dock_search)

        self.inbox_dock = MyMainWindow.ClosableDockWidget(kammanta.gui.inbox_tickler_tc.INBOX_TITLE_STR)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.inbox_dock)
        self.inbox_dock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea)
        self.inbox_container = kammanta.gui.inbox_tickler_tc.InboxDock()
        self.inbox_dock.setWidget(self.inbox_container)
        self.inbox_container.row_clicked_signal.connect(self.on_inbox_row_clicked)

        self.processing_dock = QtWidgets.QDockWidget(kammanta.widgets.processing_wid.TITLE_STR)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.processing_dock)
        self.processing_dock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea)
        # self.processing_dock.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
        self.processing_dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.processing_container = kammanta.widgets.processing_wid.ProcessingWidgetInDock()
        self.processing_container.closed_clicked_signal.connect(self.on_processing_closed_clicked)
        self.processing_dock.setWidget(self.processing_container)
        self.processing_dock.hide()

        self.done_dock = QtWidgets.QDockWidget(kammanta.widgets.done_wid.TITLE_STR)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.done_dock)
        self.done_dock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea)
        self.done_dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.done_container = kammanta.widgets.done_wid.DoneWidgetInDock()
        ##### self.done_container.closed_clicked_signal.connect(self.on_processing_closed_clicked)
        self.done_dock.setWidget(self.done_container)
        ######self.done_dock.hide()
        self.done_dock.show()

        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QtWidgets.QTabWidget.North)

        self.main_qtw_w1.setCurrentWidget(self.na_prj_w2)

        # System Tray

        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

        self.tray_menu = QtWidgets.QMenu(self)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_menu.aboutToShow.connect(self.on_about_to_show_menu)

        self.update_tray_icon(False)

        self.time_noaction = QtWidgets.QAction("Error: Time not set")
        self.time_noaction.setEnabled(False)
        self.tray_menu.addAction(self.time_noaction)

        self.tray_menu.addSeparator()

        self.tray_email_action = QtWidgets.QAction("Email")
        self.tray_email_action.triggered.connect(self.open_email_client)
        self.tray_menu.addAction(self.tray_email_action)

        self.tray_calendar_action = QtWidgets.QAction("Calendar")
        self.tray_calendar_action.triggered.connect(self.open_calendar)
        self.tray_menu.addAction(self.tray_calendar_action)

        self.tray_menu.addSeparator()

        self.tray_inbox_and_tickler_action = QtWidgets.QAction(kammanta.gui.inbox_tickler_tc.TITLE_STR)
        self.tray_inbox_and_tickler_action.triggered.connect(self.on_tray_inbox_and_tickler_triggered)
        self.tray_menu.addAction(self.tray_inbox_and_tickler_action)

        self.tray_naprj_action = QtWidgets.QAction(kammanta.gui.nas_prjs_tc.TITLE_STR)
        self.tray_naprj_action.triggered.connect(self.on_tray_na_prj_triggered)
        self.tray_menu.addAction(self.tray_naprj_action)

        self.tray_active_na_noaction = QtWidgets.QAction("Error")
        self.tray_active_na_noaction.setEnabled(False)
        self.tray_menu.addAction(self.tray_active_na_noaction)

        self.tray_ca_action = QtWidgets.QAction(kammanta.gui.contacts_agendas_tc.TITLE_STR)
        self.tray_ca_action.triggered.connect(self.on_tray_ca_triggered)
        self.tray_menu.addAction(self.tray_ca_action)

        self.tray_fd_action = QtWidgets.QAction(kammanta.gui.focus_direction_tc.TITLE_STR)
        self.tray_fd_action.triggered.connect(self.on_tray_fd_triggered)
        self.tray_menu.addAction(self.tray_fd_action)

        self.tray_rs_action = QtWidgets.QAction(kammanta.gui.reference_search_tc.TITLE_STR)
        self.tray_rs_action.triggered.connect(self.on_tray_rs_triggered)
        self.tray_menu.addAction(self.tray_rs_action)

        self.tray_menu.addSeparator()

        self.tray_paste_to_note_action = QtWidgets.QAction("Paste clipboard into new note")
        self.tray_paste_to_note_action.triggered.connect(self.on_paste_to_note_triggered)
        self.tray_menu.addAction(self.tray_paste_to_note_action)

        self.tray_take_note_action = QtWidgets.QAction("Create New Note")
        self.tray_take_note_action.triggered.connect(self.on_take_note_triggered)
        self.tray_menu.addAction(self.tray_take_note_action)

        self.tray_menu.addSeparator()

        self.tray_restore_action = QtWidgets.QAction("Restore")
        self.tray_restore_action.triggered.connect(self.on_tray_restore_triggered)
        self.tray_menu.addAction(self.tray_restore_action)

        self.tray_exit_action = QtWidgets.QAction("Exit")
        self.tray_exit_action.triggered.connect(QtWidgets.QApplication.quit)
        self.tray_menu.addAction(self.tray_exit_action)

        # Creating the main menu bar..

        # ..setup of actions

        change_main_dir_qaction = QtWidgets.QAction("Change user data directory", self)
        change_main_dir_qaction.triggered.connect(self.change_user_files_dir)
        change_ref_dir_qaction = QtWidgets.QAction("Change reference directory", self)
        change_ref_dir_qaction.triggered.connect(self.change_ref_files_dir)

        change_external_calendar_qaction = QtWidgets.QAction("Change external calendar", self)
        change_external_calendar_qaction.triggered.connect(self.on_change_external_calendar_triggered)
        change_external_email_client_qaction = QtWidgets.QAction("Change external email client", self)
        change_external_email_client_qaction.triggered.connect(self.on_change_external_email_client_triggered)

        open_trash_qaction = QtWidgets.QAction("Open trash directory", self)
        open_trash_qaction.triggered.connect(self.on_show_trash_triggered)
        clear_trash_qaction = QtWidgets.QAction("Clear trash directory", self)
        clear_trash_qaction.triggered.connect(self.on_clear_trash_triggered)

        dark_mode_qaction = QtWidgets.QAction("Dark mode", self)
        dark_mode_qaction.setCheckable(True)
        dark_mode_qaction.toggled.connect(self.on_dark_mode_toggled)
        dark_mode_qaction.setChecked(True)

        exit_qaction = QtWidgets.QAction("Exit", self)
        exit_qaction.triggered.connect(QtWidgets.QApplication.quit)

        backup_qaction = QtWidgets.QAction("Backup", self)
        backup_qaction.triggered.connect(self.backup_main_dir)

        interactive_info_qaction = QtWidgets.QAction("GTD interactive (p n c) info", self)
        interactive_info_qaction.triggered.connect(self.on_interactive_gtd_info_triggered)
        info_guide_qaction = QtWidgets.QAction("GTD help guide", self)
        info_guide_qaction.triggered.connect(self.on_gtd_info_guide_triggered)

        open_main_dir_qaction = QtWidgets.QAction("Open main dir", self)
        open_main_dir_qaction.triggered.connect(self.on_open_main_dir_triggered)
        open_ref_dir_qaction = QtWidgets.QAction("Open reference dir", self)
        open_ref_dir_qaction.triggered.connect(self.on_open_ref_dir_triggered)
        open_config_dir_qaction = QtWidgets.QAction("Open config dir", self)
        open_config_dir_qaction.triggered.connect(self.on_open_config_dir_triggered)

        redraw_qaction = QtWidgets.QAction("Redraw GUI", self)
        redraw_qaction.triggered.connect(self.on_redraw_gui_triggered)

        gc_qaction = QtWidgets.QAction("Python Garbage Collection", self)
        gc_qaction.triggered.connect(self.on_gc_triggered)

        print_fsw_info_qaction = QtWidgets.QAction("Print FileSystemWatcher info", self)
        print_fsw_info_qaction.triggered.connect(self.on_print_fsw_info_triggered)

        open_log_qaction = QtWidgets.QAction("Open log file", self)
        open_log_qaction.triggered.connect(self.on_open_log_triggered)

        self.show_inbox_dock_qaction = QtWidgets.QAction("Show Inbox Dock", self)
        self.show_inbox_dock_qaction.setCheckable(True)
        self.show_inbox_dock_qaction.triggered.connect(functools.partial(self.inbox_dock.setVisible))
        self.show_inbox_dock_qaction.setChecked(True)
        self.inbox_dock.close_signal.connect(functools.partial(self.show_inbox_dock_qaction.setChecked, False))

        self.show_search_dock_qaction = QtWidgets.QAction("Show Search Dock", self)
        self.show_search_dock_qaction.setCheckable(True)
        self.show_search_dock_qaction.triggered.connect(functools.partial(self.search_dock.setVisible))
        self.show_search_dock_qaction.setChecked(True)
        self.search_dock.close_signal.connect(functools.partial(self.show_search_dock_qaction.setChecked, False))

        # ..adding the menus
        self.menu_bar = self.menuBar()
        application_menu = self.menu_bar.addMenu("&Application")
        application_menu.addAction(backup_qaction)
        application_menu.addAction(dark_mode_qaction)
        application_menu.addAction(exit_qaction)

        directories_menu = self.menu_bar.addMenu("&Directories")
        directories_menu.addAction(open_main_dir_qaction)
        directories_menu.addAction(change_main_dir_qaction)
        directories_menu.addSeparator()
        directories_menu.addAction(open_ref_dir_qaction)
        directories_menu.addAction(change_ref_dir_qaction)
        directories_menu.addSeparator()
        directories_menu.addAction(open_config_dir_qaction)
        directories_menu.addSeparator()
        directories_menu.addAction(open_trash_qaction)
        directories_menu.addAction(clear_trash_qaction)

        external_tools_menu = self.menu_bar.addMenu("&External")
        external_tools_menu.addAction(change_external_calendar_qaction)
        external_tools_menu.addAction(change_external_email_client_qaction)

        self.windows_menu = self.menu_bar.addMenu("&Windows")
        self.windows_menu.addAction(self.show_inbox_dock_qaction)
        self.windows_menu.addAction(self.show_search_dock_qaction)
        self.windows_menu.addSeparator()
        self.add_fnd_action(kammanta.model.aoi_obj)
        self.add_fnd_action(kammanta.model.go_obj)
        self.add_fnd_action(kammanta.model.vision_obj)
        self.add_fnd_action(kammanta.model.pp_obj)

        debug_menu = self.menu_bar.addMenu("&Debug")
        debug_menu.addAction(redraw_qaction)
        debug_menu.addAction(gc_qaction)
        debug_menu.addAction(print_fsw_info_qaction)
        debug_menu.addAction(open_log_qaction)

        help_menu = self.menu_bar.addMenu("&Help")
        help_menu.addAction(interactive_info_qaction)
        help_menu.addAction(info_guide_qaction)

        self.updating_gui_bool = False

        fsw = kammanta.glob.FswSingleton.get()
        fsw.directoryChanged.connect(self.on_file_or_dir_changed)
        fsw.fileChanged.connect(self.on_file_or_dir_changed)

        self.minute_timer = kammanta.shared_timer.SharedMinuteTimer()
        self.minute_timer.tickler_notification_signal.connect(self.on_timer_tickler_update_triggered)
        self.minute_timer.clock_signal.connect(self.on_clock_signal_triggered)
        self.minute_timer.start()

        self.light_qp = QtGui.QPalette()

        self.dark_qp = QtGui.QPalette()
        green_qcolor = QtGui.QColor(0, 128, 0)
        darkgray_qcolor = QtGui.QColor(64, 64, 64)
        black_qcolor = QtGui.QColor(32, 32, 32)
        white_qcolor = QtGui.QColor(250, 250, 250)
        yellow_qcolor = QtGui.QColor(200, 200, 0)
        almostblack_qcolor = QtGui.QColor(32, 32, 32)
        self.dark_qp.setColor(QtGui.QPalette.Window, darkgray_qcolor)
        self.dark_qp.setColor(QtGui.QPalette.WindowText, white_qcolor)
        self.dark_qp.setColor(QtGui.QPalette.Base, black_qcolor)
        self.dark_qp.setColor(QtGui.QPalette.AlternateBase, darkgray_qcolor)
        self.dark_qp.setColor(QtGui.QPalette.ToolTipBase, black_qcolor)
        self.dark_qp.setColor(QtGui.QPalette.ToolTipText, white_qcolor)
        self.dark_qp.setColor(QtGui.QPalette.Text, white_qcolor)
        self.dark_qp.setColor(QtGui.QPalette.Button, darkgray_qcolor)
        self.dark_qp.setColor(QtGui.QPalette.ButtonText, white_qcolor)
        self.dark_qp.setColor(QtGui.QPalette.BrightText, yellow_qcolor)
        self.dark_qp.setColor(QtGui.QPalette.Highlight, green_qcolor)
        # dark_qp.setColor(QtGui.QPalette.Link, yellow_qcolor)
        # dark_qp.setColor(QtGui.QPalette.Highlight, yellow_qcolor)
        # dark_qp.setColor(QtGui.QPalette.HighlightedText, yellow_qcolor)
        QtGui.QGuiApplication.setPalette(self.dark_qp)


        self.show()
        self.update_gui()
        self._restore_dock_state()

    def on_dark_mode_toggled(self, i_checked: bool):
        if i_checked:
            QtGui.QGuiApplication.setPalette(self.dark_qp)
        else:
            QtGui.QGuiApplication.setPalette(self.light_qp)

    def on_open_log_triggered(self):
        log_path_str = kammanta.glob.get_config_path(kammanta.glob.LOG_FILE_NAME_STR)
        with open(log_path_str, "r") as file:
            contents_str = file.read()
            QtWidgets.QMessageBox.information(self, "Log file", contents_str)
        # kammanta.glob.launch_string(log_path_str)

    def before_closing(self):
        for fnd_dock in self.fnd_dock_dict.values():
            self._save_dock_state(fnd_dock)

    def _save_dock_state(self, dock_widget: QtWidgets.QDockWidget):
        title_str = dock_widget.windowTitle()
        state_bool = dock_widget.isVisible()
        state_str = "false"
        if state_bool:
            state_str = "true"
        kammanta.glob.add_string_to_config(
            kammanta.glob.SETTINGS_SECTION_DOCKS_STR, title_str, state_str
        )

    def _restore_dock_state(self):
        for fnd_dock in self.fnd_dock_dict.values():
            title_str = fnd_dock.windowTitle()
            status_bool = kammanta.glob.get_boolean_from_config(
                kammanta.glob.SETTINGS_SECTION_DOCKS_STR, title_str, True
            )
            if not status_bool:
                fnd_dock.close()

    def on_clock_signal_triggered(self):
        self.update_tray_tooltip()

    def on_timer_tickler_update_triggered(self, i_string: str):
        self.tray_icon.showMessage("Tickler item moved to inbox", i_string)
        self.inbox_tickler.update_gui()
        self.inbox_container.update_gui()

    def on_focus_state_changed(self, i_status: bool):
        # -focus here is the focus dialog that the user can start for an NA or project
        self.update_tray_icon(i_status)
        self.update_tray_tooltip()

    def update_tray_icon(self, i_focus: bool):
        icon_path_str = kammanta.glob.get_icon_path(i_focus)
        pixmap = QtGui.QPixmap(icon_path_str)
        new_icon = QtGui.QIcon(pixmap)
        self.tray_icon.setIcon(new_icon)

    def update_tray_tooltip(self):
        now_pydt = datetime.datetime.now()
        now_pydt += datetime.timedelta(minutes=1)
        # -better to be a bit early rather than late
        now_str = now_pydt.strftime("%H:%M")

        systray_hover_text_str = f"{kammanta.glob.APPLICATION_TITLE_STR}, {now_str}"
        if kammanta.widgets.checklist_cw.ChecklistWidget.active_focus_dlg:
            focus_item = kammanta.widgets.checklist_cw.ChecklistWidget.active_focus_dlg.focus_item_ref
            focus_name_str = focus_item.get_core_name()
            systray_hover_text_str = f"{kammanta.glob.APPLICATION_TITLE_STR}, {now_str}, --- {focus_name_str}"

        self.tray_icon.setToolTip(systray_hover_text_str)
        # -Please note: tray_icon (not tray_menu)

    def on_about_to_show_menu(self):
        now_pydt = datetime.datetime.now()
        now_pydt_str = now_pydt.strftime("%c")
        self.time_noaction.setText(now_pydt_str)

        active_na_item = kammanta.model.na_files.get_active_item()
        active_na_item_name_str = active_na_item.get_core_name()
        self.tray_active_na_noaction.setText(f"Active NA context: {active_na_item_name_str}")

        # TODO: Same with projects?

    def on_tray_activated(self, i_reason: QtWidgets.QSystemTrayIcon.ActivationReason):
        logging.debug(f"on_tray_activated, {i_reason=}")
        if i_reason == QtWidgets.QSystemTrayIcon.Trigger:
            self._restore()
            if kammanta.widgets.checklist_cw.ChecklistWidget.active_focus_dlg is not None:
                kammanta.widgets.checklist_cw.ChecklistWidget.active_focus_dlg.restore_and_activate()

    def on_print_fsw_info_triggered(self):
        fsw = kammanta.glob.FswSingleton.get()
        nr_dirs_int = len(fsw.directories())
        nr_files_int = len(fsw.files())
        logging.info(f"===== FileSystemWatcher =====")
        logging.info(f"{nr_dirs_int=}")
        logging.info(f"{nr_files_int=}")
        logging.info("=====")

    def add_fnd_action(self, i_fnd_obj: kammanta.model.TextFile):
        title_str = i_fnd_obj.get_main_title()

        self.fnd_dock_dict[title_str] = MyMainWindow.ClosableDockWidget(title_str)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.fnd_dock_dict[title_str])
        self.fnd_dock_dict[title_str].setAllowedAreas(
            QtCore.Qt.RightDockWidgetArea |
            QtCore.Qt.LeftDockWidgetArea
        )
        self.fnd_dock_dict[title_str].setFeatures(
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetClosable
        )
        fnd_container = kammanta.gui.focus_direction_tc.FDArea(i_fnd_obj, True)
        self.fnd_dock_dict[title_str].setWidget(fnd_container)

        fnd_action = QtWidgets.QAction("Show " + title_str, self)
        fnd_action.setCheckable(True)
        fnd_action.triggered.connect(
            functools.partial(self.fnd_dock_dict[title_str].setVisible)
        )
        fnd_action.setChecked(True)
        self.windows_menu.addAction(fnd_action)

        self.fnd_dock_dict[title_str].close_signal.connect(
            functools.partial(fnd_action.setChecked, False)
        )

        # Alt: Using a custom title bar widget, see example code below
        """
        title_bar_widget = QtWidgets.QWidget()
        tb_hbox = QtWidgets.QHBoxLayout()
        title_bar_widget.setLayout(tb_hbox)
        tb_hbox.addWidget(QtWidgets.QLabel(title_str))
        tb_hbox.addStretch(1)
        edit_qpb = QtWidgets.QPushButton("edit")
        edit_qpb.clicked.connect(functools.partial(self.on_fnd_edit_clicked, i_fnd_obj))
        tb_hbox.addWidget(edit_qpb)
        self.fnd_dock_dict[title_str].setTitleBarWidget(title_bar_widget)
        # -docs: https://doc.qt.io/qt-5/qdockwidget.html#setTitleBarWidget

        self.fnd_dock_dict[title_str].setContentsMargins(0, 0, 0, 0)
        # self.fnd_container_dict[title_str].setContentsMargins(0, 0, 0, 0)
        title_bar_widget.setContentsMargins(0, 0, 0, 0)
        tb_hbox.setContentsMargins(0, 0, 0, 0)
        edit_qpb.setContentsMargins(0, 0, 0, 0)
        """

    def on_fnd_edit_clicked(self, i_fnd_obj: kammanta.model.TextFile):
        logging.debug("on_fnd_edit_clicked")

        (new_text_str, okay_bool) = kammanta.widgets.md_input_dlg.MarkdownInputDialog.open_dlg_and_get_text(
                i_fnd_obj.get_path())
        if okay_bool:
            with open(i_fnd_obj.get_path(), "w") as file:
                file.write(new_text_str)
            # self.text_edited_signal.emit()
            # -doesn't seem to be needed here, even if we have the Focus/Direction tab open
            i_fnd_obj.set_text_contents(new_text_str)
        self.update_gui()

    def on_inbox_dock_closed(self):
        # self.updating_gui_bool = True
        self.show_inbox_dock_qaction.setChecked(False)
        # self.updating_gui_bool = False

    def close_all_open_in_left_dock(self):
        self.left_dock_visible_list.clear()
        if self.inbox_dock.isVisible():
            self.inbox_dock.hide()
            self.left_dock_visible_list.append(self.inbox_dock)
        if self.search_dock.isVisible():
            self.search_dock.hide()
            self.left_dock_visible_list.append(self.search_dock)

    def reopen_closed_in_left_dock(self):
        for dock in self.left_dock_visible_list:
            dock.show()

    def on_processing_closed_clicked(self):
        self.processing_dock.hide()
        self.reopen_closed_in_left_dock()

    def on_dock_search(self, is_file_search: bool, search_text: str):
        self.main_qtw_w1.setCurrentWidget(self.reference_search)
        if is_file_search:
            self.reference_search.file_name_search_qrb.click()
        else:
            self.reference_search.text_search_qrb.click()
        self.reference_search.search_qle.setText(search_text)
        self.reference_search.search_qpb.click()

    def on_inbox_row_clicked(self, i_id: str):
        #####self.main_qsw_w0.setCurrentWidget(self.processing)
        # gtd.model.inbox_dir.get_item()

        inbox_item_obj = kammanta.model.inbox_dir.get_item(i_id)
        source_path_str = inbox_item_obj.get_path()
        self.processing_container.set_source_path(source_path_str)

        # self.processing_dlg.set_source_path(source_path_str)
        # self.processing_dlg.show()
        self.close_all_open_in_left_dock()
        self.processing_dock.show()

    def on_show_trash_triggered(self):
        trash_dir_path_str = kammanta.glob.get_path(kammanta.glob.TRASH_DIR_STR)
        kammanta.glob.launch_string(trash_dir_path_str)

    def on_clear_trash_triggered(self):
        code_for_button_clicked_int = QtWidgets.QMessageBox.question(
            self, "Clear the trash?", "Are you sure you want to clear the trash?",
            defaultButton=QtWidgets.QMessageBox.No
        )
        if code_for_button_clicked_int == QtWidgets.QMessageBox.Yes:
            kammanta.glob.clear_trash()

    def on_interactive_gtd_info_triggered(self):
        QtWidgets.QWhatsThis.enterWhatsThisMode()

    def on_gtd_info_guide_triggered(self):
        guide_text_str = kammanta.gtd_info.get_guide_text()
        kammanta.widgets.md_display_dlg.MarkdownDisplayDialog.open_dlg("GTD Info Guide", guide_text_str)

    def open_calendar(self):
        calendar_str = kammanta.glob.get_string_from_config(
            kammanta.glob.SETTINGS_SECTION_EXTERNAL_TOOLS_STR,
            kammanta.glob.SETTINGS_CALENDAR_STR,
            "https://calendar.google.com/calendar/r/week"
        )
        kammanta.glob.launch_string(calendar_str)

    def open_email_client(self):
        email_str = kammanta.glob.get_string_from_config(
            kammanta.glob.SETTINGS_SECTION_EXTERNAL_TOOLS_STR,
            kammanta.glob.SETTINGS_EMAIL_STR,
            "thunderbird"
        )
        if kammanta.glob.is_valid_command(email_str):
            kammanta.glob.launch_string(email_str)

    def on_redraw_gui_triggered(self):
        self.update_gui()

    def on_gc_triggered(self):
        kammanta.glob.do_garbage_collection()

    def on_fnd_text_edited(self):
        self.update_gui()

    def on_open_main_dir_triggered(self):
        path_str = kammanta.glob.get_path()
        kammanta.glob.launch_string(path_str)

    def on_open_ref_dir_triggered(self):
        path_str = kammanta.glob.get_ref_path()
        kammanta.glob.launch_string(path_str)

    def on_open_config_dir_triggered(self):
        path_str = kammanta.glob.get_config_path()
        kammanta.glob.launch_string(path_str)

    def on_open_contacts_dir_triggered(self):
        path_str = kammanta.glob.get_path(kammanta.glob.CONTACTS_DIR_STR)
        kammanta.glob.launch_string(path_str)

    def on_tray_restore_triggered(self):
        self._restore()

    def _restore(self):
        self.show()
        self.raise_()
        if self.isMaximized():
            self.showMaximized()
        else:
            self.showNormal()

    def on_take_note_triggered(self):
        # noinspection PyTypeChecker
        (text_str, okay_bool) = QtWidgets.QInputDialog.getMultiLineText(
            None, "Title Text", "Help text"
        )
        # -parent is set to none to avoid switching to the main window in case there is another
        #  GUI application running in the foreground. (This is only a problem when MyGTD is running
        #  "normalized")
        if okay_bool:
            new_note_name_str = kammanta.glob.get_new_note_name()
            kammanta.model.inbox_dir.add_new_item(new_note_name_str)
            item_obj = kammanta.model.inbox_dir.get_item(new_note_name_str)
            item_obj.set_text_contents(text_str)

            # gtd.model.inbox_dir.add_note(text_str)

            text_shortened_str = textwrap.shorten(text_str, width=NOTIFICATION_CHAR_LIMIT_INT)
            self.tray_icon.showMessage("MyGTD - New note created", text_shortened_str)

        self.inbox_container.update_gui()
        self.inbox_tickler.update_gui()

    def on_paste_to_note_triggered(self):
        qt_clipboard = QtGui.QGuiApplication.clipboard()
        text_from_system_clipboard_str = qt_clipboard.text()

        if text_from_system_clipboard_str:
            # gtd.model.inbox_dir.add_note(text_from_system_clipboard_str)

            new_note_name_str = kammanta.glob.get_new_note_name()
            kammanta.model.inbox_dir.add_new_item(new_note_name_str)
            item_obj = kammanta.model.inbox_dir.get_item(new_note_name_str)
            item_obj.set_text_contents(text_from_system_clipboard_str)

            text_shortened_str = textwrap.shorten(text_from_system_clipboard_str, width=NOTIFICATION_CHAR_LIMIT_INT)
            self.tray_icon.showMessage("MyGTD - Clipboard pasted into new note", text_shortened_str)
        else:
            pass  # -clipboard is empty

        self.inbox_container.update_gui()
        self.inbox_tickler.update_gui()

    def on_tray_inbox_and_tickler_triggered(self):
        self.show()
        self.main_qtw_w1.setCurrentWidget(self.inbox_tickler)

    def on_tray_na_prj_triggered(self):
        self.show()
        self.main_qtw_w1.setCurrentWidget(self.na_prj_w2)

    def on_tray_fd_triggered(self):
        self.show()
        self.main_qtw_w1.setCurrentWidget(self.focus_direction)

    def on_tray_ca_triggered(self):
        # self.raise_()
        # self.show()
        # self.setVisible(True)
        self.showMaximized()
        self.main_qtw_w1.setCurrentWidget(self.contacts_agendas)

    def on_tray_rs_triggered(self):
        self.show()
        self.main_qtw_w1.setCurrentWidget(self.reference_search)

    def on_tab_changed(self, i_index: str):
        pass
        """
        widget = self.main_qtw_w1.currentWidget()
        # noinspection PyUnresolvedReferences
        widget.update_gui()  # -duck typing
        """

    def change_ref_files_dir(self):
        home_dir = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.HomeLocation)[0]
        new_dir_str = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Choose dir", home_dir, QtWidgets.QFileDialog.ShowDirsOnly
        )
        if not new_dir_str:
            return
        logging.debug(f"New ref directory: {new_dir_str}")
        kammanta.glob.add_string_to_config(
            kammanta.glob.SETTINGS_SECTION_GENERAL_STR, kammanta.glob.SETTINGS_REFERENCE_DIR_STR, new_dir_str
        )
        self.update_gui()

    def change_user_files_dir(self):
        home_dir = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.HomeLocation)[0]
        new_dir_str = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Choose dir", home_dir, QtWidgets.QFileDialog.ShowDirsOnly
        )
        if not new_dir_str:
            return
        logging.debug(f"New user directory: {new_dir_str}")
        kammanta.glob.add_string_to_config(
            kammanta.glob.SETTINGS_SECTION_GENERAL_STR, kammanta.glob.SETTINGS_BASE_DIR_STR, new_dir_str
        )
        self.update_gui()

    def on_change_external_calendar_triggered(self):
        old_calendar_str = kammanta.glob.get_string_from_config(
            kammanta.glob.SETTINGS_SECTION_EXTERNAL_TOOLS_STR, kammanta.glob.SETTINGS_CALENDAR_STR, ""
        )
        if not old_calendar_str:
            return
        (new_calendar_str, result_bool) = QtWidgets.QInputDialog.getText(self, "Title", "Label", text=old_calendar_str)
        if result_bool:
            kammanta.glob.add_string_to_config(
                kammanta.glob.SETTINGS_SECTION_EXTERNAL_TOOLS_STR,
                kammanta.glob.SETTINGS_CALENDAR_STR,
                new_calendar_str
            )

    def on_change_external_email_client_triggered(self):
        old_email_client_str = kammanta.glob.get_string_from_config(
            kammanta.glob.SETTINGS_SECTION_EXTERNAL_TOOLS_STR, kammanta.glob.SETTINGS_EMAIL_STR, ""
        )
        if not old_email_client_str:
            return
        (new_email_client_str, result_bool) = QtWidgets.QInputDialog.getText(self, "Title", "Label", text=old_email_client_str)
        if result_bool:
            kammanta.glob.add_string_to_config(
                kammanta.glob.SETTINGS_SECTION_EXTERNAL_TOOLS_STR,
                kammanta.glob.SETTINGS_EMAIL_STR,
                new_email_client_str
            )

    def on_file_or_dir_changed(self, i_path: str):
        logging.debug("on_file_or_dir_changed, i_path = " + i_path)
        ##### fsw = kammanta.glob.FswSingleton.get()
        self.update_gui()

    def update_gui(self):
        logging.debug("Running update_gui in main_window")
        # -please note that when testing with real files that are written this function will
        # be called many times from on_file_or_dir_changed

        QtGui.QGuiApplication.processEvents()
        # -this call is important!

        self.updating_gui_bool = True

        """
        # for file_path_str in filesystemwatcher.files():
        fsw = gtd.gtd_global.get_filesyswatcher()
        file_path_list = fsw.files()
        if len(file_path_list) > 0:
            fsw.removePaths(file_path_list)
        dir_path_list = fsw.directories()
        if len(dir_path_list) > 0:
            fsw.removePaths(dir_path_list)
        """

        # Dock widgets
        for fnd_dock in self.fnd_dock_dict.values():
            if fnd_dock.isVisible():
                fnd_dock.widget().update_gui()
        if self.inbox_dock.isVisible():
            self.inbox_container.update_gui()
            nr_of_all_items_int = len(kammanta.model.inbox_dir.get_all_items())
            inbox_title_str = f"Inbox ({nr_of_all_items_int} items)"
            self.inbox_dock.setWindowTitle(inbox_title_str)
        self.done_container.update_gui()

        # Tab widgets
        # noinspection PyUnresolvedReferences
        self.main_qtw_w1.currentWidget().update_gui()  # -duck typing

        self.updating_gui_bool = False

    def backup_main_dir(self):
        date_str = datetime.datetime.now().strftime(kammanta.glob.QT_DATETIME_FORMAT_STR)
        file_name_str = "backup_" + date_str + ".tar.gz"
        (dest_str, files_okay) = QtWidgets.QFileDialog.getSaveFileName(
            self, "Please select destination", file_name_str
        )
        if files_okay:
            dest_str = os.path.join(dest_str, "")
            shutil.make_archive(dest_str, "gztar", kammanta.glob.create_and_get_path())
        # file_size_in_bytes_int = os.path.getsize(new_file_path_str)
        # return file_size_in_bytes_int

