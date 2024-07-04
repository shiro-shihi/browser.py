import sys
import os
import json
import re
from PyQt5.QtCore import Qt, QUrl, QUrlQuery, QFile, QSize, QStandardPaths
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QLabel,
    QProgressBar,
    QAction,
    QDialog,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QDialogButtonBox,
    QMenu,
    QActionGroup,
    QShortcut,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Browser")
        self.setGeometry(100, 100, 1200, 800)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.new_tab_button = QPushButton("+")
        self.new_tab_button.clicked.connect(self.add_new_tab)

        self.back_button = QPushButton("<")
        self.back_button.clicked.connect(self.navigate_back)

        self.forward_button = QPushButton(">")
        self.forward_button.clicked.connect(self.navigate_forward)

        self.reload_button = QPushButton("Reload")
        self.reload_button.clicked.connect(self.reload_page)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(120)
        self.progress_bar.hide()

        self.status_label = QLabel()
        self.status_label.setMinimumWidth(100)

        self.menu_button = QPushButton("Menu")
        self.menu_button.setMenu(self.create_menu())

        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar.addWidget(self.new_tab_button)
        toolbar.addWidget(self.back_button)
        toolbar.addWidget(self.forward_button)
        toolbar.addWidget(self.reload_button)
        toolbar.addWidget(self.url_bar)
        toolbar.addWidget(self.progress_bar)
        toolbar.addWidget(self.status_label)
        toolbar.addWidget(self.menu_button)

        toolbar_widget = QWidget()
        toolbar_widget.setLayout(toolbar)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(toolbar_widget)
        layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.bookmarks = []
        self.history = []

        self.load_history()
        self.load_bookmarks()

        self.create_initial_tab()

        self.setup_shortcuts()

    def setup_shortcuts(self):
        shortcut_new_tab = QShortcut(Qt.CTRL + Qt.Key_T, self)
        shortcut_new_tab.activated.connect(self.add_new_tab)

        shortcut_close_tab = QShortcut(Qt.CTRL + Qt.Key_W, self)
        shortcut_close_tab.activated.connect(self.close_active_tab)

        shortcut_close_all_tabs = QShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_W, self)
        shortcut_close_all_tabs.activated.connect(self.close_all_tabs)

        shortcut_add_bookmark = QShortcut(Qt.CTRL + Qt.Key_B, self)
        shortcut_add_bookmark.activated.connect(self.add_bookmark)

        shortcut_history = QShortcut(Qt.CTRL + Qt.Key_H, self)
        shortcut_history.activated.connect(self.show_history)

    def load_history(self):
        history_file_path = self.get_history_file_path()

        if os.path.exists(history_file_path):
            with open(history_file_path, 'r') as file:
                self.history = json.load(file)

    def save_history(self):
        history_file_path = self.get_history_file_path()

        with open(history_file_path, 'w') as file:
            json.dump(self.history, file)

    def get_history_file_path(self):
        data_dir = QStandardPaths.standardLocations(QStandardPaths.AppDataLocation)[0]
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        return os.path.join(data_dir, 'history.json')

    def create_menu(self):
        menu = QMenu(self)

        bookmark_action = QAction("Bookmarks", self)
        bookmark_action.triggered.connect(self.show_bookmarks)
        menu.addAction(bookmark_action)

        history_action = QAction("History", self)
        history_action.triggered.connect(self.show_history)
        menu.addAction(history_action)

        return menu

    def create_initial_tab(self):
        self.add_new_tab("http://www.google.com")

    def add_new_tab(self, url=""):
        if not url:
            url = "http://www.google.com"
        index = self.tabs.addTab(BrowserTab(self), "New Tab")
        self.tabs.setCurrentIndex(index)
        self.tabs.currentWidget().load_url(url)

    def close_tab(self, index):
        self.tabs.removeTab(index)
        if self.tabs.count() == 0:
            self.close()

    def close_active_tab(self):
        current_index = self.tabs.currentIndex()
        self.tabs.removeTab(current_index)
        if self.tabs.count() == 0:
            self.close()

    def close_all_tabs(self):
        while self.tabs.count() > 0:
            self.tabs.removeTab(0)
        self.close()

    def navigate_back(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.web_view.back()

    def navigate_forward(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.web_view.forward()

    def reload_page(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.web_view.reload()

    def navigate_to_url(self):
        text = self.url_bar.text().strip()
        if self.is_valid_url(text):
            self.tabs.currentWidget().load_url(text)
            self.add_to_history(text)
        elif re.match(r'^[^.]+\.[a-zA-Z]+$', text):
            url = "http://" + text
            self.tabs.currentWidget().load_url(url)
            self.add_to_history(url)
        else:
            query = QUrlQuery()
            query.addQueryItem("q", text)
            url = "https://www.google.com/search?" + query.toString()
            self.tabs.currentWidget().load_url(url)
            self.add_to_history(url)

    def is_valid_url(self, url):
        try:
            result = QUrl(url)
            return result.scheme() and result.isValid()
        except ValueError:
            return False

    def update_status_bar(self, text):
        self.status_label.setText(str(text))

    def update_progress_bar(self, progress):
        if progress < 100:
            self.progress_bar.setValue(progress)
            self.progress_bar.show()
        else:
            self.progress_bar.hide()

    def add_bookmark(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_url = current_tab.web_view.url().toString()
            if current_url not in self.bookmarks:
                self.bookmarks.append(current_url)
                print(f"Bookmark added for {current_url}")
                self.save_bookmarks()

    def save_bookmarks(self):
        bookmarks_file_path = self.get_bookmarks_file_path()

        with open(bookmarks_file_path, 'w') as file:
            json.dump(self.bookmarks, file)

    def load_bookmarks(self):
        bookmarks_file_path = self.get_bookmarks_file_path()

        if os.path.exists(bookmarks_file_path):
            with open(bookmarks_file_path, 'r') as file:
                self.bookmarks = json.load(file)

    def get_bookmarks_file_path(self):
        data_dir = QStandardPaths.standardLocations(QStandardPaths.AppDataLocation)[0]
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        return os.path.join(data_dir, 'bookmarks.json')

    def show_bookmarks(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Bookmarks")
        dialog.setMinimumSize(300, 400)

        layout = QVBoxLayout()

        list_widget = QListWidget()
        list_widget.itemDoubleClicked.connect(self.open_bookmarked_tab)

        for bookmark in self.bookmarks:
            item = QListWidgetItem(bookmark)
            list_widget.addItem(item)

        layout.addWidget(list_widget)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)

        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec_()

    def open_bookmarked_tab(self, item):
        url = item.text()
        self.add_new_tab(url)

    def add_to_history(self, url):
        if url not in self.history:
            self.history.append(url)
            self.save_history()

    def show_history(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("History")
        dialog.setMinimumSize(300, 400)

        layout = QVBoxLayout()

        list_widget = QListWidget()

        for history_item in self.history:
            item = QListWidgetItem(history_item)
            list_widget.addItem(item)

        list_widget.itemDoubleClicked.connect(self.open_history_tab)

        layout.addWidget(list_widget)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)

        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec_()

    def open_history_tab(self, item):
        url = item.text()
        self.add_new_tab(url)

class BrowserTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.web_view = QWebEngineView()
        self.web_view.loadProgress.connect(self.parent().update_progress_bar)
        self.web_view.loadFinished.connect(self.parent().update_status_bar)
        self.layout.addWidget(self.web_view)
        self.setLayout(self.layout)

    def load_url(self, url):
        self.web_view.setUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())
