import sys  # sys нужен для передачи argv в QApplication
import os
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox, QPushButton, QLineEdit, QTableView
from PyQt5.QtCore import QDate
import PGdb
import datetime
import untitled  # Конвертированный файл дизайна
from data_base.db import (sqlite_start, DBinsert, DBinsert_profit, get_list, db_delete, get_count, db_insert, get_column, get_column_profit)
from data_base.db import (autodeletePG, autodeleteLite, autofillLite, autofillPG)
from diagrams import (save_dia_s, save_dia_c, save_dia_m, save_dia_m_plus, get_groups, get_month, get_month_plus)

class ExampleApp(QtWidgets.QMainWindow, untitled.Ui_MainWindow):
        def __init__(self):
            # Это здесь нужно для доступа к переменным, методам в файле untitled.py
            super().__init__()
            self.setupUi(self)  # Это нужно для инициализации нашего дизайна
            self.buttonsWork()
            self.wigetsWork()
            self.startStyle()
            self.styleButton()
        def wigetsWork(self):
            # Скрываем заголовки вкладок
            self.tabWidget.tabBar().hide()
            self.tabWidget_2.tabBar().hide()
            self.tabWidget_3.tabBar().hide()
            self.tabWidget_4.tabBar().hide()

            # Установка даты в DateEdit
            self.dateEdit.setDate(datetime.datetime.today())
            self.dateEdit_2.setDate(QDate(2021, 1, 1))
            self.dateEdit_3.setDate(datetime.datetime.today())
            self.dateEdit_4.setDate(datetime.datetime.today())

            self.date_change()
            self.update("shops", self.tableWidget)
            self.update("category", self.tableWidget_2)
            self.update("category_profit", self.tableWidget_4)
            self.update_history(self.tableWidget_3)
            self.update_history_profit(self.tableWidget_5)
            self.dateEdit_3.dateChanged.connect(self.date_change)

            # Окно ПРОФИЛЬ
            file = open("user.txt", "r")
            file.seek(0)
            id = file.readlines()[1]
            self.label_16.setText(PGdb.query(f"SELECT login FROM users WHERE id = {id}")[0][0])
            self.pushButton_17.clicked.connect(lambda: self.export_db())
            self.pushButton_18.clicked.connect(lambda: self.import_db())
            # self.pushButton_19.clicked.connect()
            self.pushButton_20.clicked.connect(lambda: self.logout())

            # Скрываем заголовки таблиц
            self.tableWidget.verticalHeader().hide()
            self.tableWidget.horizontalHeader().hide()
            self.tableWidget_2.verticalHeader().hide()
            self.tableWidget_2.horizontalHeader().hide()
            self.tableWidget_3.verticalHeader().hide()
            self.tableWidget_3.horizontalHeader().hide()
            self.tableWidget_4.verticalHeader().hide()
            self.tableWidget_4.horizontalHeader().hide()
            self.tableWidget_5.verticalHeader().hide()
            self.tableWidget_5.horizontalHeader().hide()
        def buttonsWork(self):
            self.pushButton_7.clicked.connect(lambda: self.tabWidget_2.setCurrentIndex(0))
            self.pushButton_8.clicked.connect(lambda: self.tabWidget_2.setCurrentIndex(1))
            self.pushButton_12.clicked.connect(lambda: self.tabWidget_2.setCurrentIndex(2))
            self.pushButton_9.clicked.connect(lambda: self.tabWidget_3.setCurrentIndex(0))
            self.pushButton_10.clicked.connect(lambda: self.tabWidget_3.setCurrentIndex(1))
            self.pushButton_15.clicked.connect(lambda: self.tabWidget_4.setCurrentIndex(0))
            self.pushButton_16.clicked.connect(lambda: self.tabWidget_4.setCurrentIndex(1))
            self.pushButton_21.clicked.connect(lambda: self.tabWidget.setCurrentIndex(0))
            self.pushButton_22.clicked.connect(lambda: self.tabWidget.setCurrentIndex(1))
            self.pushButton_23.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
            self.pushButton_24.clicked.connect(lambda: self.tabWidget.setCurrentIndex(3))
            self.pushButton_25.clicked.connect(lambda: self.tabWidget.setCurrentIndex(4))

            self.pushButton_2.clicked.connect(lambda: self.update_history(self.tableWidget_3))
            self.pushButton_2.clicked.connect(lambda: self.update_history_profit(self.tableWidget_5))
            self.pushButton_3.clicked.connect(lambda: self.delete(self.lineEdit_3, "shops", self.tableWidget))
            self.pushButton_4.clicked.connect(lambda: self.insert(self.lineEdit_3, "shops", self.tableWidget))
            self.pushButton_5.clicked.connect(lambda: self.delete(self.lineEdit_5, "category", self.tableWidget_2))
            self.pushButton_6.clicked.connect(lambda: self.insert(self.lineEdit_5, "category", self.tableWidget_2))
            self.pushButton_14.clicked.connect(lambda: self.delete(self.lineEdit, "category_profit", self.tableWidget_4))
            self.pushButton_13.clicked.connect(lambda: self.insert(self.lineEdit, "category_profit", self.tableWidget_4))

            self.pushButton.clicked.connect(self.insert_outlay)
            self.pushButton_11.clicked.connect(self.insert_profit)
        def logout(self):
            autodeletePG()
            autofillPG()
            autodeleteLite()
            file = open("user.txt", "w")
            file.write("0")
            self.close()
            os.system("python second.py")
        def export_db(self):
            autodeletePG()
            autofillPG()
        def import_db(self):
            autodeleteLite()
            autofillLite()
            self.update_history(self.tableWidget_3)
            self.update_history_profit(self.tableWidget_5)
        def sh_cat_up(self):
            self.comboBox.clear()
            self.comboBox_2.clear()
            self.comboBox_3.clear()
            list1 = get_list("shops")
            for i in range(len(list1)):
                self.comboBox.addItem(list1[i])
            list1 = get_list("category")
            for i in range(len(list1)):
                self.comboBox_2.addItem(list1[i])
            list1 = get_list("category_profit")
            for i in range(len(list1)):
                self.comboBox_3.addItem(list1[i])
        def insert_outlay(self):
            shop = self.comboBox.currentText()
            print(shop)
            cat  = self.comboBox_2.currentText()
            print(cat)
            date = self.dateEdit.date().toPyDate()
            print(date)
            sum  = self.lineEdit_4.text()
            print(sum)
            if shop == "":
                QMessageBox.critical(self,
                                     "Ошибка ",
                                     f'Вы не заполнили поле "Магазин". Если нет доступных вариантов для заполнения, добавьте их в разделе "Категории/Магазины."',
                                     QMessageBox.Ok)
                return
            if cat  == "":
                QMessageBox.critical(self,
                                     "Ошибка ",
                                     f'Вы не заполнили поле "Категория". Если нет доступных вариантов для заполнения, добавьте их в разделе "Категории/Магазины".',
                                     QMessageBox.Ok)
                return
            if sum  == "":
                QMessageBox.critical(self, "Ошибка ",
                                     f'Вы не заполнили поле "Сумма".',
                                     QMessageBox.Ok)
                return
            DBinsert(shop, cat, date, sum)
            self.update_history(self.tableWidget_3)
        def insert_profit(self):
            cat = self.comboBox_3.currentText()
            print(cat)
            date = self.dateEdit_4.date().toPyDate()
            print(date)
            sum = self.lineEdit_2.text()
            print(sum)
            if cat  == "":
                QMessageBox.critical(self,
                                     "Ошибка ",
                                     f'Вы не заполнили поле "Категория". Если нет доступных вариантов для заполнения, добавьте их в разделе "Категории/Магазины".',
                                     QMessageBox.Ok)
                return
            if sum  == "":
                QMessageBox.critical(self, "Ошибка ",
                                     f'Вы не заполнили поле "Сумма".',
                                     QMessageBox.Ok)
                return
            DBinsert_profit(cat, date, sum)
            self.update_history_profit(self.tableWidget_5)
        def update(self, table, w_table):
            # получаем список из базы данных
            my_list = get_list(table)
            # устанавливаем количество столбцов и строк и растягиваем строку по всей ширине
            w_table.setColumnCount(1)
            w_table.setRowCount(len(my_list))
            w_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

            w_table.setHorizontalHeaderLabels([""])
            w_table.horizontalHeaderItem(0).setToolTip("Column 1")

            # заполняем таблицу
            for i in range(len(my_list)):
                w_table.setItem(0, i, QTableWidgetItem(my_list[i]))

            self.sh_cat_up()
        def update_history(self, w_table):
            date1 = self.dateEdit_2.date().toPyDate()
            date2 = self.dateEdit_3.date().toPyDate()
            rows = get_column(date1, date2)
            w_table.setColumnCount(4)
            w_table.setRowCount(len(rows))
            w_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

            w_table.setHorizontalHeaderLabels(["Магазин","Категория","Дата","Сумма"])
            w_table.horizontalHeaderItem(0).setToolTip("Column 1")

            for i in range(len(rows)):
                for j in range(4):
                    w_table.setItem(i, j, QTableWidgetItem(str(rows[i][j+1])))
            self.past_pic()
        def update_history_profit(self, w_table):
            date1 = self.dateEdit_2.date().toPyDate()
            date2 = self.dateEdit_3.date().toPyDate()
            rows = get_column_profit(date1, date2)
            w_table.setColumnCount(3)
            w_table.setRowCount(len(rows))
            w_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

            w_table.setHorizontalHeaderLabels(["Категория","Дата","Сумма"])
            w_table.horizontalHeaderItem(0).setToolTip("Column 1")

            for i in range(len(rows)):
                for j in range(3):
                    w_table.setItem(i, j, QTableWidgetItem(str(rows[i][j+1])))
            self.past_pic()
        def delete(self, n: QLineEdit, table, w_table):
            name = n.text()
            if name == "":
                QMessageBox.critical(self, "Ошибка ", f'Вы не заполнили поле', QMessageBox.Ok)
                return
            count = get_count(name, table)
            if count == 0:
                QMessageBox.critical(self, "Ошибка ", f'Не удалось найти "{name}" в списке', QMessageBox.Ok)
                return
            else:
                db_delete(name, table)
                self.update(table, w_table)
            self.update_history(self.tableWidget_3)
            self.update_history_profit(self.tableWidget_5)
        def insert(self, n: QLineEdit, table, w_table):
            name = n.text()
            if name == "":
                QMessageBox.critical(self, "Ошибка ", f'Вы не заполнили поле', QMessageBox.Ok)
                return
            if get_count(name, table) != 0:
                QMessageBox.critical(self, "Ошибка ", f'"{name}" уже есть в списке', QMessageBox.Ok)
                return
            db_insert(name, table)
            self.update(table, w_table)
            self.update_history(self.tableWidget_3)
            self.update_history_profit(self.tableWidget_5)
        def date_change(self):
            date1 = self.dateEdit_2.date().toPyDate()
            date2 = self.dateEdit_3.date().toPyDate()
            self.dateEdit_2.setMaximumDate(date2)
            if date1 > date2:
                self.dateEdit_2.setDate(date2)
        #Сохраняет диаграммы
        def past_pic(self):
            x, y = get_groups("category")
            save_dia_c(x, y)
            x, y = get_groups("shop")
            save_dia_s(x, y)
            x, y = get_month()
            save_dia_m(x, y)
            x, y = get_month_plus()
            save_dia_m_plus(x, y)

            pixmap = QPixmap("diagramsPic/pieS.png")
            self.label_11.setPixmap(pixmap)
            pixmap = QPixmap("diagramsPic/pieC.png")
            self.label_12.setPixmap(pixmap)
            pixmap = QPixmap("diagramsPic/pieM.png")
            self.label_13.setPixmap(pixmap)
            pixmap = QPixmap("diagramsPic/pieMp.png")
            self.label_14.setPixmap(pixmap)
        #СТИЛИ ДЛЯ КНОПОК
        def styleNorm(self, pB: QPushButton):
            styleCSS =  "QPushButton {"
            styleCSS += "  background-color: rgba(0,0,0,0);"
            styleCSS += "  font: 25 10pt \"Bahnschrift Light\";"
            styleCSS += "  color:rgb(193, 193, 193);"
            styleCSS += "  }"
            styleCSS += "QPushButton:hover{"
            styleCSS += "  background-color: rgba(0,0,0,0);"
            styleCSS += "  font: 25 10pt \"Bahnschrift Light\";"
            styleCSS += "  color:rgb(255, 255, 255)}"
            styleCSS += "QPushButton:pressed{"
            styleCSS += "  background-color: rgb(89,191,151);"
            styleCSS += "  font: 25 10pt \"Bahnschrift Light\";"
            styleCSS += "  color:rgb(255,255,255)}"
            pB.setStyleSheet(styleCSS)
        def styleActive(self, pB: QPushButton):
            styleCSS = "QPushButton {"
            styleCSS += "  background-color: rgb(89,191,151);"
            styleCSS += "  font: 25 10pt \"Bahnschrift Light\";"
            styleCSS += "  color:rgb(255,255,255);"
            styleCSS += "  }"
            pB.setStyleSheet(styleCSS)
        def styleButton(self):
            self.pushButton_21.clicked.connect(lambda: self.styleActive(self.pushButton_21))
            self.pushButton_21.clicked.connect(lambda: self.styleNorm(self.pushButton_22))
            self.pushButton_21.clicked.connect(lambda: self.styleNorm(self.pushButton_23))
            self.pushButton_21.clicked.connect(lambda: self.styleNorm(self.pushButton_24))
            self.pushButton_21.clicked.connect(lambda: self.styleNorm(self.pushButton_25))

            self.pushButton_22.clicked.connect(lambda: self.styleActive(self.pushButton_22))
            self.pushButton_22.clicked.connect(lambda: self.styleNorm(self.pushButton_21))
            self.pushButton_22.clicked.connect(lambda: self.styleNorm(self.pushButton_23))
            self.pushButton_22.clicked.connect(lambda: self.styleNorm(self.pushButton_24))
            self.pushButton_22.clicked.connect(lambda: self.styleNorm(self.pushButton_25))

            self.pushButton_23.clicked.connect(lambda: self.styleActive(self.pushButton_23))
            self.pushButton_23.clicked.connect(lambda: self.styleNorm(self.pushButton_21))
            self.pushButton_23.clicked.connect(lambda: self.styleNorm(self.pushButton_22))
            self.pushButton_23.clicked.connect(lambda: self.styleNorm(self.pushButton_24))
            self.pushButton_23.clicked.connect(lambda: self.styleNorm(self.pushButton_25))

            self.pushButton_24.clicked.connect(lambda: self.styleActive(self.pushButton_24))
            self.pushButton_24.clicked.connect(lambda: self.styleNorm(self.pushButton_21))
            self.pushButton_24.clicked.connect(lambda: self.styleNorm(self.pushButton_22))
            self.pushButton_24.clicked.connect(lambda: self.styleNorm(self.pushButton_23))
            self.pushButton_24.clicked.connect(lambda: self.styleNorm(self.pushButton_25))

            self.pushButton_25.clicked.connect(lambda: self.styleActive(self.pushButton_25))
            self.pushButton_25.clicked.connect(lambda: self.styleNorm(self.pushButton_21))
            self.pushButton_25.clicked.connect(lambda: self.styleNorm(self.pushButton_22))
            self.pushButton_25.clicked.connect(lambda: self.styleNorm(self.pushButton_23))
            self.pushButton_25.clicked.connect(lambda: self.styleNorm(self.pushButton_24))

            self.pushButton_9.clicked.connect(lambda: self.styleActive(self.pushButton_9))
            self.pushButton_9.clicked.connect(lambda: self.styleNorm(self.pushButton_10))

            self.pushButton_10.clicked.connect(lambda: self.styleActive(self.pushButton_10))
            self.pushButton_10.clicked.connect(lambda: self.styleNorm(self.pushButton_9))

            self.pushButton_15.clicked.connect(lambda: self.styleActive(self.pushButton_15))
            self.pushButton_15.clicked.connect(lambda: self.styleNorm(self.pushButton_16))

            self.pushButton_16.clicked.connect(lambda: self.styleActive(self.pushButton_16))
            self.pushButton_16.clicked.connect(lambda: self.styleNorm(self.pushButton_15))

            self.pushButton_7.clicked.connect(lambda: self.styleActive(self.pushButton_7))
            self.pushButton_7.clicked.connect(lambda: self.styleNorm(self.pushButton_8))
            self.pushButton_7.clicked.connect(lambda: self.styleNorm(self.pushButton_12))

            self.pushButton_8.clicked.connect(lambda: self.styleActive(self.pushButton_8))
            self.pushButton_8.clicked.connect(lambda: self.styleNorm(self.pushButton_7))
            self.pushButton_8.clicked.connect(lambda: self.styleNorm(self.pushButton_12))

            self.pushButton_12.clicked.connect(lambda: self.styleActive(self.pushButton_12))
            self.pushButton_12.clicked.connect(lambda: self.styleNorm(self.pushButton_7))
            self.pushButton_12.clicked.connect(lambda: self.styleNorm(self.pushButton_8))
        def startStyle(self):
            self.tabWidget.setCurrentIndex(0)
            self.tabWidget_2.setCurrentIndex(0)
            self.tabWidget_3.setCurrentIndex(0)
            self.tabWidget_4.setCurrentIndex(0)

            self.styleActive(self.pushButton_21)
            self.styleActive(self.pushButton_9)
            self.styleActive(self.pushButton_15)
            self.styleActive(self.pushButton_7)

            self.styleNorm(self.pushButton_22)
            self.styleNorm(self.pushButton_23)
            self.styleNorm(self.pushButton_24)
            self.styleNorm(self.pushButton_25)
            self.styleNorm(self.pushButton_10)
            self.styleNorm(self.pushButton_16)
            self.styleNorm(self.pushButton_8)
            self.styleNorm(self.pushButton_12)

            self.styleNorm(self.pushButton_17)
            self.styleNorm(self.pushButton_18)
            # self.styleNorm(self.pushButton_19)
            self.styleNorm(self.pushButton_20)

            self.styleNorm(self.pushButton)
            self.styleNorm(self.pushButton_11)
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.showMaximized()  # Показываем окно
    app.exec_()
if __name__ == '__main__':
    sqlite_start()
    main()