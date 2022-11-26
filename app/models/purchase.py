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
    @staticmethod
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
                              ORDER BY time_purchased DESC
                              """,
                              uid = uid)
        return [Purchase(*row) for row in rows]
    
    #!melannie testing!
    @staticmethod
    def get_most_recent_purchase_id():
        rows = app.db.execute('''
                                SELECT id, uid, pid, time_purchased, fulfillment_status
                                FROM Purchases
                                ORDER BY id DESC
                                ''')
        id = rows[0][0]
        return id
    
    @staticmethod
    def add_purchase_history(id, uid, pid, time_purchased):
        rows = app.db.execute('''
                                INSERT INTO Purchases (id, uid, pid, time_purchased, fulfillment_status)
                                VALUES(:id, :uid, :pid, :time_purchased, :fulfillment_status)
                                ''',
                            id = id,
                            uid=uid,
                            pid=pid,
                            time_purchased =time_purchased,
                            fulfillment_status = False)
        
    
    # @staticmethod
    # def get_purchase_history_info(uid):
    #     rows = app.db.execute("""
    #                           SELECT SUM(Carts.u_price), Carts.quantity, purchases.fulfillment_status
    #                           FROM Purchases, Carts
    #                           WHERE Carts.uid = :Carts.uid and Purchases.pid = Products.id
    #                           ORDER BY Purchases.time_purchased DESC
    #                           """,
    #                           uid = uid)
    #     return [Purchase(*row) for row in rows]
    
    # @staticmethod
    # def get_purchase_total_cost(uid):
    #     rows = app.db.execute("""
    #                           SELECT SUM(Carts.u_price)
    #                           FROM Purchases, Carts
    #                           WHERE Carts.uid = :Carts.uid and Purchases.pid = Carts.id
    #                           GROUP BY Purchases.time_purchased
    #                           ORDER BY Purchases.time_purchased DESC
    #                           """,
    #                           uid = uid)
    #     return [Purchase(*row) for row in rows]