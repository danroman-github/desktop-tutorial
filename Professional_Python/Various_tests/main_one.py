"""Программа 'Секретарь'."""

# Исходные данные
documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
    {"type": "driver license", "number": "5455 028765", "name": "Василий Иванов"},
]

directories = {
    "1": ["2207 876234", "11-2", "5455 028765"],
    "2": ["10006"],
    "3": []
}

def get_name(doc_number):
    """Возвращает имя владельца документа по номеру документа."""
    for doc in documents:
        if doc["number"] == doc_number:
            return doc["name"]
    return "Документ не найден"

def get_directory(doc_number):
    """Возвращает номер полки, документа."""
    for shelf, docs in directories.items():
        if doc_number in docs:
            return shelf
    return "Полки с таким документом не найдено"

def add_new_document(document_type, number, name, shelf_number):
    """Добавляет новый документ в каталог и на указанную полку."""
    # Добавляем документ в список documents
    documents.append({
        "type": document_type,
        "number": number,
        "name": name
    })

    # Преобразуем номер полки в строку, если это необходимо
    shelf_number = str(shelf_number)

    # Добавляем документ на полку (создаем полку, если ее нет)
    if shelf_number in directories:
        directories[shelf_number].append(number)
    else:
        directories[shelf_number] = [number]
