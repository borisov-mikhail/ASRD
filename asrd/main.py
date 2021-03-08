import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

from asrd.qt_design.form import Ui_MainWindow  # Converted file with design
from asrd.data_preparation import Analyzer


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.analyzer = Analyzer()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.path)
        self.ui.pushButton_2.clicked.connect(self.plot)

    def path(self):
        path = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.ui.lineEdit.setText(path)
        self.analyzer.parse(path)
        self.ui.comboBox.addItems(self.analyzer.get_samples_names())

    def plot(self):
        self.analyzer.models_calculation()
        sample_index = self.ui.comboBox.currentIndex()
        pixmap = QPixmap(self.analyzer.plot_graph(sample_index))
        self.ui.label_2.setPixmap(pixmap)


app = QtWidgets.QApplication([])
application = MyApp()
application.show()

sys.exit(app.exec())
