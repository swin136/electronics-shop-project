import pytest
from src.keyboard import Keyboard


def test_keyboard_instance():
    """Проверяем правильность функционирования экземпляра класса Keyboard"""
    kb = Keyboard('Dark Project KD87A', 9600, 5)
    # Проверяем корректность гетера, наследованного от класса Item
    assert str(kb) == 'Dark Project KD87A'
    # Проверяем корректность гетера, наследованного от класса-миксина Keyboard
    assert str(kb.language) == "EN"

    # Вызываем метод смены раскладки клавиатуры
    kb.change_lang()
    assert str(kb.language) == "RU"

    # Сделали последовательно смену раскладок RU -> EN -> RU
    kb.change_lang().change_lang()
    assert str(kb.language) == "RU"
    # Проверяем, что смена раскладки клавиатуры через свойство невозможно
    with pytest.raises(AttributeError):
        kb.language = 'CH'
