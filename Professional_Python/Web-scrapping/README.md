# Задание «Web-scrapping»

## Задание 1

Нужно парсить страницу со свежими статьями ([HABR](https://habr.com/ru/all/)) и выбирать те статьи, 
в которых встречается хотя бы одно из ключевых слов. Эти слова определяем в начале скрипта. 
Поиск вести по всей доступной preview-информации, т. е. по информации, доступной с текущей страницы. 
Выведите в консоль список подходящих статей в формате: 

<дата> – <заголовок> – <ссылка>.

```python
# Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# Код
```

Код [main.py](/Professional_Python/Web-scrapping/main.py) Результат [articles.json](/Professional_Python/Web-scrapping/articles.json)

## Задание 2

Улучшить скрипт так, чтобы он анализировал не только preview-информацию статьи, но и весь текст статьи целиком.

Для этого потребуется получать страницы статей и искать по тексту внутри этой страницы.

Код [improved.py](/Professional_Python/Web-scrapping/improved.py) Результат [improved.json](/Professional_Python/Web-scrapping/improved.json)

