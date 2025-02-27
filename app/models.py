class Book:
    def __init__(self, id, name, category_id, page_count, bounded_price):
        self.id = id
        self.name = name
        self.category_id = category_id
        self.page_count = page_count
        self.bounded_price = bounded_price


class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name
