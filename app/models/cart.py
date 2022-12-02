from flask import current_app as app


class Cart:
    def __init__(self, uid, pid, quantity, u_price, name, sid, fulfillment_status):
        self.uid = uid
        self.pid = pid
        self.quantity = quantity
        self.u_price = u_price
        self.name = name
        self.sid = sid
        self.fulfillment_status = fulfillment_status

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT Carts.uid as uid, Carts.pid as pid, Carts.quantity as quantity, Products.price as price,
Products.name as name, Carts.sid as sid, Purchases.fulfillment_status as fulfillment_status
FROM Carts, Products, Purchases
WHERE Carts.uid = :uid and Products.id = Carts.pid and 
Purchases.pid = Carts.pid and Purchases.sid = Carts.sid
''',
                              uid=uid)
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
WHERE uid = :uid
RETURNING uid
''',
                              uid=uid)
       id = rows[0][0]
       return Cart.get(id) 
   
    def addProduct(uid, pid, price, sid):
        rows = app.db.execute('''
INSERT INTO Carts(uid, pid, quantity, u_price, sid)
VALUES(:uid, :pid, :quantity, :price, :sid)
''',
                            uid=uid,
                            pid=pid,
                            quantity = 1,
                            price=price,
                            sid = sid)
    def get_with_status(uid):
        rows = app.db.execute('''
SELECT Carts.uid as uid, Carts.pid as pid, Carts.quantity as quantity, Products.price as price,
Products.name as name, Carts.sid as sid, Purchases.fulfillment_status as fulfillment_status
FROM Carts, Products, Purchases
WHERE Carts.uid = :uid and Products.id = Carts.pid and 
Purchases.pid = Carts.pid and Purchases.sid = Carts.sid
''',
                              uid=uid)
        return [Cart(*row) for row in rows]