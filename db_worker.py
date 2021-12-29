from dataclasses import dataclass
import sqlite3


@dataclass
class Armature:
    type: str
    Rs: float
    xi_r: float
    a_r: float


@dataclass
class Concrete:
    type: str
    R: float


class DBWorker:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    
    def get_armature(self, armature_type: str) -> Armature:
        """Возвращает объект арматуры с возможностью получения значений через точку."""
        
        # Делаем запрос по типу арматуры
        request = self.cursor.execute("SELECT Rs, xi_r, a_r FROM armature WHERE type=?", (armature_type,))
        
        # Получаем один результат из курсора
        result = self.cursor.fetchone()
        
        # Если результат равен None, такой арматуры в базе нет, 
        # возвращаем None для последующей обработки в коде
        if result is None:
            return None
        
        # Возвращаем объект арматуры
        return Armature(armature_type, *result)
    
    
    def get_concrete(self, concrete_type: str) -> Concrete:
        """Возвращает объект бетона с возможностью получения значений через точку."""
        
        # Делаем запрос по типу бетона
        request = self.cursor.execute("SELECT R FROM concrete WHERE type=?", (concrete_type,))
        
        # Получаем один результат из курсора
        result = self.cursor.fetchone()
        
        # Если результат равен None, такого бетона в базе нет, 
        # возвращаем None для последующей обработки в коде
        if result is None:
            return None
        
        # Возвращаем объект бетона
        return Concrete(concrete_type, *result)
    
    
    def get_all_concrete(self) -> list[Concrete]:
        # * Делаем запрос к таблице бетона
        # request = self.cursor.execute("SELECT type, Rs, xi_r, a_r FROM armature")
        request = self.cursor.execute("SELECT type, R FROM concrete")
        
        # Получаем все результаты из курсора
        result = self.cursor.fetchall()
        
        # Если результат равен None, бетона в базе нет, 
        # возвращаем None для последующей обработки в коде
        if result is None:
            return None
        
        # Возвращаем объект бетона
        return [Concrete(line[0], line[1]) for line in result]
    
    
    def get_all_armature(self) -> list[Concrete]:
        # Делаем запрос к таблице арматуры
        request = self.cursor.execute("SELECT type, Rs, xi_r, a_r FROM armature")
        
        # Получаем все результаты из курсора
        result = self.cursor.fetchall()
        
        # Если результат равен None, арматуры в базе нет, 
        # возвращаем None для последующей обработки в коде
        if result is None:
            return None
        
        # Возвращаем объект арматуры
        return [Armature(*line) for line in result]


# Пример работы. Будет запускаться только если запущен непосредственно файл
if __name__ == '__main__':
    # Создаём объект класса DBWorker и передаем относительный путь к базе
    # ВНИМАНИЕ! СОЗДАВАТЬ ТОЛЬКО ОДИН РАЗ В КОДЕ!
    # SQL блокирует больше одного соединения в одно время в базе
    db = DBWorker('database.sqlite')
    
    # Получаем арматуру типа A240 из базы
    armature = db.get_armature('A240')
    
    # Получаем бетон типа B15 из базы
    concrete = db.get_concrete('B15')
    
    # Выведем в консоль объекты арматуры и бетона
    print(armature, concrete, sep='\n')
    
    # Получим значение xi_r из объекта арматуры
    xi_r = armature.xi_r
    
    # Получим значение R из объекта бетона
    R = concrete.R
    
    # Выведем полученные значения
    print(f'xi_r арматуры: {xi_r}', f'R бетона: {R}', sep='\n')
    
    # Таким образом можно использовать вызовы в любом месте кода.
    # Самое главное — создать инстанс класса (в данном случае db)
    # где-нибудь, например, в конструкторе, чтобы обращаться именно
    # к нему.