import os
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QFileDialog, QComboBox,
                             QListWidgetItem, QStatusBar, QProgressBar, QLabel,
                             QApplication, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from styles import get_style, get_icons
from settings_manager import SettingsManager
from utils import get_supported_formats
from conversion_worker import ConversionWorker

ICONS = None

class CustomFileItemWidget(QWidget):
    """
    Custom widget for each item in the file list.
    Includes an icon, file name, format selector, and a remove button.
    """
    remove_requested = pyqtSignal(QListWidgetItem)

    def __init__(self, file_path, supported_formats, parent_item):
        super().__init__()
        self.file_path = file_path
        self.parent_item = parent_item

        # Outer frame for shadow and rounded bg
        frame = QFrame(self)
        frame.setObjectName("FileItemFrame")
        frame.setStyleSheet("""
            QFrame#FileItemFrame {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #2B2D4A, stop:1 #3A1C71);
                border-radius: 16px;
                border: 1.5px solid #5A5CFF;
                box-shadow: 0px 6px 24px rgba(58,28,113,0.18);
                backdrop-filter: blur(8px);
                opacity: 0.98;
                transition: box-shadow 0.3s, border 0.3s;
            }
            QFrame#FileItemFrame:hover {
                border: 2px solid #7F53FF;
                box-shadow: 0px 12px 32px rgba(127,83,255,0.12);
                opacity: 1.0;
            }
        """)
        frame_layout = QHBoxLayout(frame)
        frame_layout.setContentsMargins(16, 10, 16, 10)
        frame_layout.setSpacing(20)
        frame_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # File Icon
        icon_label = QLabel()
        icon_label.setPixmap(self.get_file_icon().pixmap(32, 32))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        icon_label.setStyleSheet("""
            QLabel {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.7, fx:0.5, fy:0.5, stop:0 #7F53FF, stop:1 transparent);
                border-radius: 10px;
                padding: 2px;
            }
        """)
        frame_layout.addWidget(icon_label)

        # File Name
        file_name_label = QLabel(os.path.basename(file_path))
        file_name_label.setToolTip(file_path)
        file_name_label.setMinimumHeight(32)
        file_name_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        file_name_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #E0E6F8;
                font-weight: 600;
                padding-left: 6px;
                letter-spacing: 0.5px;
                text-shadow: 0px 2px 8px rgba(58,28,113,0.12);
            }
        """)
        frame_layout.addWidget(file_name_label, 1)

        # File Type Badge
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        badge = QLabel(ext.upper()[1:] if len(ext) > 1 else "?")
        badge.setStyleSheet("""
            QLabel {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #5A5CFF, stop:1 #7F53FF);
                color: #F5F5F7;
                border-radius: 10px;
                font-size: 13px;
                font-weight: 700;
                padding: 4px 12px;
                margin-right: 10px;
                box-shadow: 0px 2px 8px rgba(127,83,255,0.10);
                border: 1px solid #7F53FF;
            }
        """)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setToolTip(f"File type: {ext}")
        frame_layout.addWidget(badge)

        # Format ComboBox
        self.format_combo = QComboBox()
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        for category, formats in supported_formats.items():
            if ext in formats:
                self.format_combo.addItems(formats[ext])
        self.format_combo.setMinimumHeight(32)
        self.format_combo.setEditable(False)
        self.format_combo.setStyleSheet("""
            QComboBox {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #23242A, stop:1 #5A5CFF);
                color: #E0E6F8;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 600;
                padding: 6px 18px;
                border: 1.5px solid #7F53FF;
                box-shadow: 0px 2px 8px rgba(127,83,255,0.10);
            }
            QComboBox:hover {
                background: #7F53FF;
                color: #F5F5F7;
                border: 2px solid #5A5CFF;
            }
        """)
        self.format_combo.setToolTip("Select output format")
        frame_layout.addWidget(self.format_combo, alignment=Qt.AlignmentFlag.AlignVCenter)

        # Remove Button
        remove_button = QPushButton()
        remove_button.setIcon(ICONS['remove'])
        remove_button.setObjectName("RemoveButton")
        remove_button.setToolTip("Remove this file")
        remove_button.setMinimumHeight(32)
        remove_button.setMaximumWidth(36)
        remove_button.setStyleSheet("""
            QPushButton#RemoveButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #5A5CFF, stop:1 #3A1C71);
                border-radius: 10px;
                color: #F5F5F7;
                font-weight: bold;
                border: 1.5px solid #7F53FF;
                box-shadow: 0px 2px 8px rgba(127,83,255,0.10);
                transition: background 0.3s, color 0.3s;
            }
            QPushButton#RemoveButton:hover {
                background: #7F53FF;
                color: #E0E6F8;
                border: 2px solid #5A5CFF;
            }
        """)
        remove_button.setSizePolicy(remove_button.sizePolicy().horizontalPolicy(), remove_button.sizePolicy().verticalPolicy())
        remove_button.clicked.connect(self.emit_remove_request)
        frame_layout.addWidget(remove_button, alignment=Qt.AlignmentFlag.AlignVCenter)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 6, 0, 6)
        main_layout.addWidget(frame)
        self.setMinimumHeight(64)

    def get_file_icon(self):
        _, ext = os.path.splitext(self.file_path)
        ext = ext.lower()
        if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp']: return ICONS['img']
        if ext in ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.wma', '.m4a']: return ICONS['aud']
        if ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.webm', '.flv', '.mpeg', '.mpg']: return ICONS['vid']
        if ext in ['.docx', '.doc', '.odt', '.rtf']: return ICONS['doc']
        if ext in ['.pdf']: return ICONS['pdf']
        if ext in ['.xlsx', '.xls', '.csv']: return ICONS.get('sheet', ICONS['unknown'])
        if ext in ['.pptx', '.ppt']: return ICONS.get('ppt', ICONS['unknown'])
        if ext in ['.txt', '.py', '.json', '.xml', '.html', '.md', '.log', '.ini', '.yaml', '.yml']: return ICONS.get('text', ICONS['unknown'])
        if ext in ['.zip', '.rar', '.7z', '.tar', '.gz']: return ICONS.get('archive', ICONS['unknown'])
        return ICONS['unknown']

    def emit_remove_request(self):
        self.remove_requested.emit(self.parent_item)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global ICONS
        ICONS = get_icons()  # Now QApplication is running
        self.setWindowTitle("Px-Converter Pro")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet(get_style())
        self.setAcceptDrops(True) # Enable Drag and Drop

        self.settings_manager = SettingsManager()
        self.supported_formats = get_supported_formats()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 10, 20, 20)
        self.layout.setSpacing(15)

        self.setup_ui()
        self.output_directory = self.settings_manager.get('output_directory', os.path.expanduser('~'))
        self.update_output_dir_label()
        self.update_empty_list_label_visibility()

    def setup_ui(self):
        # Header
        title = QLabel("Px-Converter Pro")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel#TitleLabel {
                font-size: 38px;
                font-weight: 900;
                color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #5A5CFF, stop:1 #7F53FF);
                letter-spacing: 2px;
                padding: 18px 0 18px 0;
                text-shadow: 0px 4px 24px rgba(58,28,113,0.18);
                border-radius: 18px;
            }
        """)
        self.layout.addWidget(title)
        
        # File List Area
        list_frame = QFrame()
        list_layout = QVBoxLayout(list_frame)
        list_layout.setContentsMargins(0,0,0,0)
        
        self.file_list_widget = QListWidget()
        self.file_list_widget.itemChanged.connect(self.update_empty_list_label_visibility)
        list_layout.addWidget(self.file_list_widget)

        self.empty_list_label = QLabel("Drag & Drop Files Here or 'Add Files'")
        self.empty_list_label.setObjectName("EmptyListLabel")
        self.empty_list_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        list_layout.addWidget(self.empty_list_label)
        
        self.layout.addWidget(list_frame, 1)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.add_files_button = QPushButton(" Add Files")
        self.add_files_button.setIcon(ICONS['add'])
        self.add_files_button.setObjectName("SecondaryButton")
        self.add_files_button.clicked.connect(self.add_files_dialog)
        self.add_files_button.setMinimumHeight(38)
        self.add_files_button.setStyleSheet("""
            QPushButton#SecondaryButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #23242A, stop:1 #5A5CFF);
                color: #E0E6F8;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 700;
                padding: 8px 24px;
                border: 1.5px solid #7F53FF;
                box-shadow: 0px 2px 8px rgba(127,83,255,0.10);
                transition: background 0.3s, color 0.3s;
            }
            QPushButton#SecondaryButton:hover {
                background: #7F53FF;
                color: #F5F5F7;
                border: 2px solid #5A5CFF;
            }
        """)
        button_layout.addWidget(self.add_files_button)

        self.set_output_dir_button = QPushButton(" Set Output")
        self.set_output_dir_button.setIcon(ICONS['folder'])
        self.set_output_dir_button.setObjectName("SecondaryButton")
        self.set_output_dir_button.clicked.connect(self.set_output_directory)
        self.set_output_dir_button.setMinimumHeight(38)
        self.set_output_dir_button.setStyleSheet(self.add_files_button.styleSheet())
        button_layout.addWidget(self.set_output_dir_button)

        self.clear_all_button = QPushButton(" Clear All")
        self.clear_all_button.setIcon(ICONS['clear'])
        self.clear_all_button.setObjectName("SecondaryButton")
        self.clear_all_button.clicked.connect(self.clear_all_files)
        self.clear_all_button.setMinimumHeight(38)
        self.clear_all_button.setStyleSheet(self.add_files_button.styleSheet())
        button_layout.addWidget(self.clear_all_button)

        button_layout.addStretch()

        self.convert_button = QPushButton(" Convert Files")
        self.convert_button.setIcon(ICONS['convert'])
        self.convert_button.setObjectName("ActionButton")
        self.convert_button.clicked.connect(self.start_conversion)
        self.convert_button.setMinimumHeight(42)
        self.convert_button.setStyleSheet("""
            QPushButton#ActionButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #5A5CFF, stop:1 #7F53FF);
                color: #F5F5F7;
                border-radius: 14px;
                font-size: 18px;
                font-weight: 900;
                padding: 10px 32px;
                border: 2px solid #7F53FF;
                box-shadow: 0px 4px 16px rgba(127,83,255,0.18);
                letter-spacing: 1px;
                transition: background 0.3s, color 0.3s;
            }
            QPushButton#ActionButton:hover {
                background: #23242A;
                color: #7F53FF;
                border: 2.5px solid #5A5CFF;
            }
        """)
        button_layout.addWidget(self.convert_button)
        self.layout.addLayout(button_layout)
        
        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        self.output_dir_label = QLabel()
        self.status_bar.addWidget(self.output_dir_label)

        dev_label = QLabel("Developed by Jeba Seelan")
        self.status_bar.addPermanentWidget(dev_label)

    def process_files(self, file_paths):
        for file_path in file_paths:
            _, ext = os.path.splitext(file_path)
            # Check if extension is supported
            is_supported = any(ext.lower() in formats for formats in self.supported_formats.values())
            if is_supported:
                list_item = QListWidgetItem()
                item_widget = CustomFileItemWidget(file_path, self.supported_formats, list_item)
                item_widget.remove_requested.connect(self.remove_file_item)
                self.file_list_widget.addItem(list_item)
                self.file_list_widget.setItemWidget(list_item, item_widget)
                # Set a fixed height for better stretching and background radius
                list_item.setSizeHint(item_widget.sizeHint())
            else:
                self.status_bar.showMessage(f"Unsupported file type: {os.path.basename(file_path)}", 5000)
        self.update_empty_list_label_visibility()

    def add_files_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files to Convert")
        if files:
            self.process_files(files)

    def remove_file_item(self, item):
        row = self.file_list_widget.row(item)
        self.file_list_widget.takeItem(row)
        self.update_empty_list_label_visibility()

    def clear_all_files(self):
        self.file_list_widget.clear()
        self.update_empty_list_label_visibility()
        
    def set_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory", self.output_directory)
        if directory:
            self.output_directory = directory
            self.settings_manager.set('output_directory', directory)
            self.update_output_dir_label()

    def update_output_dir_label(self):
        self.output_dir_label.setText(f"Output: {self.output_directory}")
        
    def update_empty_list_label_visibility(self):
        is_empty = self.file_list_widget.count() == 0
        self.empty_list_label.setVisible(is_empty)
        # Update QSS for item background radius and border
        if is_empty:
            self.file_list_widget.setStyleSheet("QListWidget { border: 2px dashed #4A4C50; border-radius: 8px; } QListWidget::item { border-radius: 8px; }")
        else:
            self.file_list_widget.setStyleSheet("QListWidget { border: 1px solid #4A4C50; border-radius: 8px; } QListWidget::item { border-radius: 8px; }")

    def start_conversion(self):
        print("Convert button pressed!")
        files_to_convert = []
        for i in range(self.file_list_widget.count()):
            item = self.file_list_widget.item(i)
            widget = self.file_list_widget.itemWidget(item)
            if widget:
                file_path = widget.file_path
                output_format = widget.format_combo.currentText().strip()
                if not output_format:
                    print(f"Skipping {file_path}: No output format selected.")
                    self.status_bar.showMessage(f"No output format selected for {os.path.basename(file_path)}", 5000)
                    continue
                print(f"Queued for conversion: {file_path} -> {output_format}")
                files_to_convert.append((file_path, output_format))

        if files_to_convert:
            print(f"Starting conversion for {len(files_to_convert)} files. Output dir: {self.output_directory}")
            self.convert_button.setEnabled(False)
            self.worker = ConversionWorker(files_to_convert, self.output_directory)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.status.connect(self.status_bar.showMessage)
            self.worker.finished.connect(lambda: self.convert_button.setEnabled(True))
            self.worker.finished.connect(lambda: self.progress_bar.setValue(100))
            self.worker.start()
        else:
            print("No files to convert!")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        file_paths = [url.toLocalFile() for url in urls if url.isLocalFile()]
        self.process_files(file_paths)
