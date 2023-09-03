from src.item import Item


class Phone(Item):
    """
    Класс для представления телефона в магазине.
    """
    def __init__(self, name: str, price: float, quantity: int, number_of_sim: int) -> None:
        """
           Создание экземпляра класса Phone.

           :param name: Название товара.
           :param price: Цена за единицу товара.
           :param quantity: Количество товара в магазине.
           :param number_of_sim: Количество сим-карт в телефоне.
           """
        super().__init__(name, price, quantity)
        self.__number_of_sim = number_of_sim

    @property
    def number_of_sim(self):
        return self.__number_of_sim

    @number_of_sim.setter
    def number_of_sim(self, value: int):
        if value <= 0:
            raise ValueError('Количество физических SIM-карт должно быть целым числом больше нуля.')
        self.__number_of_sim = value

    def __repr__(self):
        """Магический метод для официального "текстового" образа объекта класса"""
        return (f"{self.__class__.__name__}('{self.name}', {self.price}, {self.quantity}, "
                f"{self.number_of_sim})")
