from PySide6.QtWidgets import QMainWindow


class AoPlugin(QMainWindow):
    plugin_name: str = None
    plugin_icon: str = None

    def __init__(self):
        super().__init__()
