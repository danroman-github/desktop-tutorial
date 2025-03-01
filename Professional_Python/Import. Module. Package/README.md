# Задание «Import. Module. Package»

## Задание 1

Разработать структуру программы «Бухгалтерия»:

[main.py](/Professional_Python/Import.%20Module.%20Package/main.py)

[application/salary.py](/Professional_Python/Import.%20Module.%20Package/application/salary.py)

[application/db/people.py](/Professional_Python/Import.%20Module.%20Package/application/db/people.py)

Main.py — основной модуль для запуска программы. В модуле salary.py функция calculate_salary. В модуле people.py функция get_employees.

## Задание 2

Импортировать функции в модуль main.py и вызывать эти функции в конструкции.

```python
if __name__ == '__main__':
```

Сами функции реализовывать не нужно. Достаточно добавить туда какой-либо вывод.

## Задание 3

Познакомиться с модулем datetime. При вызове функций модуля main.py выводить текущую дату.

## Задание 4

Найти интересный для себя пакет на pypi и в файле [requirements.txt](/Professional_Python/Import.%20Module.%20Package/requirements.txt) указать его с актуальной версией. При желании можно написать программу с этим пакетом.

## Общие советы

- Параметры подключения к БД следует выносить в отдельные переменные: логин, пароль, название БД и пр.
- Загружать значения лучше из окружения ОС, например, через `os.getenv()`.
- Заполнять данными можно вручную или выполнить необязательное задание 3.
