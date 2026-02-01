# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'apikey.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_APIkeyDialog(object):
    def setupUi(self, APIkeyDialog):
        if not APIkeyDialog.objectName():
            APIkeyDialog.setObjectName(u"APIkeyDialog")
        APIkeyDialog.resize(230, 138)
        APIkeyDialog.setMaximumSize(QSize(230, 138))
        self.verticalLayout_3 = QVBoxLayout(APIkeyDialog)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.APIkeyFrame = QFrame(APIkeyDialog)
        self.APIkeyFrame.setObjectName(u"APIkeyFrame")
        self.APIkeyFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.APIkeyFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.APIkeyFrame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.preference1Frame = QFrame(self.APIkeyFrame)
        self.preference1Frame.setObjectName(u"preference1Frame")
        self.preference1Frame.setMaximumSize(QSize(16777215, 200))
        self.preference1Frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.preference1Frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.preference1Frame)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.APIkeyLabel = QLabel(self.preference1Frame)
        self.APIkeyLabel.setObjectName(u"APIkeyLabel")

        self.verticalLayout.addWidget(self.APIkeyLabel)

        self.APIkeyLineEdit = QLineEdit(self.preference1Frame)
        self.APIkeyLineEdit.setObjectName(u"APIkeyLineEdit")

        self.verticalLayout.addWidget(self.APIkeyLineEdit)

        self.buttonBox = QDialogButtonBox(self.preference1Frame)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)

        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 2)

        self.horizontalLayout.addWidget(self.preference1Frame)


        self.verticalLayout_3.addWidget(self.APIkeyFrame)


        self.retranslateUi(APIkeyDialog)

        QMetaObject.connectSlotsByName(APIkeyDialog)
    # setupUi

    def retranslateUi(self, APIkeyDialog):
        APIkeyDialog.setWindowTitle(QCoreApplication.translate("APIkeyDialog", u"API key", None))
        self.APIkeyLabel.setText(QCoreApplication.translate("APIkeyDialog", u"Please enter your API key", None))
    # retranslateUi

