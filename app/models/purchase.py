from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, pid, name, time_purchased, fulfillment_status):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.name = name
        self.time_purchased = time_purchased
        self.fulfillment_status = fulfillment_status

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

# API: Given a user id, find all purchases of that user.
    def get_all_user_purchases(uid):
        rows = app.db.execute("""
                              SELECT Purchases.id as id, 
                              Purchases.uid as uid, 
                              Products.id as pid,
                              Products.name as name,
                              Purchases.time_purchased as time_purchased,
                              purchases.fulfillment_status as fulfillment_status
                              FROM Purchases, Products
                              WHERE uid = :uid and Purchases.pid = Products.id
                              """,
                              uid = uid)
        return [Purchase(*row) for row in rows]