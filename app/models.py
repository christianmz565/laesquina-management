class Book():
    def __init__(self, id, name, category_id, price):
        self.id = id
        self.name = name
        self.category_id = category_id
        self.price = price

    def __str__(self):
        return f"{self.id} - {self.name} - {self.category_id} - S/.{self.price}"

class Category():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"{self.id} - {self.name}"