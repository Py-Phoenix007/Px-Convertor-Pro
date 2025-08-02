import qtawesome as qta

def get_style():
    """
    Returns the QSS stylesheet for the application.
    """
    return """
    QWidget {
        background-color: #2B2D30; /* A darker, softer black */
        color: #EAEAEA;
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        font-size: 15px;
    }
    QMainWindow {
        border: 1px solid #1E1F22;
    }
    /* Title Label */
    #TitleLabel {
        font-size: 28px;
        font-weight: bold;
        padding: 10px;
        color: #FFFFFF;
    }
    /* Empty List Label */
    #EmptyListLabel {
        color: #7A7C80;
        font-size: 20px;
        font-style: italic;
    }
    QListWidget {
        background-color: #212325;
        border: 2px dashed #4A4C50; /* Dashed border for drop area */
        border-radius: 8px;
        padding: 10px;
    }
    QListWidget::item {
        background-color: #2B2D30;
        border: 1px solid #3A3C40;
        border-radius: 5px;
        padding: 5px;
        margin-bottom: 5px;
    }
    QListWidget::item:hover {
        background-color: #3A3C40;
    }
    QListWidget::item:selected {
        background-color: #0078D4;
        border: 1px solid #005A9E;
        color: #FFFFFF;
    }
    /* Main Action Buttons */
    QPushButton#ActionButton {
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0078D4, stop:1 #005A9E);
        color: #FFFFFF;
        border: none;
        padding: 12px 24px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 16px;
    }
    QPushButton#ActionButton:hover {
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0084E8, stop:1 #0066B8);
    }
    QPushButton#ActionButton:pressed {
        background-color: #005A9E;
    }
    /* Secondary Buttons */
    QPushButton#SecondaryButton {
        background-color: #4A4C50;
        color: #EAEAEA;
        border: 1px solid #5A5C60;
        padding: 10px 20px;
        border-radius: 6px;
    }
    QPushButton#SecondaryButton:hover {
        background-color: #5A5C60;
        border-color: #6A6C70;
    }
    QPushButton#SecondaryButton:pressed {
        background-color: #3A3C40;
    }
    /* Remove Button inside list item */
    QPushButton#RemoveButton {
        background-color: transparent;
        border: none;
        padding: 5px;
        border-radius: 4px;
    }
    QPushButton#RemoveButton:hover {
        background-color: #E81123;
    }
    QComboBox {
        background-color: #3A3C40;
        border: 1px solid #5A5C60;
        border-radius: 5px;
        padding: 8px;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px;
        border-left: 1px solid #5A5C60;
    }
    QComboBox QAbstractItemView {
        background-color: #3A3C40;
        border: 1px solid #5A5C60;
        selection-background-color: #0078D4;
        padding: 5px;
    }
    QStatusBar {
        background-color: #1E1F22;
        color: #A0A0A0;
        font-size: 13px;
    }
    QProgressBar {
        border: 1px solid #4A4C50;
        border-radius: 5px;
        text-align: center;
        background-color: #3A3C40;
        color: #EAEAEA;
    }
    QProgressBar::chunk {
        background-color: #0078D4;
        border-radius: 4px;
    }
    """

# Icon definitions
def get_icons():
    """
    Returns a dictionary of icons used in the application.
    """
    # Only create icons when called, after QApplication is running
    return {
        "add": qta.icon('fa5s.plus-circle', color='#FFFFFF'),
        "folder": qta.icon('fa5s.folder-open', color='#FFFFFF'),
        "convert": qta.icon('fa5s.cogs', color='#FFFFFF'),
        "clear": qta.icon('fa5s.trash-alt', color='#EAEAEA'),
        "remove": qta.icon('fa5s.times-circle', color='#EAEAEA'),
        "doc": qta.icon('fa5s.file-word', color='#2B579A'),
        "img": qta.icon('fa5s.file-image', color='#4B8A08'),
        "aud": qta.icon('fa5s.file-audio', color='#C33B18'),
        "vid": qta.icon('fa5s.file-video', color='#5B2C6F'),
        "pdf": qta.icon('fa5s.file-pdf', color='#B30B00'),
        "text": qta.icon('fa5s.file-alt', color='#A0A0A0'),
        "unknown": qta.icon('fa5s.file', color='#CCCCCC')
    }
