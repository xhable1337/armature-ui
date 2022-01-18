# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'info.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self):
        """Метод инициализации интерфейса."""
        super().__init__()
        self.setupUi(self)
    
    def setupUi(self, Dialog: QtWidgets.QDialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowFlags(Dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        Dialog.resize(600, 300)
        Dialog.setMinimumSize(QtCore.QSize(600, 300))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.info_text = QtWidgets.QTextBrowser(Dialog)
        self.info_text.setStyleSheet("    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: #828790;")
        self.info_text.setObjectName("info_text")
        self.gridLayout.addWidget(self.info_text, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
    def closeEvent(self, e: QtGui.QCloseEvent) -> None:
        self.resize(600, 300)
        return super().closeEvent(e)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle("Помощь и информация")
        self.info_text.setHtml(_translate(
            "Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Circe\'; font-size:14pt; font-weight:600; text-decoration: underline;\">Помощь по программе</span></p>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Circe\'; font-size:14pt; font-weight:600;\">a, b, h</span><span style=\" font-family:\'Circe\'; font-size:14pt;\"> — габариты сечения, где a &lt; h</span></p>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Circe\'; font-size:14pt; font-weight:600;\">A</span><span style=\" font-family:\'Circe\'; font-size:14pt; font-weight:600; vertical-align:sub;\">s</span><span style=\" font-family:\'Circe\'; font-size:14pt;\"> — площадь сечения растянутой арматуры</span></p>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Circe\'; font-size:14pt; font-weight:600;\">M</span><span style=\" font-family:\'Circe\'; font-size:14pt;\"> — изгибающий момент с учетом кратковременных нагрузок</span></p>"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Circe\'; font-size:14pt; font-weight:600;\">N</span><span style=\" font-family:\'Circe\'; font-size:14pt;\"> — растягивающая сила</span></p>"
            "</body></html>"
        ))