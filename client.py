from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt5.Qt import QUrl, QDesktopServices
import requests
import sys
import webbrowser


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Client")
        self.setFixedSize(400, 400)

        self.label1 = QLabel("Enter your hostname:", self)
        self.label1.move(10, 0)
        self.text = QLineEdit(self)
        self.text.move(10, 15)

        self.label3 = QLabel("Enter your api_key:", self)
        self.label3.move(10, 45)
        self.text3 = QLineEdit(self)
        self.text3.move(10, 60)

        self.label4 = QLabel("Enter your host IP:", self)
        self.label4.move(10, 90)
        self.text4 = QLineEdit(self)
        self.text4.move(10, 105)



        self.label2 = QLabel("Answer:", self)
        self.label2.move(10, 240)
        self.button = QPushButton("Send", self)
        self.button.move(10, 130)

        self.button.clicked.connect(self.on_click)
        self.button.pressed.connect(self.on_click)

        self.show()

    def on_click(self):
        hostname = self.text.text()
        ip = self.text4.text()
        api_key= self.text3.text()

        if hostname == "":
            QMessageBox.about(self, "Error", "Please fill the field")
        else:
            res = self.__query(hostname, ip, api_key)
            if res:
                self.label2.setText(" %s \n %s" % (res["Longitude"], res["Latitude"]))
                self.label2.adjustSize()
                self.show()
                coord = "https://www.openstreetmap.org/?mlat=%s&mlon=%s#map=12" % (res["Latitude"], res["Longitude"])
                webbrowser.open_new_tab(coord)

    def __query(self, hostname, ip, api_key):
        url = "http://%s/ip/%s?key=%s" % (hostname, ip , api_key)
        r = requests.get(url)
        if r.status_code == requests.codes.NOT_FOUND:
            QMessageBox.about(self, "Error", "IP not found")
        if r.status_code == requests.codes.OK:
            return r.json()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()