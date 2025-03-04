# Задание «Regular expressions»
## Задача

Привести в порядок адресную книгу [phonebook_raw.csv](/Professional_Python/Regexp/phonebook_raw.csv), используя регулярные выражения.
Структура данных будет всегда такая:
lastname,firstname,surname,organization,position,phone,email

Предполагается, что:

-телефон и e-mail у одного человека может быть только один;

-если совпали одновременно Фамилия и Имя, это точно один и тот же человек (даже если не указано его отчество).

1) Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно. В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О.

2) Привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999.

3) Объединить все дублирующиеся записи о человеке в одну.

```python
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

# ваш код

with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)
```
