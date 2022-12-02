from flask import current_app as app

class Product:
    def __init__(self, id, name, category, description, price, available, image):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.available = available
        self.description = description
        self.image = image

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, category, description, price, available, image
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, category, description, price, available, image
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

##
##

    @staticmethod
    def get_top_K_expensive(available=True, k = 0):
        rows = app.db.execute('''
SELECT id, name, description, price, available, 
FROM Products
ORDER BY price DESC
''',
                              available=available)
                              
        if k == 0:
            return []    
        else:
            return [Product(*row) for row in rows[:k]]
        
#     @staticmethod
#     def filterByCategory(category):
#         rows = app.db.execute('''
# SELECT id, name, description, price, available
# FROM Products
# WHERE category = :category
# ''',
#                               available=True)
#         return [Product(*row) for row in rows]


# TODO: CHANGE THE QUERY from name to category
    @staticmethod
    def filterByCategory(name):
        rows = app.db.execute('''
SELECT id, name, description, price, available
FROM Products
WHERE name = :name
''',
                            name = name)
        return [Product(*row) for row in rows]


