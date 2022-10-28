
import sys
import sqlite3

import PyQt5
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

conn = sqlite3.connect('class_beton.db')
cur = conn.cursor()
# cur.execute("""CREATE TABLE IF NOT EXISTS beton(
#    class TEXT,
#    mean TEXT);
# """)
# conn.commit()
# all_beton = [('B15', '8.5'), ('B20', '11.5'), ( 'B25', '14.5'),('B30', '17'),
#              ('B35', '19.5'),('B40', '22'),
#              ('B45', '25'), ('B50', '27.5'), ('B55', '30'), ('B60', '33')]
# cur.executemany("INSERT INTO beton VALUES(?, ?);", all_beton)
# conn.commit()
cur.execute("SELECT * FROM beton;")
one_result = cur.fetchall()

class Calc(QWidget):
    def __init__(self):
        super().__init__()
        self.setting_calc()

    def setting_calc(self):
        uic.loadUi("Calculating.ui", self)
        self.setWindowTitle('Результат')
        self.pushButton.clicked.connect(self.input_A_s)

    def input_A_s(self):
        self.take_A_s = Asform()
        self.take_A_s.show()

    def returnres(self, result):
        self.textedit.setText(result)
        text = open('zxc.txt')
        history = text.read()
        text.close()
        with open('zxc.txt', 'w'): pass

        text = open('zxc.txt', 'a+')
        text.write(result)
        text.write(history)
        text.close()


class Help(QWidget):
    def __init__(self):
        super().__init__()
        self.setting_help()

    def setting_help(self):
        uic.loadUi("help.ui", self)
        self.setWindowTitle('Помощь')
        self.textEdit.setText("1) Посмотрите допустимые значениями,"
                              " нажав на кнопку 'Допустимые значения переменных'.\n"
                              "2) Начинайте вводить переменные."
                              "выберите класс бетона и арматуры. "
                              "3) После нажмите на 'Вычислить'.\n"
                              "4) Для просмотра текствого файла"
                              " куда записывается история ваших "
                              "вычислений нажмите на кнопку 'Содержимое текствого файла'.\n"
                              "5) Для очистки текстового "
                              "файла используйте кнопку 'Очистить текстовый файл'.\n"
                              "6) Чтобы стереть заполненные вамиполя, "
                              "нажмите на кнопку 'Очистить заполненные поля'.")
        self.info.clicked.connect(self.info_about)
        self.instuction.clicked.connect(self.instraction_use)
        self.limit.clicked.connect(self.limit_mean)

    def info_about(self):
        string = "H - высота колонны.\n" \
                 "Продольная сила и изгибающие моменты в опорном сечении " \
                 "от вертикальных нагрузок: полная N_v, M_v," \
                 " постоянных и длительных: N_l, M_l.\n" \
                 "Тяжёлый бетон: от B15 до B60 включительно.\n" \
                 "Арматура: от A240 до A500 включительно.\n"

        self.textEdit.setText(string)

    def limit_mean(self):
        strin = "Значения должны быть от 0 до 10000, включая 0 и 10000"
        self.textEdit.setText(strin)

    def instraction_use(self):
        self.textEdit.setText("1) Посмотрите допустимые значениями,"
                              " нажав на кнопку 'Допустимые значения переменных'.\n"
                              "2) Начинайте вводить переменные."
                              "выберите класс бетона и арматуры. "
                              "3) После нажмите на 'Вычислить'.\n"
                              "4) Для просмотра текствого "
                              "файла куда записывается история ваших "
                              "вычислений нажмите на кнопку 'Содержимое текствого файла'.\n"
                              "5) Для очистки текстового "
                              "файла используйте кнопку 'Очистить текстовый файл'.\n"
                              "6) Чтобы стереть заполненные вамиполя, "
                              "нажмите на кнопку 'Очистить заполненные поля'.")


class Asform(QWidget):
    def __init__(self):
        super().__init__()
        self.setting_asform()

    def setting_asform(self):
        uic.loadUi("A_sForm.ui", self)
        self.setWindowTitle('Таблица значений A_s')


