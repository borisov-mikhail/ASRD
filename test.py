from PyQt5 import QtCore, QtWidgets

app = QtWidgets.QApplication([])

wb_patch = QtWidgets.QFileDialog.getOpenFileName()[0]
print(wb_patch)
