from PyQt5 import QtCore, QtGui, QtWidgets
import firebase_admin
from firebase_admin import credentials,firestore
import threading

class Ui_Form(object):

    def click(self, state):

        col_query = self.db.collection(u'data').document(u'test')

        if state == QtCore.Qt.Checked:

            col_query.update({"durum": "on"})
            self.checkBox.setText("on")


        elif state == QtCore.Qt.Unchecked:

            col_query.update({"durum": "off"})
            self.checkBox.setText("off")

    def setupUi(self, Form):

        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(90, 120, 81, 20))

        self.checkBox.stateChanged.connect(self.click)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


        callback_done = threading.Event()

        self.Id = credentials.Certificate(r'./dosya_adi.json')
        self.app = firebase_admin.initialize_app(self.Id)
        self.db = firestore.client()

        callback_done = threading.Event()

        delete_done = threading.Event()

        def on_snapshot(col_snapshot, changes, read_time):

            for change in changes:
                if change.type.name == 'ADDED':

                    print(f'New : {change.document.to_dict()}')
                    data = change.document.to_dict()

                    if data["durum"] == "on":
                        self.checkBox.setChecked(True)
                        self.checkBox.setText("on")

                    else:

                        self.checkBox.setChecked(False)

                        self.checkBox.setText("off")


                elif change.type.name == 'MODIFIED':

                    print(f'Modified : {change.document.to_dict()}')
                    data = change.document.to_dict()

                    if data["durum"] == "on":
                        self.checkBox.setChecked(True)
                        self.checkBox.setText("on")

                    else:

                        self.checkBox.setChecked(False)

                        self.checkBox.setText("off")


                elif change.type.name == 'REMOVED':

                    print(f'Removed : {change.document.to_dict()}')
                    data = change.document.to_dict()

                    if data["durum"] == "on":
                        self.checkBox.setChecked(True)
                        self.checkBox.setText("on")

                    else:
                        self.checkBox.setChecked(False)
                        self.checkBox.setText("off")


                    delete_done.set()

            callback_done.set()

        document = self.db.collection("data").document("test")

        query_watch = document.on_snapshot(on_snapshot)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.checkBox.setText(_translate("Form", " "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

