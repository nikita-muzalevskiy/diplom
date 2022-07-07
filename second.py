import login, PGdb
import os
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox, QWidget, QPushButton, \
    QLineEdit, QInputDialog, QListView, QTableView
from data_base.db import autofillLite, autofillPG, autodeletePG, autodeleteLite


class ExampleApp(QtWidgets.QMainWindow, login.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле untitled.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.tabWidget.setCurrentIndex(0)
        self.pushButton.clicked.connect(lambda: self.login())
        self.pushButton_2.clicked.connect(lambda: self.tabWidget.setCurrentIndex(1))
        self.pushButton_3.clicked.connect(lambda: self.registration())
        self.pushButton_4.clicked.connect(lambda: self.tabWidget.setCurrentIndex(0))

        self.tabWidget.tabBar().hide()

    def login(self):
        log = self.lineEdit.text()
        pas = self.lineEdit_2.text()
        i = PGdb.query(f"SELECT COUNT(*) FROM users WHERE login = '{log}'")[0][0]
        if i == 1:
            j = PGdb.query(f"SELECT COUNT(*) FROM users WHERE login = '{log}' AND pass = '{pas}'")[0][0]
            if j == 1:
                self.set_text_id()
                autofillLite()
                self.close()
                os.system('python main.py')
            else:
                QMessageBox.critical(self, "Ошибка ", f'Неверный пароль', QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Ошибка ", f'Не найден пользователь с таким логином', QMessageBox.Ok)
    def registration(self):
        log = self.lineEdit_3.text()
        pas = self.lineEdit_4.text()
        pas2 = self.lineEdit_5.text()
        i = PGdb.query(f"SELECT COUNT(*) FROM users WHERE login = '{log}'")[0][0]
        if i == 1:
            QMessageBox.critical(self, "Ошибка ", f'Пользователь с таким логином уже существует', QMessageBox.Ok)
        elif pas != pas2:
            QMessageBox.critical(self, "Ошибка ", f'Повторный пароль введен неверно', QMessageBox.Ok)
        elif i == 0:
            PGdb.query_no_ret(f"INSERT INTO users (login, pass) VALUES ('{log}', '{pas}')")
    def set_text_id(self):
        log = self.lineEdit.text()
        i = PGdb.query(f"SELECT * FROM users WHERE login = '{log}'")
        id = i[0][0]
        print(id)
        file = open("user.txt", "w")
        file.write(f"1\n{id}")




def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()



if __name__ == '__main__':


        #ДЛЯ ЗАПУСКА ОКНА 1 ВАРИАНТ

    main()