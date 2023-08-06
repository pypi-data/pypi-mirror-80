# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calibration_panel.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_CalibrationPanel(object):
    def setupUi(self, CalibrationPanel):
        if not CalibrationPanel.objectName():
            CalibrationPanel.setObjectName(u"CalibrationPanel")
        CalibrationPanel.resize(95, 158)
        self.verticalLayout = QVBoxLayout(CalibrationPanel)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.buttonBox = QDialogButtonBox(CalibrationPanel)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Save)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(CalibrationPanel)

        QMetaObject.connectSlotsByName(CalibrationPanel)
    # setupUi

    def retranslateUi(self, CalibrationPanel):
        CalibrationPanel.setWindowTitle(QCoreApplication.translate("CalibrationPanel", u"Calibration", None))
        CalibrationPanel.setTitle(QCoreApplication.translate("CalibrationPanel", u"Calibration", None))
    # retranslateUi

