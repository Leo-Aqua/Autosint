from autosint import Plugin
import PySide6.QtWidgets as QtWidgets


class TestPlugin(Plugin):

    def __init__(
        self,
        name="Test Plugin2",
        version="0.0.0",
        input_fields=[1],
        output_fields=[1],
        compatible_plugins=[1],
    ):
        super().__init__(
            name=name,
            version=version,
            input_fields=input_fields,
            output_fields=output_fields,
            compatible_plugins=compatible_plugins,
        )
    
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("This is a custom widget"))
        self.setLayout(layout)

