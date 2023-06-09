from flask import current_app as app

class Inventory:
    def __init__(self, sid, pid, quantity, price, firstname = " ", lastname = " ", p_name = ""):
        self.sid = sid 
        self.pid = pid
        self.price = price
        self.quantity = quantity
        self.firstname = firstname
        self.lastname = lastname
        self.p_name = ""
        
    '''
    *** verify_seller(sid) checks if the given seller is registered to be a seller
    @param sid = seller_id
    @return val = True if sid is seller else False
    '''
    @staticmethod
    def verify_seller(sid):
        val = app.db.execute('''
        SELECT seller FROM Users WHERE id = :sid
        ''',sid=sid)[0][0]
        return val

    '''
    *** get(sid) gets sid,pid,price,and quantity data from database for a given seller and returns Inventory objects with this data
    @param sid = seller_id
    @return Inventory objects with sid,pid,price,and quantity information from database
    '''
    @staticmethod
    def get(sid):
        rows = app.db.execute('''
            SELECT *
            FROM Inventory
            WHERE sid = :sid
            ORDER BY pid
            ''',
                              sid=sid)
        return [Inventory(*row) for row in rows]

    '''
    *** add(sid, pid, quantity, u_price) adds a new product into the given user's inventory
    @param sid = seller_id, pid = product_id, quantity = product quantity, u_price = product price
    @return Inventory objects with sid, pid, quantity, price information
    '''
    @staticmethod
    def add(sid, pid, quantity, u_price):
        app.db.execute('''
        DO
        $do$
        BEGIN
            IF NOT EXISTS (SELECT FROM Inventory WHERE pid = :pid and sid = :sid) THEN
            INSERT INTO Inventory (sid, pid, quantity, u_price)
            VALUES (:sid, :pid, :quantity, :u_price);
            END IF;
        END
        $do$
        ''', sid = sid, pid = pid, quantity = quantity, u_price = u_price)
        return Inventory.get(sid)

    '''
    *** remove(sid,pid) removes a product from a user's inventory
    @param sid = seller_id, pid = product_id
    @return Inventory objects with sid, pid, quantity, price information
    '''
    @staticmethod
    def remove(sid, pid):
        app.db.execute('''
            DELETE FROM Inventory
            WHERE sid = :sid AND pid = :pid
            ''', sid=sid, pid=pid)
        return Inventory.get(sid)
    
    '''
    *** change_q(sid,pid,quantity) changes the quantity of a product in a user's inventory
    @param sid = seller_id, pid = product_id, quantity = new quantity to change quantity to
    @return Inventory objects with sid, pid, quantity, price information
    '''  
    @staticmethod
    def change_q(sid, pid, quantity):
        app.db.execute('''
            UPDATE Inventory
            SET quantity = :quantity
            WHERE sid = :sid AND pid = :pid
        ''', quantity = quantity, sid = sid, pid=pid)
        return Inventory.get(sid)

    '''
    *** decreaseInventory(pid, change, sid) reduces a product's quantity by a value "change" for a given seller's inventory
    @param: pid = product ID, change = the amount to change in quantity, sid = the seller ID whose inventory must be changed
    @return: none
    '''
    @staticmethod
    def decreaseInventory(pid, change, sid):
        app.db.execute('''
            UPDATE Inventory
            SET quantity = quantity-:change
            WHERE pid = :pid AND sid = :sid
        ''', change = change, pid=pid, sid = sid)

    '''
    *** get_from_pid(pid) gets all users who have products with id pid in their inventory
    @param: pid = product ID
    @return: Inventory objects with sid, pid, quantity, price information
    '''
    @staticmethod
    def get_from_pid(pid):
        rows = app.db.execute('''
            SELECT I.sid, I.pid, I.quantity, I.u_price, U.firstname, U.lastname
            FROM Inventory I, Users U
            WHERE I.pid = :pid AND I.sid = U.id
            ORDER BY I.u_price
            ''',
                              pid=pid)
        return [Inventory(*row) for row in rows]

    '''
    *** get_from_pid_specific(pid, sid) gets a certain product's information from a given seller
    @param: pid = product ID, sid = seller ID
    @return: all fields in the inventory database that match the seller ID and product ID
    '''
    def get_from_pid_specific(pid, sid):
        rows = app.db.execute('''
            SELECT I.sid, I.pid, I.quantity, I.u_price, U.firstname, U.lastname
            FROM Inventory I, Users U
            WHERE I.pid = :pid AND I.sid = :sid
            ORDER BY I.sid
            ''',
                              pid=pid,
                              sid = sid)
        return rows[0]

    '''
    ***get_name_from_pid(pid) gets the name of a product given the product's id
    @param: pid = product ID
    @return: the product's name
    '''
    @staticmethod
    def get_name_from_pid(pid):
        val = app.db.execute('''
            SELECT name
            FROM Products
            WHERE id = :pid
            ''',
                              pid=pid)
        return val[0][0]

    '''
    *** add_new_product(seller_id, name,description,price,quantity,image,category) adds a new product into the given user's inventory and also adds it to the products on sale
    @param seller_id = seller_id, name = product name, description = product description, price = product price, quantity = quantity of product, image = product image, category = product category
    '''
    @staticmethod
    def add_new_product(seller_id, name,description,price,quantity,image,category):
        available = True
        # product_in_db = app.db.execute('SELECT * FROM Products WHERE name=:name AND description=:description',name=name,description=description)
        product_in_db = app.db.execute('SELECT * FROM Products WHERE name=:name',name=name)
        if not product_in_db:
            max_pid = app.db.execute(' SELECT MAX(id) FROM Products')
            new_pid = int(max_pid[0][0])+1
            app.db.execute('''
            DO
            $do$
            BEGIN
                IF NOT EXISTS (SELECT FROM Products WHERE name = :name ) THEN
                INSERT INTO Products (id, name, category, description, price, available, image) 
                VALUES (:new_pid, :name, :category, :description, :price, :available, :image);
                END IF;
            END
            $do$
            ''', new_pid = new_pid, name=name, category = category, description=description, price = price, quantity = quantity, image = image, available = available)
        else:
            new_pid = product_in_db[0][0]
        Inventory.add(seller_id, new_pid, quantity, price)
        
    '''
    *** given sid find times that people bought from seller
    @param: sid = seller id
    @return times that people bought from seller
    '''  
    @staticmethod
    def times_bought_from_seller(sid):
        times = app.db.execute('SELECT time_purchased FROM Purchases where sid=:sid',sid=sid)
        return times
        
    '''
    *** given sid find names of people bought from seller
    @param: sid = seller id
    @return names of people that bought from seller
    '''  
    @staticmethod
    def users_buying_from_seller(sid):
        users = app.db.execute('SELECT U.firstname,U.lastname FROM Purchases P,Users U where P.sid=:sid AND U.id=P.uid',sid=sid)
        return users

    '''
    *** given sid find quantites and names of products that people bought from seller
    @param: sid = seller id
    @return quantities and names of people that bought from seller
    '''  
    @staticmethod
    def product_popularity(sid):
        name = app.db.execute('SELECT P.name,Pu.quantity FROM Purchases Pu, Products P WHERE Pu.pid=P.id AND Pu.sid = :sid',sid=sid)
        return name