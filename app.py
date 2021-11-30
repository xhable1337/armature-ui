from math import sqrt
from sys import argv

from PyQt5.QtWidgets import QApplication, QMainWindow

import design

# pushButton - кнопка «Рассчитать»
# a_field - поле для ввода a
# b_field - поле для ввода b
# h_field - поле для ввода h
# answer_text - поле для вывода ответа 

class ExampleApp(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.count)

    def __text_to_html(self, text, font_family='Circe', font_size=14):
        return f'''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html>
<head>
    <meta name="qrichtext" content="1" />
    <style type="text/css">
        p, li {{ white-space: pre-wrap; }}
    </style>
</head>
<body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">
<span style=" font-family:'{font_family}'; font-size:{font_size}pt;">{text}</span></p>
</body>
</html>'''

    def set_answer(self, answer, font_family='Circe', font_size=14):
        return self.answer_text.setHtml(self.__text_to_html(answer))

    def count(self):
        As_ = 1005      # мм²  - площадь сечения арматуры, (5Ø16)
        M = 116 * 10**6 # Н·м - изгибающий момент
        Rb = 8.5        # МПа  - тяжёлый бетон класса B15
        N = 160000      # Н   - растягивающая сила
        Rs = 350        # МПа  - продольная арматура класса A400
        alphar = 0.391  # Значение для арматуры А400 (с. 54, таблица 3.3)
        Rsc = Rs

        As = 0          # Ответ

        try:
            fields = (self.a_field.text(), self.b_field.text(), self.h_field.text())
            a, b, h = tuple(map(int, fields))
            a_ = a
        except ValueError:
            if fields == ('', '', ''):
                self.a_field.setText('35')
                self.b_field.setText('1000')
                self.h_field.setText('200')
                a, b, h = 35, 1000, 200
                a_ = a
            else:
                self.set_answer('Введены не числа. Повторите попытку.')
                return
        
        h0 = h - a       # мм
        e0 = M/N         # мм
        e = e0 - h/2 + a # мм
        e_ = e0+ h/2 - a # мм

        try:
            if e_ <= h0 - a_:
                print(f"e\' <= h0 - a'")
                As = (N*e_) / (Rs * (h0 - a_)) # мм² - ответ
            else:
                print("e > h0 - a\'")
                alpham: float = round((N*e - Rsc * As_ * (h0 - a_)) / (Rb * b * h0 * h0), 3)
                if alpham < 0:
                    print(f'alpham == {alpham} < 0')
                    As = round((N*e_) / (Rs * (h0 - a_)), 3) # мм² - ответ
                elif 0 < alpham < alphar:
                    print(f'0 < alpham = {alpham} < alphar = {alphar}')
                    xi = round(1 - sqrt(1 - 2 * alpham), 3)
                    As = round((((xi * b * h0 * Rb) + N) / Rs) + (As_ * (Rsc / Rs)), 3) # мм² - ответ
                else:
                    self.set_answer(f'Так как αₘ > αᵣ, вам следует увеличить размеры сечения.')
                    return
        except ZeroDivisionError:
            self.set_answer(f'Обнаружено деление на ноль. Измените входные данные.')
            return
        
        if As > 0:
            self.set_answer(f'{As} мм²')
        else:
            self.set_answer(
                f'Получено отрицательное значение ({As}). '
                'Следует принять площадь сечения арматуры с учетом конструктивных требований '
                'и минимального % армирования в зависимости от гибкости элемента.',
                font_size=10
            )


def main():
    app = QApplication(argv) 
    window = ExampleApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()