from flask import current_app as app

class Inventory:
    def __init__(self, sid, pid, quantity, price):
        self.sid = sid 
        self.pid = pid
        self.price = price
        self.quantity = quantity

    @staticmethod
    def get(sid):
        rows = app.db.execute('''
SELECT *
FROM Inventory
WHERE sid = :sid
''',
                              sid=sid)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def add(sid, pid, quantity, u_price):
        app.db.execute('''
        INSERT INTO Inventory (sid, pid, quantity, u_price)
        VALUES (:sid, :pid, :quantity, :u_price)
        ''', sid = sid, pid = pid, quantity = quantity, u_price = u_price)

    @staticmethod
    def remove(sid, pid):
        app.db.execute('''
            DELETE FROM Inventory
            WHERE sid = :sid AND pid = :pid
            ''', sid=sid, pid=pid)
    
    @staticmethod
    def change_q(sid, pid, quantity):
        app.db.execute('''
            UPDATE Inventory
            SET quantity = :quantity
            WHERE sid = :sid AND pid = :pid
        ''', quantity = quantity, sid = sid, pid=pid)
        
    
    @staticmethod
    def decreaseInventory(pid, change):
        app.db.execute('''
            UPDATE Inventory
            SET quantity = quantity-:change
            WHERE pid = :pid
        ''', change = change, pid=pid)

