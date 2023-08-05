#!/usr/bin/env python3

import argparse
import logging
import logging.handlers
import sys
import os

this_dir_abs_path_str = os.path.dirname(os.path.abspath(__file__))
parent_dir_abs_path_str = os.path.dirname(this_dir_abs_path_str)
# print(f"{this_dir_abs_path_str=}")
print(f"{parent_dir_abs_path_str=}")
# print(f"{sys.path=}")
# sys.path.append(this_dir_abs_path_str)
sys.path.append(parent_dir_abs_path_str)
# -this is done automatically by pycharm (run configurations), but in case we run from a script
# we need to have it here
# Pycharm docs: https://www.jetbrains.com/help/pycharm/configuring-content-roots.html
from kammanta import glob

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--testing", "-t", help="Testing (data saved in memory only)", action="store_true")
# -for info about "store_true" please search here: https://docs.python.org/3/howto/argparse.html
argument_parser.add_argument("--example", "-e", help="Example (data saved in memory only)", action="store_true")
args = argument_parser.parse_args()
glob.testing_bool = False
glob.example_bool = False
if args.testing:
    glob.testing_bool = True
    glob.copy_and_setup_testing()
if args.example:
    glob.example_bool = True
    glob.copy_and_setup_testing()
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import kammanta.gui.main_window


main_window = None


def on_about_to_quit_fired():
    logging.info("Exiting Kammanta application")
    if main_window is not None:
        main_window.before_closing()


def main():
    # Logging
    # Please also see the code in the kammanta.__init__.py module for more info on how we do logging
    logger = logging.getLogger()
    # -if we set a name here for the logger the file handler will no longer work, unknown why
    logger.handlers = []  # -removing the default stream handler first
    # logger.propagate = False
    log_file_path_str = kammanta.glob.get_config_path(kammanta.glob.LOG_FILE_NAME_STR)
    # -TODO: at the moment the config dir is used, do we want to change this to something else?

    # Logging to file
    rfile_handler = logging.handlers.RotatingFileHandler(log_file_path_str, maxBytes=8192, backupCount=2)
    rfile_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    rfile_handler.setFormatter(formatter)
    logger.addHandler(rfile_handler)

    # Logging to stdout
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Handling of (otherwise) uncaught exceptions
    def handle_exception(exc_type, exc_value, exc_traceback):
        logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        """
        if issubclass(exc_type, KeyboardInterrupt):
            sys.excepthook(exc_type, exc_value, exc_traceback)

        if issubclass(exc_type, Exception):
            logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        else:
            sys.excepthook(exc_type, exc_value, exc_traceback)
        """
    sys.excepthook = handle_exception

    logging.info("Starting Kammanta application")

    QtWidgets.QApplication.setDesktopSettingsAware(False)
    application = QtWidgets.QApplication(sys.argv)
    application.setStyle("fusion")

    application.aboutToQuit.connect(on_about_to_quit_fired)
    os.makedirs(kammanta.glob.get_config_path(), exist_ok=True)
    global main_window
    main_window = kammanta.gui.main_window.MyMainWindow()
    application.setQuitOnLastWindowClosed(False)
    main_window.show()
    application.exec_()


if __name__ == "__main__":
    main()

