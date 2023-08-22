import pytest
from src.phone import Phone
from src.item import Item


@pytest.fixture
def get_instance_phone():
    return Phone("iPhone 14", 120_000, 5, 2)


def test_init(get_instance_phone):
    """Проверяем инициализация экземпляра класса Phone"""
    # Инициализируем экземпляры класса Phone для тестирования
    phone1 = get_instance_phone
    # Тестируем корректность инициализации параметров, т.ч. через родительский класс Item
    assert str(phone1) == 'iPhone 14'
    assert repr(phone1) == "Phone('iPhone 14', 120000, 5, 2)"
    assert phone1.quantity == 5
    assert phone1.number_of_sim == 2


def test_number_of_sim_setter(get_instance_phone):
    """Проверяем корректность работы сеттера экземпляра класса Phone"""
    # Инициализируем экземпляры класса Phone для тестирования
    phone1 = get_instance_phone

    # Тестируем проверку в сеттере - пытаемся установить количество сим-карт равное 0
    with pytest.raises(ValueError):
        phone1.number_of_sim = 0


def test_add_method(get_instance_phone):
    """Проверяем функцию сложения экземпляров класса Phone и Item"""
    # Инициализируем экземпляры класса Phone для тестирования
    phone1 = get_instance_phone
    phone2 = Phone("iPhone 10", 80_000, 10, 2)
    # Проверяем операцию сложения
    assert phone1 + phone2 == 15

    # Проверяем возможность сложения с экземпляром родительского класса Item
    item_check = Item("Смартфон", 10000, 20)
    assert phone1 + item_check == 25
    assert phone2 + item_check == 30
    assert item_check + phone1 == 25


def test_add_illegal(get_instance_phone):
    """Проверяем невозможность сложения с экземплярами не `Phone` или `Item` классов"""
    phone1 = get_instance_phone

    # Создаем класс IllegalItem в котором есть поле quantity
    class IllegalItem:
        def __init__(self, quantity: int):
            self.quantity = quantity

    # Создаем экземпляр класса IllegalItem
    illegal_item = IllegalItem(20)
    # Пытаемся осуществить сложение экземпляра класса Phone c экземпляром класса IllegalItem
    # и поймать ошибку TypeError, генерируемую декоратором @check_instance_item класса Item
    with pytest.raises(TypeError) as tp_error:
        assert phone1 + illegal_item == 25
    # Дополнительно проверяем сообщение, которое передается при попытке некорректного сложения
    assert str(tp_error.value) == ('Несоответствие типов для проведения арифметических (логических) операций с '
                                   'экземплярами классов!')
