from flask import current_app as app


class Cart:
    def __init__(self, uid, pid, quantity, u_price, name, prodid):
        self.uid = uid
        self.pid = pid
        self.quantity = quantity
        self.u_price = u_price
        self.name = name
        self.prodid = prodid

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT Carts.uid as uid, Carts.pid as pid, Carts.quantity as quantity, Carts.u_price as price,
Products.name as name, Products.id as id
FROM Carts, Products
WHERE uid = :uid and Products.id = Carts.pid
''',
                              uid=uid)
        return [Cart(*row) for row in rows]