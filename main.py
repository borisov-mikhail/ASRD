import sys  # sys нужен для передачи argv в QApplication
import os  # Отсюда нам понадобятся методы для отображения содержимого директорий
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
from data_preparation import *
from form import *  # Это наш конвертированный файл дизайна


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.path)
        self.ui.pushButton_2.clicked.connect(self.plot)

    def path(self):
        path = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.ui.lineEdit.setText(path)
        self.ui.comboBox.addItems(read_data(self.ui.lineEdit.text()))

    def plot(self):
        pixmap = QPixmap(plot_graph(self.ui.comboBox.currentIndex(), x='P/P0_1', y='V'))
        self.ui.label_2.setPixmap(pixmap)


app = QtWidgets.QApplication([])
application = MyApp()
application.show()

sys.exit(app.exec())
