# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'remote_panel.ui'
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


class Ui_RemotePanel(object):
    def setupUi(self, RemotePanel):
        if not RemotePanel.objectName():
            RemotePanel.setObjectName(u"RemotePanel")
        RemotePanel.resize(112, 182)
        self.verticalLayout = QVBoxLayout(RemotePanel)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.goToParentButton = QPushButton(RemotePanel)
        self.goToParentButton.setObjectName(u"goToParentButton")

        self.verticalLayout.addWidget(self.goToParentButton)


        self.retranslateUi(RemotePanel)

        QMetaObject.connectSlotsByName(RemotePanel)
    # setupUi

    def retranslateUi(self, RemotePanel):
        RemotePanel.setWindowTitle(QCoreApplication.translate("RemotePanel", u"Remote Device Panel", None))
        RemotePanel.setTitle(QCoreApplication.translate("RemotePanel", u"Remote Device", None))
        self.goToParentButton.setText(QCoreApplication.translate("RemotePanel", u"Go To Radio Tab", None))
    # retranslateUi

