from src.item import Item
from src.item import InstantiateCSVError

if __name__ == '__main__':
    # Файл items.csv отсутствует.
    Item.csv_file = '..\\src\\no_items.csv'
    try:
        Item.instantiate_from_csv()
    except FileNotFoundError as file_not_exists_err:
        print(file_not_exists_err)
    # FileNotFoundError: Отсутствует файл item.csv

    # В файле items_3.csv удалена последняя колонка.
    Item.csv_file = '..\\src\\items_3.csv'
    try:
        Item.instantiate_from_csv()
    except InstantiateCSVError as inst_csv_error:
        print(inst_csv_error)
    # InstantiateCSVError: Файл item.csv поврежден
