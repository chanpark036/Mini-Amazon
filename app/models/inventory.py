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
