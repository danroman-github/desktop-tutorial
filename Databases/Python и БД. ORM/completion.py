import json
from models import Publisher, Shop, Book, Stock, Sale

def load_data_from_json(session, json_file_path):
    """Загружает данные из JSON файла в базу данных."""

    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:

        model = item.get('model')
        pk_id = item.get('pk')
        fields = item.get('fields')

        if model == 'publisher':
            publisher = Publisher(
                id=pk_id,
                name=fields['name']
            )
            session.add(publisher)

        elif model == 'book':
            book = Book(
                id=pk_id,
                title=fields['title'],
                id_publisher=fields['id_publisher']
            )
            session.add(book)

        elif model == 'shop':
            shop = Shop(
                id=pk_id,
                name=fields['name']
            )
            session.add(shop)

        elif model == 'stock':
            stock = Stock(
                id=pk_id,
                id_book=fields['id_book'],
                id_shop=fields['id_shop'],
                count=fields['count']
            )
            session.add(stock)

        elif model == 'sale':
            sale = Sale(
                id=pk_id,
                price=fields['price'],
                date_sale=fields['date_sale'],
                id_stock=fields['id_stock'],
                count=fields['count']
            )
            session.add(sale)

    session.commit()
    print(f"Успешно загружено {len(data)} записей в базу данных.")
