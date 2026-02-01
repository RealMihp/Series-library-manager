# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preferences.ui'
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
    QFrame, QLabel, QLineEdit, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        if not Preferences.objectName():
            Preferences.setObjectName(u"Preferences")
        Preferences.resize(400, 513)
        self.verticalLayout = QVBoxLayout(Preferences)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.preferencesFrame = QFrame(Preferences)
        self.preferencesFrame.setObjectName(u"preferencesFrame")
        self.preferencesFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.preferencesFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.preferencesFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.preference1Frame = QFrame(self.preferencesFrame)
        self.preference1Frame.setObjectName(u"preference1Frame")
        self.preference1Frame.setMaximumSize(QSize(16777215, 70))
        self.preference1Frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.preference1Frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.preference1Frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.P1label = QLabel(self.preference1Frame)
        self.P1label.setObjectName(u"P1label")

        self.verticalLayout_2.addWidget(self.P1label)

        self.P1LineEdit = QLineEdit(self.preference1Frame)
        self.P1LineEdit.setObjectName(u"P1LineEdit")

        self.verticalLayout_2.addWidget(self.P1LineEdit)


        self.verticalLayout_3.addWidget(self.preference1Frame)

        self.preference2Frame = QFrame(self.preferencesFrame)
        self.preference2Frame.setObjectName(u"preference2Frame")
        self.preference2Frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.preference2Frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_3.addWidget(self.preference2Frame)

        self.preference3Frame = QFrame(self.preferencesFrame)
        self.preference3Frame.setObjectName(u"preference3Frame")
        self.preference3Frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.preference3Frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_3.addWidget(self.preference3Frame)


        self.verticalLayout.addWidget(self.preferencesFrame)

        self.buttonBox = QDialogButtonBox(Preferences)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Preferences)
        self.buttonBox.accepted.connect(Preferences.accept)
        self.buttonBox.rejected.connect(Preferences.reject)

        QMetaObject.connectSlotsByName(Preferences)
    # setupUi

    def retranslateUi(self, Preferences):
        Preferences.setWindowTitle(QCoreApplication.translate("Preferences", u"Preferences", None))
        self.P1label.setText(QCoreApplication.translate("Preferences", u"API key", None))
    # retranslateUi

