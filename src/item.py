import math
import csv
from os import path as os_path
from pathlib import Path


class InstantiateCSVError(Exception):
    """Класс пользовательского исключения InstantiateCSVError"""
    def __init__(self, message):
        super().__init__(message)


class Item:
    """
    Класс для представления товара в магазине.
    """
    # Аттрибуты класса
    pay_rate = 1.0
    all = []
    csv_file = '..\\src\\items.csv'

    def __init__(self, name: str, price: float, quantity: int) -> None:
        """
        Создание экземпляра класса item.

        :param name: Название товара.
        :param price: Цена за единицу товара.
        :param quantity: Количество товара в магазине.
        """
        super().__init__()
        self.__name = name.strip()
        if not (isinstance(price, float) or isinstance(price, int)):
            raise ValueError('Цена за единицу товара должна быть только числом.')
        if price <= 0:
            raise ValueError('Цена за единицу товара может быть положительным числом!')
        self.price = price
        if not isinstance(quantity, int):
            raise ValueError('Количество товара должно быть только числом.')
        if quantity <= 0:
            raise ValueError('Количество товара может быть только положительным числом"')
        self.quantity = quantity
        Item.all.append(self)

    def calculate_total_price(self) -> float:
        """
        Рассчитывает общую стоимость конкретного товара в магазине.

        :return: Общая стоимость товара.
        """
        return self.price * self.quantity

    def apply_discount(self) -> None:
        """
        Применяет установленную скидку для конкретного товара.
        """
        self.price *= Item.pay_rate

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if len(value) > 10:
            value = value[:10]
        self.__name = value

    @staticmethod
    def string_to_number(value: str) -> int:
        """Статический метод, возвращающий число из числа-строки."""
        float_value = float(value)
        return math.floor(float_value)

    @classmethod
    def get_only_filename(cls):
        """Функция, которая получает 'чистое' имя файла, хранящееся в аттрибуте класса csv_file"""
        return Path(cls.csv_file).name

    @classmethod
    def instantiate_from_csv(cls):
        """Класс-метод инициализации списка элементов класса Item из файла src/items.csv"""
        if not os_path.isfile(cls.csv_file):
            raise FileNotFoundError(f'Отсутствует файл {cls.get_only_filename()}')
        # Обнуляем список объектов класса
        cls.all = []
        with open(Item.csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                read_name = row.get('name')
                read_price = row.get('price')
                read_quantity = row.get('quantity')
                # Файл поврежден, нет какого-то столбца - выбрасываем исключение InstantiateCSVError с именем
                # csv-файла, который не удалось открыть и сбрасываем счетчик экземпляров класса all
                if read_name is None or read_price is None or read_quantity is None:
                    cls.all = []
                    raise InstantiateCSVError(f'Файл {cls.get_only_filename()} поврежден')
                # Все нормально - создаем экземпляр класса Item
                cls(read_name, float(read_price), int(read_quantity))

    @staticmethod
    def check_instance_item(function):
        """Проверяет чтобы второй аргумент функции был экземпляров того же класса, что и первый"""
        def inner(*args, **kwargs):
            if not isinstance(args[1], Item):
                raise TypeError('Несоответствие типов для проведения арифметических '
                                '(логических) операций с экземплярами классов!')
            result = function(*args, **kwargs)
            return result
        return inner

    @check_instance_item
    def __add__(self, other):
        return self.quantity + other.quantity

    def __repr__(self):
        """Магический метод для официального "текстового" образа объекта класса"""
        return f"{self.__class__.__name__}('{self.name}', {self.price}, {self.quantity})"

    def __str__(self):
        """Магический метод для строкового представления объекта класса"""
        return f'{self.name}'
