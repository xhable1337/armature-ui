from math import sqrt
from sys import argv

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QPixmap
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QGraphicsPixmapItem, QGraphicsScene

from ui import mainwindow
from resources import resource_path, Values
from db_worker import DBWorker


class ExampleApp(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        """Метод инициализации интерфейса."""
        super().__init__()
        
        # Подключение шрифтов
        QFontDatabase.addApplicationFont(resource_path('fonts/circe.ttf'))
        QFontDatabase.addApplicationFont(resource_path('fonts/circe-bold.ttf'))
        QFontDatabase.addApplicationFont(resource_path('fonts/circe-extrabold.ttf'))
        
        self.setupUi(self)
        
        # Подключение клавиши расчёта к функции
        self.pushButton.clicked.connect(self.count)

        # Создание инстанса класса для взаимодействия с базой данных
        self.db = DBWorker(resource_path('database.sqlite'))
        
        # Создание сцены для картинки
        pixmap = QPixmap()
        pixmap.load(resource_path('img/picture.png'))
        item_picture = QGraphicsPixmapItem(pixmap)
        self.scene_picture = QGraphicsScene(self)
        self.scene_picture.addItem(item_picture)
        self.graphicsView_2.setScene(self.scene_picture)
    
    
    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        """Вписывает сцену в graphicsView при изменении размеров окна."""
        self.graphicsView_2.fitInView(self.scene_picture.itemsBoundingRect(), Qt.KeepAspectRatio)
        return super().resizeEvent(e)


    def __text_to_html(self, text, font_family='Circe', font_size=14):
        """Возвращает HTML-разметку для поля вывода ответа с переданным текстом text."""
        return f'''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html>
<head>
    <meta name="qrichtext" content="1" />
    <style type="text/css">
        p, li {{ white-space: pre-wrap; }}
    </style>
</head>
<body style=" font-family:'{font_family}'; font-size:{font_size}pt; font-weight:400; font-style:normal; color: white">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">
<span style=" font-family:'{font_family}'; font-size:{font_size}pt; color: white">{text}</span></p>
</body>
</html>'''
    
    
    @staticmethod
    def __get_float_field(field: QLineEdit):
        try:
            return float(field.text())
        except ValueError:
            if field.text() == '':
                field.setText(field.placeholderText())
                return float(field.placeholderText())
            else:
                return None


    def __get_numbers_from_fields(self) -> Values:
        """Возвращает датакласс значений, введённых в поля.
        Если в полях введён текст, возвращает None."""
        
        concrete_type = self.concrete_type_3.currentText()
        armature_type = self.armature_type_3.currentText()
        fields = (
            self.a_field_3, 
            self.b_field_3, 
            self.h_field_3,
            self.M_field_3,
            self.N_field,
            self.As__field,
        )
        
        values = tuple((self.__get_float_field(field) for field in fields))
        
        if None in values:
            return None
        
        if len(values) == 6:
            return Values(*values, concrete_type, armature_type)
        else:
            return Values(*values[:-1], concrete_type, armature_type, values[-1])


    def set_answer(self, answer: str, font_family='Circe', font_size=14):
        """Устанавливает ответ answer в поле ответа."""
        answer = answer.replace('\n', '<br>')
        return self.answer_text_3.setHtml(self.__text_to_html(answer, font_family, font_size))


    def count(self):
        # ! Values(a, b, h, M, N, As_, concrete_type, armature_type=)
        # Получение и валидация введённых значений
        fields = self.__get_numbers_from_fields()
        
        if fields == None:
            # Если в строках введён текст, а не числа, пишем об этом в поле ответа
            return self.set_answer('Введены не числа. Повторите попытку.')
        else:
            fields.M *= 10**6
            fields.N *= 10**3
            # Если введены числа, продолжаем расчёты
            a, b, h, M, N, As_ = fields.a, fields.b, fields.h, fields.M, fields.N, fields.As_
            a_ = a

            if a > h:
                return self.set_answer('Значение a не может быть больше h. Повторите попытку.')
        
        current_armature = self.db.get_armature(fields.armature_type)
        current_concrete = self.db.get_concrete(fields.concrete_type)
        
        Rsc = Rs = current_armature.Rs   # МПа
        αr = current_armature.a_r        # Значение αr для арматуры 
        Rb = current_concrete.R          # МПа
        
        As = 0           # Ответ
        h0 = h - a       # мм
        e0 = M/N         # мм
        e = e0 - h/2 + a # мм
        e_ = e0+ h/2 - a # мм

        try:
            if e_ <= h0 - a_:
                print(f"e\' <= h0 - a'")
                As = round((N*e_) / (Rs * (h0 - a_)), 3) # мм² - ответ
            else:
                print("e > h0 - a\'")
                αm: float = round((N*e - Rsc * As_ * (h0 - a_)) / (Rb * b * h0 * h0), 3)
                if αm < 0:
                    print(f'αm == {αm} < 0')
                    As = round((N*e_) / (Rs * (h0 - a_)), 3) # мм² - ответ
                elif 0 < αm < αr:
                    print(f'0 < αm = {αm} < αr = {αr}')
                    xi = round(1 - sqrt(1 - 2 * αm), 3)
                    As = round((((xi * b * h0 * Rb) + N) / Rs) + (As_ * (Rsc / Rs)), 3) # мм² - ответ
                else:
                    self.set_answer(f'Так как αₘ > αᵣ, вам следует увеличить размеры сечения, размеры As или повысить класс бетона.')
                    return
        except ZeroDivisionError:
            self.set_answer(f'Обнаружено деление на ноль. Измените входные данные.')
            return
        
        if As > 0:
            self.set_answer(f'Площадь сечения арматуры: {As} мм²')
        else:
            self.set_answer(
                f'Получено отрицательное значение ({As}). '
                'Следует принять площадь сечения арматуры с учетом конструктивных требований '
                'и минимального % армирования в зависимости от гибкости элемента.',
                font_size=10
            )


def main():
    app = QApplication(argv)
    
    # Открытие QSS файла
    with open(resource_path("ui/Darkeum.qss"), "r") as file:
        qss = file.read()
        app.setStyleSheet(qss)
    
    window = ExampleApp()
    window.show()
    window.graphicsView_2.fitInView(window.scene_picture.itemsBoundingRect(), Qt.KeepAspectRatio)
    app.exec_()


if __name__ == '__main__':
    main()