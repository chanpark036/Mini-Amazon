from flask import current_app as app


class Cart:
    def __init__(self, uid, pid, quantity, u_price, name, sid, saved):
        self.uid = uid
        self.pid = pid
        self.quantity = quantity
        self.u_price = u_price
        self.name = name
        self.sid = sid
        self.saved = saved

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
            SELECT DISTINCT Carts.uid as uid, Carts.pid as pid, Carts.quantity as quantity, Carts.u_price as u_price,
            Products.name as name, Carts.sid as sid, Carts.saved as saved
            FROM Carts, Products, Inventory
            WHERE Carts.uid = :uid and Products.id = Carts.pid and 
            Inventory.sid = Carts.sid and Carts.saved = :false
            ''',
                              uid=uid,
                              false = False)
        return [Cart(*row) for row in rows]
    
    
    def getSaved(uid):
        rows = app.db.execute('''
            SELECT DISTINCT Carts.uid as uid, Carts.pid as pid, Carts.quantity as quantity, Carts.u_price as u_price,
            Products.name as name, Carts.sid as sid, Carts.saved as saved
            FROM Carts, Products, Inventory
            WHERE Carts.uid = :uid and Products.id = Carts.pid and 
            Inventory.sid = Carts.sid and Carts.saved = :true
            ''',
                                uid=uid,
                                true = True)
        return [Cart(*row) for row in rows]
    
    
    
    @staticmethod
    def updateCount(uid, pid, newValue):
        rows = app.db.execute('''
UPDATE Carts
SET quantity = :newValue
WHERE pid = :pid and uid = :uid
RETURNING uid
''',
                              uid = uid,
                              pid = pid, 
                              newValue=newValue)
        id = rows[0][0]
        return Cart.get(id)
    
    
    @staticmethod
    def delete_product(uid, pid):
       rows = app.db.execute('''
DELETE FROM Carts
WHERE pid= :pid and uid = :uid
RETURNING uid
''',
                              uid=uid,
                              pid=pid)
       id = rows[0][0]
       return Cart.get(id) 
    def emptyCart(uid):
       rows = app.db.execute('''
DELETE FROM Carts
WHERE uid = :uid and saved = :false
RETURNING uid
''',
                              uid=uid,
                              false = False)
       id = rows[0][0]
       return Cart.get(id) 
   
    def addProduct(uid, pid, price, sid):
        rows = app.db.execute('''
INSERT INTO Carts(uid, pid, quantity, u_price, sid, saved)
VALUES(:uid, :pid, :quantity, :price, :sid, :saved)
''',
                            uid=uid,
                            pid=pid,
                            quantity = 1,
                            price=price,
                            sid = sid,
                            saved = False)
        
    def saveForLater(uid, pid, saved):
        rows = app.db.execute('''
UPDATE Carts
SET saved = :saved
WHERE pid = :pid and uid = :uid
RETURNING uid
''',
                              uid = uid,
                              pid = pid,
                              saved = True)
        id = rows[0][0]
        return Cart.getSaved(id)
    
    def moveItem(uid, pid, saved):
        rows = app.db.execute('''
UPDATE Carts
SET saved = :saved
WHERE pid = :pid and uid = :uid
RETURNING uid
''',
                              uid = uid,
                              pid = pid,
                              saved = False)
        id = rows[0][0]
        return Cart.getSaved(id)
    
    