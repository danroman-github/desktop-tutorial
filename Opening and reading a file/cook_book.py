import pprint

# Функция подсчета строк
def count_lines(recipes):
    with open(recipes) as f:
        content = f.read()
        len_f = content.count('\n')
        return len_f


def create_cook_book(recipes):

    with open(recipes) as f:
        len_f = count_lines(recipes)
        cook_book = {}
        counter = 0

        while counter < len_f:
            dish = f.readline().strip()
            counter += 1

            if dish:
                quantity = int(f.readline().strip())
                counter += 1
                ingredients = []

                for _ in range(quantity):
                    ing_line = f.readline().strip()
                    name, quantity, measure = map(str.strip, ing_line.split('|'))
                    counter += 1
                    ingredients.append({
                        'ingredient_name': name,
                        'quantity': int(quantity),
                        'measure': measure
                    })

                cook_book[dish] = ingredients
            else:
                counter += 1
    return cook_book


def get_shop_list_by_dishes(dishes, person_count, cook_book):
    shop_list = {}

    for dish in dishes:

        if dish in cook_book:
            
            for ingredient in cook_book[dish]:
                quantity = ingredient['quantity'] * person_count

                if ingredient['ingredient_name'] in shop_list:
                    shop_list[ingredient['ingredient_name']]['quantity'] += quantity
                else:
                    shop_list[ingredient['ingredient_name']] = {
                        'quantity': quantity,
                        'measure': ingredient['measure']
                    }

    return shop_list


cook_book = create_cook_book('recipes.txt')
pprint.pprint(cook_book)

dishes = ['Запеченный картофель', 'Омлет']
person_count = 2
shop_list = get_shop_list_by_dishes(dishes, person_count, cook_book)
pprint.pprint(shop_list)