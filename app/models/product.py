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

    '''
    @ get(id) gets the attributes related to row with id = id.
    @param: id = product ID
    @return: all fields in the Products table that match the product ID
    '''

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, category, description, price, available, image
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    '''
    @ get_all(True) gets all entries in Products table 
    @return: all fields of all entries in the Products table
    '''
    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, category, description, price, available, image
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]


    '''
    @ get_top_K_expensive(True, k) gets top k most expensive elements
    @param: k = value for top K
    @return: top k elements with respect to price in the Products table
    '''
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
        

    '''
    @ filterByName(name) returns rows that have name = name
    @param: name = name
    @return: returns rows that have name = name in the Products table
    '''
    @staticmethod
    # def filterByCategory(name):
    def filterByName(name):
        rows = app.db.execute('''
SELECT id, name, description, price, available
FROM Products
WHERE name = :name
''',
                            name = name)
        return [Product(*row) for row in rows]

    '''
    @ update_product_name(id, name) sets name to name of row with id = id in Products table
    @param: id = id, name = new name
    '''
    @staticmethod
    def update_product_name(id, name):
        rows = app.db.execute("""
UPDATE Products
SET name = :name
WHERE id= :id
""",
                              id=id,
                              name=name)

    '''
    @ update_product_description(id, description) sets description to description of row with id = id in Products table
    @param: id = id, description = new description
    '''
    @staticmethod
    def update_product_description(id, description):
        rows = app.db.execute("""
UPDATE Products
SET description = :description
WHERE id= :id
""",
                              id=id,
                              description=description)

    '''
    @ update_product_category(id, category) sets category to category of row with id = id in Products table
    @param: id = id, category = new category
    '''
    @staticmethod
    def update_product_category(id, category):
        rows = app.db.execute("""
UPDATE Products
SET category = :category
WHERE id= :id
""",
                              id=id,
                              category=category)

    '''
    @ update_product_image(id, imageurl) sets image to imageurl of row with id = id in Products table
    @param: id = id, imageurl = new image url
    '''
    @staticmethod
    def update_product_image(id, imageurl):
        rows = app.db.execute("""
UPDATE Products
SET image = :imageurl
WHERE id= :id
""",
                              id=id,
                              imageurl=imageurl)



    '''
    @ get_valid_products(available=True) gets all products that have at least one seller with quantity > 0 for that product
    @return: all fields of all entries in the Products table have at least one seller with quantity > 0 for that product. 
        For price, the min price among all sellers is returned 
    '''
    @staticmethod
    def get_valid_products(available=True):
        rows = app.db.execute('''
SELECT P.id, P.name, P.category, P.description, MIN(I.u_price), P.available, P.image
FROM Products P
LEFT JOIN Inventory I ON P.id = I.pid 
WHERE available = :available AND I.quantity > 0
GROUP BY P.id
''',
                              available=available)
        return [Product(*row) for row in rows]

    '''
    @ get_valid_products_under50(available=True) gets all products that have at least one seller with quantity > 0 for that product and have price < 50
    @return: all fields of all entries in the Products table have at least one seller with quantity > 0 for that product and have price < 50.
        For price, the min price among all sellers is returned 
    '''
    @staticmethod
    def get_valid_products_under50(available=True):
        rows = app.db.execute('''
SELECT P.id, P.name, P.category, P.description, MIN(I.u_price), P.available, P.image
FROM Products P
LEFT JOIN Inventory I ON P.id = I.pid 
WHERE available = :available AND I.quantity > 0 AND I.u_price < 50
GROUP BY P.id
''',
                              available=available)
        return [Product(*row) for row in rows]

    '''
    @ get_valid_products_from50to100(available=True) gets all products that have at least one seller with quantity > 0 for that product and have price >= 50 and <= 100
    @return: all fields of all entries in the Products table have at least one seller with quantity > 0 for that product and have price >= 50 and <= 100.
        For price, the min price among all sellers is returned 
    '''
    @staticmethod
    def get_valid_products_from50to100(available=True):
        rows = app.db.execute('''
SELECT P.id, P.name, P.category, P.description, MIN(I.u_price), P.available, P.image
FROM Products P
LEFT JOIN Inventory I ON P.id = I.pid 
WHERE available = :available AND I.quantity > 0 AND I.u_price >= 50 AND I.u_price <= 100
GROUP BY P.id
''',
                              available=available)
        return [Product(*row) for row in rows]

    '''
    @ get_valid_products_over100(available=True) gets all products that have at least one seller with quantity > 0 for that product and have price > 100
    @return: all fields of all entries in the Products table have at least one seller with quantity > 0 for that product and have price > 100.
        For price, the min price among all sellers is returned 
    '''
    @staticmethod
    def get_valid_products_over100(available=True):
        rows = app.db.execute('''
SELECT P.id, P.name, P.category, P.description, MIN(I.u_price), P.available, P.image
FROM Products P
LEFT JOIN Inventory I ON P.id = I.pid 
WHERE available = :available AND I.quantity > 0 AND I.u_price > 100
GROUP BY P.id
''',
                              available=available)
        return [Product(*row) for row in rows]