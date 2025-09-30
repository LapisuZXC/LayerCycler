from krita import DockWidget, Krita, DockWidgetFactory, DockWidgetFactoryBase
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel

DOCKER_NAME = "LayerCycler"
DOCKER_ID = "pykrita_layercycler"
KI = Krita.instance()


class LayerCyclerDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layer Cycler")
        self.doc = None
        self.layers = []
        self.current_idx = None
        self.initUI()

    def initUI(self):
        widget = QWidget(self)
        layout = QGridLayout(self)

        self.lbl = QLabel("Current Layer: None")
        layout.addWidget(self.lbl, 0, 0, 1, 2)

        btn_hide_all_but_top = QPushButton("Hide All but Top")
        btn_hide_all_but_top.clicked.connect(self.hide_all_but_top)
        layout.addWidget(
            btn_hide_all_but_top,
            1,
            0,
        )

        btn_hide_all_but_bottom = QPushButton("Hide All but Bottom")
        btn_hide_all_but_bottom.clicked.connect(self.hide_all_but_bottom)
        layout.addWidget(btn_hide_all_but_bottom, 1, 1)

        btn_up = QPushButton("Move Layer Up")
        btn_up.clicked.connect(self.move_up)
        layout.addWidget(btn_up, 2, 0)

        btn_down = QPushButton("Move Layer Down")
        btn_down.clicked.connect(self.move_down)
        layout.addWidget(btn_down, 2, 1)

        widget.setLayout(layout)
        self.setWidget(widget)

    def update_doc(self):
        self.doc = KI.activeDocument()
        if self.doc:
            self.layers = self.doc.topLevelNodes()

    def hide_all_but_top(self):
        self.update_doc()
        if not self.layers:
            return
        for layer in self.layers:
            layer.setVisible(False)
        self.layers[-1].setVisible(True)  # ???
        self.current_idx = len(self.layers) - 1
        self.layers[0].setVisible(True)
        self.doc.refreshProjection()
        self.update_label()

    def hide_all_but_bottom(self):
        self.update_doc()
        if not self.layers:
            return
        for layer in self.layers:
            layer.setVisible(False)
        self.layers[0].setVisible(True)
        if self.layers[1]:
            self.layers[1].setVisible(True)
        self.current_idx = 1

        self.doc.refreshProjection()
        self.update_label()

    def move_up(self):
        self.update_doc()
        if (
            not self.layers
            or self.current_idx is None
            or self.current_idx == len(self.layers) - 1
        ):
            return
        self.layers[self.current_idx].setVisible(False)
        self.current_idx += 1
        self.layers[self.current_idx].setVisible(True)
        self.doc.refreshProjection()
        self.update_label()

    def move_down(self):
        self.update_doc()
        if not self.layers or self.current_idx is None or self.current_idx == 1:
            return
        self.layers[self.current_idx].setVisible(False)
        self.current_idx -= 1
        self.layers[self.current_idx].setVisible(True)
        self.doc.refreshProjection()
        self.update_label()

    def update_label(self):
        if self.layers and self.current_idx is not None:
            self.lbl.setText(f"Current Layer: {self.layers[self.current_idx].name()}")
        else:
            self.lbl.setText("Current Layer: None")

    def canvasChanged(self, canvas):
        pass


def register_docker():
    dock_widget_factory = DockWidgetFactory(
        "pykrita_layercycler", DockWidgetFactoryBase.DockRight, LayerCyclerDocker
    )

    KI.addDockWidgetFactory(dock_widget_factory)
