# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(788, 675)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_main = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.gif_layout = QtWidgets.QHBoxLayout()
        self.gif_layout.setObjectName("gif_layout")
        self.left_column = QtWidgets.QVBoxLayout()
        self.left_column.setObjectName("left_column")
        self.gif_widget = QtWidgets.QLabel(self.centralwidget)
        self.gif_widget.setText("")
        self.gif_widget.setObjectName("gif_widget")
        self.left_column.addWidget(self.gif_widget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.left_column.addItem(spacerItem)
        self.gif_layout.addLayout(self.left_column)
        self.right_column = QtWidgets.QVBoxLayout()
        self.right_column.setObjectName("right_column")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.right_column.addItem(spacerItem1)
        self.gif_layout.addLayout(self.right_column)
        self.verticalLayout_main.addLayout(self.gif_layout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.beginning_button = QtWidgets.QPushButton(self.centralwidget)
        self.beginning_button.setText("")
        icon = QtGui.QIcon.fromTheme("media-skip-backward")
        self.beginning_button.setIcon(icon)
        self.beginning_button.setObjectName("beginning_button")
        self.horizontalLayout.addWidget(self.beginning_button)
        self.previous_button = QtWidgets.QPushButton(self.centralwidget)
        self.previous_button.setText("")
        icon = QtGui.QIcon.fromTheme("media-seek-backward")
        self.previous_button.setIcon(icon)
        self.previous_button.setObjectName("previous_button")
        self.horizontalLayout.addWidget(self.previous_button)
        self.play_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_button.setText("")
        icon = QtGui.QIcon.fromTheme("media-playback-start")
        self.play_button.setIcon(icon)
        self.play_button.setObjectName("play_button")
        self.horizontalLayout.addWidget(self.play_button)
        self.next_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_button.setText("")
        icon = QtGui.QIcon.fromTheme("media-seek-forward")
        self.next_button.setIcon(icon)
        self.next_button.setObjectName("next_button")
        self.horizontalLayout.addWidget(self.next_button)
        self.end_button = QtWidgets.QPushButton(self.centralwidget)
        self.end_button.setText("")
        icon = QtGui.QIcon.fromTheme("media-skip-forward")
        self.end_button.setIcon(icon)
        self.end_button.setObjectName("end_button")
        self.horizontalLayout.addWidget(self.end_button)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_main.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 788, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "multigifview"))
        self.beginning_button.setShortcut(_translate("MainWindow", "B"))
        self.previous_button.setShortcut(_translate("MainWindow", "P"))
        self.play_button.setShortcut(_translate("MainWindow", "Space"))
        self.next_button.setShortcut(_translate("MainWindow", "N"))
        self.end_button.setShortcut(_translate("MainWindow", "E"))
