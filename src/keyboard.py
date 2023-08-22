from src.item import Item


class KeyboardLayoutMixin:
    """Класс-миксин для реализации функционала хранению и изменению раскладки клавиатуры """
    def __init__(self):
        # Устанавливаем раскладку клавиатуры
        self.__language = "EN"

    @property
    def language(self):
        return self.__language

    def change_lang(self):
        if self.__language == 'EN':
            self.__language = 'RU'
        else:
            self.__language = 'EN'
        return self


class Keyboard(Item, KeyboardLayoutMixin):
    """Класс для товара 'клавиатура'"""
    def __init__(self, name: str, price: float, quantity: int):
        super().__init__(name, price, quantity)
