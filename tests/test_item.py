"""Здесь надо написать тесты с использованием pytest для модуля item."""
import pytest
from src.item import Item
from src.item import InstantiateCSVError


def test_count_objects():
    """Тестируем счетчик количества объектов экземпляров класса Item и корректность хранения объектов"""
    # Тестируем счетчик
    Item("Телевизор", 12500, 220)
    Item("Ноутбук", 70000, 15)
    Item("Смартфон", 21000, 20)
    assert len(Item.all) == 3

    # Тестируем правильность записи объектов в список Item.all
    assert Item.all[1].name == "Ноутбук"


@pytest.fixture
def get_test_item():
    return Item("Телевизор", 12500, 220)


def test_legal_item(get_test_item):
    """Когда мы создаем экземпляр класса и проверяем корректность присвоения значениям полей экземпляра класса:
    - name: Название товара
    - price: Цена за единицу товара
    - quantity: Количество товара в магазине
    """
    assert get_test_item.name == "Телевизор"
    assert get_test_item.price == 12500
    assert get_test_item.quantity == 220


def test_legal_item_calc_methods(get_test_item):
    """Когда мы создаем экземпляр класса и проверяем корректность методов экземпляра класса:
    - calculate_total_price(): расчет общей стоимости конкретного товара в магазине
    - apply_discount(): применение установленной скидки для конкретного товара
    """
    assert get_test_item.calculate_total_price() == 2_750_000
    Item.pay_rate = 0.75
    get_test_item.apply_discount()
    assert get_test_item.price == 9375


def test_item_price_not_positive():
    """Когда мы создаем экземпляр класса с отрицательным значением цены за единицу товара, вернется ошибка."""
    with pytest.raises(ValueError):
        Item("Телевизор", -10000, 220)


def test_item_quantity_not_positive():
    """Когда мы создаем экземпляр класса с отрицательным значением количества товара, вернется ошибка."""
    with pytest.raises(ValueError):
        Item("Телевизор", 10000, -220)


def test_item_quantity_not_int():
    """Когда мы создаем экземпляр класса с нечисловым значением количества товара, вернется ошибка."""
    with pytest.raises(ValueError):
        Item("Телевизор", 10000, 'test_quantity')


def test_item_price_not_float():
    """Когда мы создаем экземпляр класса с нечисловым значением цены за единицу товара, вернется ошибка."""
    with pytest.raises(ValueError):
        Item("Телевизор", '20000', 220)


def test_string_to_number():
    """Тестируем статический метод, возвращающий число из числа-строки."""
    assert Item.string_to_number('5') == 5
    assert Item.string_to_number('5.0') == 5
    assert Item.string_to_number('5.5') == 5


def test_name_getter(get_test_item):
    """Тестируем работу сеттера name"""
    # Отрезаем первые 10 символов названия товарной позиции
    get_test_item.name = 'СуперСмартфон'
    assert get_test_item.name == 'СуперСмарт'


def test_instantiate_from_csv():
    """Тестируем инициализацию списка элементов класса Item из файла src/items.csv"""
    Item.instantiate_from_csv()
    # Общее количество элементов в загруженном списке
    assert len(Item.all) == 5
    # Проверяем корректность загрузки первого элемента
    item_test = Item.all[0]
    assert item_test.name == 'Смартфон'
    # Проверяем корректность загрузки четвертого элемента
    item_test = Item.all[3]
    assert item_test.name == 'Мышка'
    assert item_test.price == 50


def test_repr_method(get_test_item):
    """Тестируем магический метод __repr__"""
    item1 = Item("Смартфон", 12000, 30)
    assert repr(item1) == "Item('Смартфон', 12000, 30)"
    item2 = Item("Планшет", 25000, 18)
    assert repr(item2) == "Item('Планшет', 25000, 18)"
    assert repr(get_test_item) == "Item('Телевизор', 12500, 220)"

    # Тестируем магический метод __repr__ у экземпляра класса-потомка
    class ItemNew(Item):
        ...

    test_item = ItemNew("Монитор", 11500, 30)
    assert repr(test_item) == "ItemNew('Монитор', 11500, 30)"


def test_str_method(get_test_item):
    """Тестируем магический метод __str__"""
    assert str(get_test_item) == "Телевизор"
    item1 = Item("Смартфон", 12000, 30)
    assert str(item1) == "Смартфон"


def test_add_method():
    """Проверяем функцию сложения экземпляров класса Item"""
    # Инициализируем экземпляры класса Item для последующего сложения
    item1 = Item("Смартфон", 12000, 30)
    item2 = Item("Планшет", 25000, 18)
    # Осуществляем сложение экземпляров класса Item
    assert item1 + item2 == 48


def test_add_illegal():
    """Проверяем невозможность сложения с экземплярами не `Item` классов"""
    # Инициализируем экземпляр класса Item для последующего сложения
    item_check = Item("Смартфон", 12000, 30)

    # Создаем класс IllegalItem в котором есть поле quantity
    class IllegalItem:
        def __init__(self, quantity: int):
            self.quantity = quantity

    # Создаем экземпляр класса IllegalItem
    illegal_item = IllegalItem(20)
    # Пытаемся осуществить сложение экземпляра класса Item c экземпляром класса IllegalItem
    # и поймать ошибку TypeError, генерируемую декоратором @check_instance_item класса Item
    with pytest.raises(TypeError) as tp_error:
        assert item_check + illegal_item == 50

    # Дополнительно проверяем сообщение, которое передается при попытке некорректного сложения
    assert str(tp_error.value) == ('Несоответствие типов для проведения арифметических (логических) операций с '
                                   'экземплярами классов!')


def test_load_data_from_non_exist_file():
    """Проверяем появление исключения FileNotFoundError при отсутствии csv-файла с данными для инициализации списка
    элементов класса Item"""
    # Присваиваем аттрибуту класса имя несуществующего файла
    Item.csv_file = '..\\src\\no_items.csv'
    # Формируем сообщение, которое передается вместе вызовом исключения FileNotFoundError
    error_msg = f'Отсутствует файл {Item.get_only_filename()}'
    with pytest.raises(FileNotFoundError) as file_not_exists_err:
        Item.instantiate_from_csv()
    # Проверяем сообщение, которое передается при вызове исключения FileNotFoundError
    assert str(file_not_exists_err.value) == error_msg


def test_load_data_from_corrupt_file():
    """Проверяем появление исключения InstantiateCSVError при загрузке данных для инициализации списка элементов класса
    Item из поврежденных csv-файлов"""
    # В файле items_3.csv удалена вторая колонка.
    Item.csv_file = '..\\src\\items_2.csv'
    # Формируем сообщение, которое передается вместе вызовом исключения InstantiateCSVError
    error_msg = f'Файл {Item.get_only_filename()} поврежден'
    with pytest.raises(InstantiateCSVError) as inst_csv_error:
        Item.instantiate_from_csv()
    # Проверяем сообщение, которое передается при вызове исключения InstantiateCSVError
    assert str(inst_csv_error.value) == error_msg

    # В файле items_3.csv удалена последняя колонка.
    Item.csv_file = '..\\src\\items_3.csv'
    # Формируем сообщение, которое передается вместе вызовом исключения InstantiateCSVError
    error_msg = f'Файл {Item.get_only_filename()} поврежден'
    with pytest.raises(InstantiateCSVError) as inst_csv_error:
        Item.instantiate_from_csv()
    # Проверяем сообщение, которое передается при вызове исключения InstantiateCSVError
    assert str(inst_csv_error.value) == error_msg
