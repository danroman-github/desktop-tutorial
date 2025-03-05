import csv
import re
from pprint import pprint
from collections import defaultdict

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def split_full_name(contact):
    """Нормализует фамилию, имя и отчество на основе входных данных."""
    full_name = ' '.join(contact[:3]).split()
    return (full_name[0] if len(full_name) > 0 else '',
            full_name[1] if len(full_name) > 1 else '',
            full_name[2] if len(full_name) > 2 else '')

def normalize_phone(phone):
    """Нормализует номер телефона в формат +7(XXX)XXX-XX-XX доб.XXX."""
    phone = re.sub(r'\D', '', phone)  # Убираем все нечисловые символы
    if phone.startswith('8'):
        phone = phone.replace('8', '7', 1)  # Заменяем '8' на '7'

    add_on = None

    if len(phone) == 11:  # Если номер состоит из 11 цифр
        return f'+7({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:]}'
    elif len(phone) > 11:
        add_on = re.search(r'(\d+)', phone[11:])  # Ищем добавочный номер

        if add_on:
            ext_number = add_on.group(0)
            return f'+7({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:11]} доб.{ext_number}'

    return phone


def normalize_contacts(contacts):
    """Функция нормализации данных адресной книги."""
    unique_contacts = defaultdict(lambda: [None, None, None, None, None, None, None])

    for contact in contacts:
        # if len(contact) >= 6:
        lastname, firstname, surname = split_full_name(contact)

        organization = contact[3].strip() if len(contact) > 3 else ''
        position = contact[4].strip() if len(contact) > 4 else ''
        phone = contact[5].strip() if len(contact) > 5 else ''
        email = contact[6].strip() if len(contact) > 6 else ''

        # Нормализация телефона
        phone = normalize_phone(phone)

        # Ключ для объединения: фамилия + имя
        key = (lastname, firstname)

        # Обновляем данные в уникальном словаре
        if unique_contacts[key][0] is None:
            unique_contacts[key] = [lastname, firstname, surname, organization, position, phone, email]
        else:
            # Обновляем данные, если они есть и непустые
            unique_contacts[key][2] = surname or unique_contacts[key][2]
            unique_contacts[key][3] = organization or unique_contacts[key][3]
            unique_contacts[key][4] = position or unique_contacts[key][4]
            unique_contacts[key][5] = phone or unique_contacts[key][5]
            unique_contacts[key][6] = email or unique_contacts[key][6]

    normalized_contacts = list(unique_contacts.values())
    return normalized_contacts


normalized_contacts = normalize_contacts(contacts_list)
pprint(normalized_contacts)

with open("phonebook.csv", "w", newline='', encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(normalized_contacts)