class HistoryCalc(QWidget):
    def __init__(self):
        super().__init__()
        self.settingHistoryCalc()

    def settingHistoryCalc(self):
        uic.loadUi("histirycalc.ui", self)
        self.setWindowTitle('Содержимое текстового файла')

    def concatStr(self):
        text = open('zxc.txt')
        a = text.read()
        text.close()
        result = a
        self.textedit1.setText(self.textedit1.toPlainText() + result + '\n')


class BuildingCalc(QMainWindow):
    def __init__(self):
        super().__init__()
        self.string_result = ''
        self.settingBuildCalc()
        self.res = ''
        self.R_s = 350
        self.R_sc = 350
        self.R_b = 14.5

    def settingBuildCalc(self):
        uic.loadUi("Mainwindow.ui", self)
        self.setWindowTitle("Проверка прочности опорного сечения колонны")

        self.calculating.clicked.connect(self.print_result)
        self.history_calc.clicked.connect(self.show_history)
        self.clear.clicked.connect(self.clear_data)
        self.btn_clear_file.clicked.connect(self.clear_file)
        self.help.clicked.connect(self.help_form)

        for i in one_result:
            self.comboBox.addItem(i[0])

        self.comboBox.activated[str].connect(self.selectcombobeton)

        self.comboBox_2.addItem("A240")
        self.comboBox_2.addItem("A400")
        self.comboBox_2.addItem("A500")
        self.comboBox_2.activated[str].connect(self.selectcomboarmatura)

    def selectcombobeton(self):
        self.meanbox = str(self.comboBox.currentText())
        for i in one_result:
            if self.meanbox == i[0]:
                self.R_b = i[1]

    def selectcomboarmatura(self):
        self.meanbox = str(self.comboBox_2.currentText())
        if self.meanbox == "A240":
            self.R_s = 210
            self.R_sc = 210
        elif self.meanbox == "A400":
            self.R_s = 340
            self.R_sc = 340
        elif self.meanbox == "A500":
            self.R_s = 435
            self.R_sc = 435

    def take(self, result):
        self.res1 = result

    def help_form(self):
        self.help = Help()
        self.help.show()

    def show_history(self):
        self.history_result = HistoryCalc()
        self.history_result.concatStr()
        self.history_result.show()

    def clear_data(self):
       self.first_size.clear()
       self.second_size.clear()
       self.five.clear()
       self.six.clear()
       self.seven.clear()
       self.eight.clear()
       self.eight_2.clear()

    def clear_file(self):
        with open('zxc.txt', 'w'): pass

    def print_result(self):
        self.calc = Calc()
        self.a1 = self.first_size.text()
        self.a2 = self.second_size.text()
        self.N_v = self.five.text()
        self.M_v = self.six.text()
        self.N_l = self.seven.text()
        self.M_l = self.eight.text()
        self.h_size = self.eight_2.text()

        if not self.a1.strip() or not self.a2.strip() \
                or not self.N_v.strip() \
                or not self.M_v.strip() or not self.N_l.strip() \
                or not self.M_l.strip() or not self.h_size.strip():
            self.string_result += ("Проверьте все ли поля заполнены!!!\n\n")
            self.take(self.string_result)

        elif self.a1.isdigit() == False or self.a2.isdigit() == False \
                or self.N_v.isdigit() == False \
                or self.M_v.isdigit() == False or self.N_l.isdigit() == False \
                or self.M_l.isdigit() == False or self.h_size.isdigit() == False:
            self.string_result = ("Не все поля, введённые "
                                  "вами, являются числами!\n")
            self.take(self.string_result)
        elif (float(self.a1) < 0 or float(self.a1) > 10000) or \
                (float(self.a2) < 0 or float(self.a2) > 10000) or \
                (float(self.N_v) < 0 or float(self.N_v) > 10000) or \
                (float(self.M_v) < 0 or float(self.M_v) > 10000) or \
                (float(self.N_l) < 0 or float(self.N_l) > 10000) or \
                (float(self.M_l) < 0 or float(self.M_l) > 10000) or \
                (float(self.h_size) < 0 or float(self.h_size) > 10000):
            self.string_result = ("Вы вышли за диапазон допустимых значений,\n"
                                  " пожалуйста ознакомьтесь "
                                  "с допустимыми значениями в разделе Помощь ")
        else:
            self.a1 = float(self.first_size.text())
            self.a2 = float(self.second_size.text())
            self.N_v = float(self.five.text())
            self.M_v = float(self.six.text())
            self.N_l = float(self.seven.text())
            self.M_l = float(self.eight.text())
            self.h_size = float(self.eight_2.text())

            self.string_result += f"Исходные переменные:" \
                                  f" размер колонны = {self.a1} x {self.a2} cм, " \
                                  f"R_b = {self.R_b} МПа, " \
                                  f"R_s = R_sc = {self.R_s} МПа, A_s " \
                                  f"N_v = {self.N_v} кH, M_v = {self.M_v} кH*м, " \
                                  f"N_l = {self.N_l} кH, M_l = {self.M_l} кH*м, " \
                                  f" H = {self.h_size} м.\n"
            e_0 = round(int(self.M_v) / int(self.N_v), 3)
            e_0_r = e_0*1000
            l_0 = self.h_size*1000
            h = 400
            e_a = round(h/30, 1)
            fi_b1 = 0.83
            fi_b2 = 0.875
            self.string_result += f"Расчет. Поскольку колонна закреплена" \
                              f" с обоих концов шарнирно опёртыми" \
                  f"ригелями, принимаем, согласно 3.2.42," \
                                  f" а) расчётную длину колонны равной" \
                  f" l_0 = H = {self.h_size} м. Тогда l_0/h = {self.h_size}/0,4 = " \
                  f" {int(self.h_size) / 0.4} > 4, " \
                  f"т.е. учет прогиба колонны обязателен." \
                  f"Эксцентриситет продольной силы от всех нагрузок равен e_0 = M_v/N_v" \
                  f" = {self.M_v} / {self.N_v} = {e_0} м = {int(e_0_r)} мм." \
                  f"Поскольку h / 30 = {h} / 30 = {round(h/30, 1)} > l_0 / 600 = " \
                  f"{l_0} / 600 = {round(l_0/600, 2) }мм, согласно 3.2.46 случайный эксцентриситет" \
                  f" принимаем равным e_a= {e_a} мм > е0. Следовательно, " \
                  f"расчет колонны производим на" \
                                  f" действие продольной силы с эксцентриситетом" \
                  f"e_0 = e_a cогласно 3.2.45." \
                                  f" Из таблицы 3.5 при длительном действии нагрузки" \
                  f"fi_b = {fi_b1}, при кратковременном действии нагрузки fi_b = {fi_b2}." \
                  f"Из условия (3.99) находим при кратковременном действии нагрузки:"
            N1 = self.N_v*1000
            N2 = self.N_l*1000
            A_s_tot1 = ((N1/fi_b2)-float(self.R_b) * float(self.a1) * float(self.a2)) / float(self.R_sc)
            self.string_result += f"A_s,tot = ((N/fi)-R_b*A)/R_sc =" \
                                  f" (({N1}/{fi_b2})-{self.R_b} * " \
                                  f"{self.a1} * {self.a2} / " \
                                  f"{self.R_sc} = {round(A_s_tot1, 0)} мм^2."
            A_s_tot2 = ((N2 / fi_b1) - 0.9 * float(self.R_b) *
                        self.a1 * self.a2) / float(self.R_sc)
            self.string_result += f"A_s,tot = " \
                                  f"((N/fi)-R_b*A)/R_sc =" \
                                  f" (({N1}/{fi_b2})-{self.R_b} * " \
                                  f"{self.a1} * {self.a2}" \
                                  f" / {self.R_sc} = {round(A_s_tot2, 0)} мм^2."
            self.string_result += "Окончательно принимаем A_s,tot смотри таблицу."
        self.take(self.string_result)
        self.calc.returnres(self.res1)
        self.calc.show()
        self.string_result = ''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BuildingCalc()
    ex.show()
    sys.exit(app.exec())
