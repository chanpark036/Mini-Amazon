from flask import current_app as app


class Cart:
    def __init__(self, uid, pid, quantity, u_price):
        self.uid = uid
        self.pid = pid
        self.quantity = quantity
        self.u_price = u_price

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT *
FROM Carts
WHERE uid = :uid
''',
                              uid=uid)
        return [Cart(*row) for row in rows]