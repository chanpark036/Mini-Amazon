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
    
    @staticmethod
    def verify_seller(sid):
        val = app.db.execute('''
        SELECT seller FROM Users WHERE id = :sid
        ''',sid=sid)[0][0]
        return val

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

    @staticmethod
    def remove(sid, pid):
        app.db.execute('''
            DELETE FROM Inventory
            WHERE sid = :sid AND pid = :pid
            ''', sid=sid, pid=pid)
        return Inventory.get(sid)
    
    @staticmethod
    def change_q(sid, pid, quantity):
        app.db.execute('''
            UPDATE Inventory
            SET quantity = :quantity
            WHERE sid = :sid AND pid = :pid
        ''', quantity = quantity, sid = sid, pid=pid)
        return Inventory.get(sid)

    '''
    @TODO
    '''
    @staticmethod
    def decreaseInventory(pid, change, sid):
        app.db.execute('''
            UPDATE Inventory
            SET quantity = quantity-:change
            WHERE pid = :pid AND sid = :sid
        ''', change = change, pid=pid, sid = sid)

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
    @TODO
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

    @staticmethod
    def get_name_from_pid(pid):
        val = app.db.execute('''
            SELECT name
            FROM Products
            WHERE id = :pid
            ''',
                              pid=pid)
        return val[0][0]


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
        
        
    @staticmethod
    def times_bought_from_seller(sid):
        times = app.db.execute('SELECT time_purchased FROM Purchases where sid=:sid',sid=sid)
        return times

    @staticmethod
    def users_buying_from_seller(sid):
        users = app.db.execute('SELECT U.firstname,U.lastname FROM Purchases P,Users U where P.sid=:sid AND U.id=P.uid',sid=sid)
        return users

    @staticmethod
    def product_popularity(sid):
        name = app.db.execute('SELECT P.name,Pu.quantity FROM Purchases Pu, Products P WHERE Pu.pid=P.id AND Pu.sid = :sid',sid=sid)
        return name