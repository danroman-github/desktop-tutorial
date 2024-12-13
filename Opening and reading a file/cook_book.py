import os
import pprint


def create_cook_book(file_name):
    """Создаёт словарь рецептов из файла."""
    cook_book = {}
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"Файл {file_name} не найден.")

    with open(file_name,'r', encoding='utf-8') as f:
        while True:
            dish = f.readline().strip()

            if not dish:
                break
            try:
                quantity = int(f.readline().strip())
            except ValueError:
                raise ValueError(f"Ошибка в формате файла рецептов для блюда {dish}")

            ingredients = []

            for _ in range(quantity):
                ing_line = f.readline().strip()
                try:
                    name, quantity, measure = map(str.strip, ing_line.split('|'))
                except ValueError:
                    raise ValueError(f"Ошибка в строке ингридиента: {ing_line}")

                ingredients.append({
                    'ingredient_name': name,
                    'quantity': int(quantity),
                    'measure': measure
                })

            cook_book[dish] = ingredients
            f.readline()
    return cook_book


def get_shop_list_by_dishes(dishes, person_count, cook_book):
    """Расчёт ингредиентов для заданных блюд на указанное количество персон."""
    shop_list = {}
    for dish in dishes:
        if dish not in cook_book:
            print(f"Блюдо '{dish}' отсутствует в книге рецептов.")
            continue
            
        for ingredient in cook_book[dish]:
            name  = ingredient['ingredient_name']
            if name in shop_list:
                shop_list[name]['quantity'] += ingredient['quantity'] * person_count
            else:
                shop_list[name] = {
                    'quantity': ingredient['quantity'] * person_count,
                    'measure': ingredient['measure']
                }
    return shop_list


recipes = 'recipes.txt'
cook_book = create_cook_book(recipes)
pprint.pprint(cook_book)

dishes = ['Запеченный картофель', 'Омлет']
person_count = 2
shop_list = get_shop_list_by_dishes(dishes, person_count, cook_book)
pprint.pprint(shop_list)