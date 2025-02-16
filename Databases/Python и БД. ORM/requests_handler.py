from models import Publisher, Book, Stock, Sale, Shop


def get_purchase_facts_by_publisher(session, entered_data):
    """Выводит построчно факты покупки книг указанного издателя."""

    if isinstance(entered_data, int):
        publisher = session.query(Publisher).filter(Publisher.id == entered_data).first()
    else:
        publisher = session.query(Publisher).filter(Publisher.name == entered_data).first()

    if not publisher:
        print("Издатель не найден.")
        return

    books = session.query(Book).filter(Book.id_publisher == publisher.id).all()

    purchase_facts = []

    for book in books:
        stocks = session.query(Stock).filter(Stock.id_book == book.id).all()
        for stock in stocks:
            sales = session.query(Sale).filter(Sale.id_stock == stock.id).all()
            for sale in sales:
                shop = session.query(Shop).filter(Shop.id == stock.id_shop).first()
                purchase_facts.append((book.title, shop.name, sale.price, sale.date_sale))

    purchase_facts.sort(key=lambda x: x[3], reverse=True)

    for fact in purchase_facts:
        print(f"{fact[0]} | {fact[1]} | {fact[2]} | {fact[3]}")