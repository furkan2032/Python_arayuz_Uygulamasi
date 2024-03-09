import cv2
import numpy as np
from PyQt5.QtWidgets import *
from login import Ui_Form
from main import Ui_MainWindow


class main(QMainWindow):
    def __init__(self) ->None:
        super().__init__()
        self.anaPencereForm=Ui_MainWindow()
        self.anaPencereForm.setupUi(self)
        self.anaPencereForm.pushButton.clicked.connect(self.image)


    def image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_path, _ = file_dialog.getOpenFileName(self, "Resim Seç", "", "Images (*.png *.jpg *.bmp)")
        global image
        image = cv2.imread(file_path)
        image = cv2.resize(image, (650,650))
        cv2.imshow("byfurkan", image)

        if self.anaPencereForm.checkBox.isChecked():
            deger = self.anaPencereForm.spinBox.value()
            image[:, :, 0] = 51 * deger

        if self.anaPencereForm.checkBox_2.isChecked():
            deger_2 = self.anaPencereForm.spinBox_2.value()
            image[:, :, 1] = 51 * deger_2
        if self.anaPencereForm.checkBox_3.isChecked():
            deger_3 = self.anaPencereForm.spinBox_3.value()
            image[:, :, 2] = 51 * deger_3
        if self.anaPencereForm.radioButton.isChecked():
            name = self.anaPencereForm.lineEdit.text()
            cv2.putText(image, "Hosgeldin " + name, (160, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))
            image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0, 0, 255))
        if self.anaPencereForm.radioButton_2.isChecked():
            value = self.anaPencereForm.horizontalSlider.value()
            self.anaPencereForm.label_2.setText(f"Slider Değeri : {value }")
            image = cv2.resize(image, (value*5, value*5))
        if self.anaPencereForm.radioButton_3.isChecked():
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, thresh_image = cv2.threshold(gray_image, 220, 255, cv2.THRESH_BINARY)

            contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # image, mode , how is it
            for i, contour in enumerate(contours):
                if i == 0:
                    continue
                epsilon = 0.01 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                cv2.drawContours(image, contour, 0, (0, 0, 0), 4)

                x, y, w, h = cv2.boundingRect(approx)
                x_mid = int(x + (w / 3))
                y_mid = int(y + (h / 1.5))

                coords = (x_mid, y_mid)
                colour = (0, 0, 0)
                font = cv2.FONT_HERSHEY_DUPLEX

                if len(approx) == 3:
                    cv2.putText(image, "Triangle", coords, font, 1, colour, 1)
                elif len(approx) == 4:
                    cv2.putText(image, "Quadrilateral", coords, font, 1, colour, 1)
                elif len(approx) == 5:
                    cv2.putText(image, "Pentagon", coords, font, 1, colour, 1)
                elif len(approx) == 6:
                    cv2.putText(image, "Hexagon", coords, font, 1, colour, 1)
                else:
                    cv2.putText(image, "Circle", coords, font, 1, colour, 1)
        if self.anaPencereForm.radioButton_4.isChecked():
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier("frontalface.xml")
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            for x, y, w, h in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if self.anaPencereForm.radioButton_5.isChecked():
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([100, 50, 50])
            upper_blue = np.array([130, 255, 255])
            mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
            result_image = cv2.bitwise_and(image, image, mask=mask)
            cv2.imshow('Result Image', result_image)

        cv2.imshow("byfurkan",image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.loginForm = Ui_Form()
        self.loginForm.setupUi(self)
        self.anapencereac = main()
        self.loginForm.pushButton.clicked.connect(self.login)
    def login(self):
        userName = self.loginForm.lineEdit.text()
        password = self.loginForm.lineEdit_2.text()
        if userName == "byfurkan" and password == "123":
            self.hide()
            self.anapencereac.show()
        else:
            QMessageBox.warning(self, "Error!", "Hatalı veya yanlış giriş yaptınız\nLütfen tekrar deneyiniz.")

app = QApplication([])
pencere = Login()
pencere.show()
app.exec_()