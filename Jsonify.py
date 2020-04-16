__author__ = "Raviraj Prajapat"

from PyQt5 import QtCore, QtGui, QtWidgets
import json
import clipboard
import ast


class TextToTreeItem:
    def __init__(self):
        self.text_list = []
        self.titem_list = []

    def append(self, text_list, titem):
        for text in text_list:
            self.text_list.append(text)
            self.titem_list.append(titem)

    # Return model indices that match string
    def find(self, find_str):

        titem_list = []
        for i, s in enumerate(self.text_list):
            if find_str.lower() in s.lower():
                titem_list.append(self.titem_list[i])

        return titem_list


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        MainWindow.setAutoFillBackground(True)

        # MainWindow.setStyleSheet("QMainWindow {background: '#FFFFFF';}")

        self.text_to_titem = TextToTreeItem()

        self.find_str = ""
        self.found_titem_list = []
        self.found_idx = 0
        self.text_to_titem = TextToTreeItem()

        self.jsontree = QtWidgets.QTreeWidget()
        self.jsontree.setHeaderLabels(["Key", "Value"])
        self.jsontree.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Kozuka Gothic Pro B")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        fontinfo = QtGui.QFont()
        fontinfo.setPointSize(12)

        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 180, 791, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.jsontree = QtWidgets.QTreeWidget(self.centralwidget)
        self.jsontree.setGeometry(QtCore.QRect(60, 80, 701, 381))
        self.jsontree.setObjectName("jsontree")
        self.jsontree.setHeaderLabels(["Key", "Value"])
        self.jsontree.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.jsonButton = QtWidgets.QPushButton(self.centralwidget)
        self.jsonButton.setGeometry(QtCore.QRect(60, 50, 210, 28))
        self.jsonButton.setObjectName("jsonButton")
        self.findjson = QtWidgets.QLineEdit(self.centralwidget)
        self.findjson.setGeometry(QtCore.QRect(550, 50, 210, 28))
        self.findjson.setObjectName("findjson")
        self.findjson.setPlaceholderText("Search Json")

        self.info = QtWidgets.QLabel(self.centralwidget)
        self.info.setGeometry(QtCore.QRect(60, 5, 651, 40))
        self.info.setFont(fontinfo)
        self.info.setTextFormat(QtCore.Qt.RichText)
        self.info.setAlignment(QtCore.Qt.AlignCenter)
        self.info.setWordWrap(False)
        self.info.setObjectName("info")
        self.info.setText(
            '<span style=\" color: #004C99;\">%s</span>' % "Please Copy some text from any where and Hit Jsonify.")

        self.sinfo = QtWidgets.QLabel(self.centralwidget)
        self.sinfo.setGeometry(QtCore.QRect(60, 460, 651, 40))
        self.sinfo.setFont(fontinfo)
        self.sinfo.setTextFormat(QtCore.Qt.RichText)
        self.sinfo.setAlignment(QtCore.Qt.AlignCenter)
        self.sinfo.setWordWrap(False)
        self.sinfo.setObjectName("info")
        self.sinfo.setText('<span style=\" color: #FF007F;\">%s</span>' % "Made with &hearts; love by Raviraj.")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.jsonButton.clicked.connect(self.recure)

        self.findjson.returnPressed.connect(self.find_button_clicked)
        self.jsontree.itemDoubleClicked.connect(self.jsonpopup)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def recure(self):
        if clipboard.paste():
            try:
                try:
                    jdata = json.loads(clipboard.paste())
                except:
                    jdata = ast.literal_eval(clipboard.paste())
                self.jsontree.clear()
                root_item = QtWidgets.QTreeWidgetItem(["Root"])
                root_item.setForeground(0, QtGui.QColor("blue"))
                self.recurse_jdata(jdata, root_item)
                self.jsontree.addTopLevelItem(root_item)
            except Exception as e:
                QtWidgets.QMessageBox.information(MainWindow, 'Details',
                                                  '<span style=\" color: #ff0000;\">%s</span>' % "Please check your copied text at clipboard, error occurred with exception",
                                                  QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.information(MainWindow, 'Details',
                                              '<span style=\" color: #0066CC;\">%s</span>' % "Please copy some text to Jsonify!",
                                              QtWidgets.QMessageBox.Ok)

    def recurse_jdata(self, jdata, tree_widget):
        if isinstance(jdata, dict):
            for key, val in jdata.items():
                self.tree_add_row(key, val, tree_widget)
        elif isinstance(jdata, list):
            for i, val in enumerate(jdata):
                key = str(i)
                self.tree_add_row(key, val, tree_widget)
        else:
            print("This should never be reached!")

    def tree_add_row(self, key, val, tree_widget):

        text_list = []

        if isinstance(val, dict) or isinstance(val, list):
            text_list.append(key)
            row_item = QtWidgets.QTreeWidgetItem([key])
            row_item.setForeground(0, QtGui.QColor("green"))
            self.recurse_jdata(val, row_item)
        else:
            text_list.append(key)
            text_list.append(str(val))
            row_item = QtWidgets.QTreeWidgetItem([key, str(val)])
            row_item.setForeground(0, QtGui.QColor("green"))

        tree_widget.addChild(row_item)
        self.text_to_titem.append(text_list, row_item)

    def find_button_clicked(self):
        find_str = self.findjson.text()

        # Very common for use to click Find on empty string
        if find_str == "":
            return

        # New search string
        if find_str != self.find_str:
            self.find_str = find_str
            self.found_titem_list = self.text_to_titem.find(self.find_str)
            self.found_idx = 0
        else:
            item_num = len(self.found_titem_list)
            try:
                self.found_idx = (self.found_idx + 1) % item_num
            except:
                QtWidgets.QMessageBox.information(MainWindow, 'Details',
                                                  '<span style=\" color: #ff0000;\">%s</span>' % "Invalid Input for Search. Try Re-entering",
                                                  QtWidgets.QMessageBox.Ok)

        try:
            self.jsontree.setCurrentItem(self.found_titem_list[self.found_idx])
        except:
            QtWidgets.QMessageBox.information(MainWindow, 'Details',
                                              '<span style=\" color: #ff0000;\">%s</span>' % "Invalid Input for Search",
                                              QtWidgets.QMessageBox.Ok)

    def jsonpopup(self):
        itm = self.jsontree.selectedIndexes()[0]
        itmtxt = self.jsontree.itemFromIndex(itm).text(1)

        QtWidgets.QMessageBox.information(MainWindow, 'Details',
                                          itmtxt,
                                          QtWidgets.QMessageBox.Ok)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Jsonify Me!"))

        self.jsonButton.setText(_translate("MainWindow", "Jsonify"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
