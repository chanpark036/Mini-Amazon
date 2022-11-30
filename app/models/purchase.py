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

    # Given a user id, get all purchases of that user.
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
    
    # Get most recent purchase ID
    @staticmethod
    def get_most_recent_purchase_id():
        rows = app.db.execute('''
                                SELECT id, uid, pid, time_purchased, fulfillment_status
                                FROM Purchases
                                ORDER BY id DESC
                                ''')
        id = rows[0][0]
        return id
    
    # After submitting an order, insert purchased items into purchase history
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
        
    # Given a user ID, return total price, total quantity, fulfillment status, 
    # and time purchased of each order within their purchase history 
    @staticmethod
    def get_purchase_history(uid):
        rows = app.db.execute("""
                              SELECT SUM(Products.price) as total_price, 
                              COUNT(*) as total_quantity,
                              Purchases.fulfillment_status as fulfillment_status,
                              Purchases.time_purchased as time_purchased
                              FROM Purchases, Products
                              WHERE Purchases.uid = :uid and Purchases.pid = Products.id
                              GROUP BY time_purchased, fulfillment_status
                              ORDER BY time_purchased DESC
                              """,
                              uid = uid)
        return rows
    
    # Given a user's order, return the specific order information, such as
    # product names, total price of each product, quantity of each product, 
    # fulfillment status, and time purchased
    @staticmethod
    def get_detailed_order_page(uid, time_purchased):
        rows = app.db.execute("""
                              SELECT Products.name as name,
                              SUM(Products.price) as total_price, 
                              COUNT(name) as total_quantity,
                              Purchases.fulfillment_status as fulfillment_status,
                              Purchases.time_purchased as time_purchased
                              FROM Purchases, Products
                              WHERE Purchases.uid = :uid and Purchases.time_purchased = :time_purchased and Purchases.pid = Products.id 
                              GROUP BY name, time_purchased, fulfillment_status
                              """,
                              uid = uid,
                              time_purchased = time_purchased)
        return rows