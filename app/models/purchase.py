from flask import current_app as app


class Purchase:
    '''
    Purchase class represents a purchase object. A new purchase object is made when a user purchases a product.
    Purchase objects store the following information: purchase ID, uid, sid, pid, quantity, time purchased, fulfillment status
    current balance, and address. 
    '''
    def __init__(self, id, uid, sid, pid, quantity=0, name="", time_purchased="", fulfillment_status=False):
        self.id = id
        self.uid = uid
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.name = name
        self.time_purchased = time_purchased
        self.fulfillment_status = fulfillment_status

    '''
    *** get(uid) takes a user ID and returns all fields associated with that user.
    @param: uid = unique user ID
    @return: id, uid, pid, time_purchased
    '''
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    '''
    *** get_all_by_uid_since(uid, since) takes a user ID and returns all purchases associated with that user since a certain time.
    @param: uid = unique user ID, since = since this time
    @return: id, uid, pid, time_purchased
    '''
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

    '''
    *** get_all_user_purchases(uid) takes a user ID and returns all purchases associated with that user since a certain time.
    @param: uid = unique user ID
    @return: id, uid, pid, time_purchased
    '''
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
    
    '''
    *** get_most_recent_purchase_id() returns most recently purchased item associated.
    @param: None
    @return: id
    '''
    @staticmethod
    def get_most_recent_purchase_id():
        rows = app.db.execute('''
                                SELECT id, uid, pid, time_purchased, fulfillment_status
                                FROM Purchases
                                ORDER BY id DESC
                                ''')
        id = rows[0][0]
        return id
    
    '''
    *** add_purchase_history(id, uid, sid, pid, quantity, time_purchased) updates a user's purchase history after they submit an order. 
    @param: id = purchase ID, uid = user ID, sid = seller ID, pid = product ID, quantity = quantity, time_purchased = time the order was placed,
    fulfillment_status = Not Fulfilled at first
    @return: None
    '''
    @staticmethod
    def add_purchase_history(id, uid, sid, pid, quantity, time_purchased):
        rows = app.db.execute('''
                                INSERT INTO Purchases (id, uid, sid, pid, quantity, time_purchased, fulfillment_status)
                                VALUES(:id, :uid, :sid, :pid, :quantity, :time_purchased, :fulfillment_status)
                                ''',
                            id = id,
                            uid=uid,
                            sid=sid,
                            pid=pid,
                            quantity = quantity,
                            time_purchased =time_purchased,
                            fulfillment_status = "Not Fulfilled")
        
    '''
    *** get_purchase_history(uid) returns details of each other within a user's purchase history  
    @param: uid = user ID
    @return: total_price, total_quantity, fulfillment_status, time_purchased
    '''
    @staticmethod
    def get_purchase_history(uid):
        rows = app.db.execute("""
                              SELECT SUM(Inventory.u_price*Purchases.quantity) as total_price, 
                              SUM(Purchases.quantity) as total_quantity,
                              Purchases.fulfillment_status as fulfillment_status,
                              Purchases.time_purchased as time_purchased
                              FROM Purchases, Products, Inventory
                              WHERE Purchases.uid = :uid and Purchases.pid = Products.id and 
                              Products.id = Inventory.pid and Inventory.sid = Purchases.sid
                              GROUP BY time_purchased, fulfillment_status
                              ORDER BY time_purchased DESC
                              """,
                              uid = uid)
        return rows
    
    '''
    *** get_detailed_order_page(uid, time_purchased) return the specific order information per item
    @param: uid = user ID, time_purchased = the time an order was purchased
    @return: name, total_price, total_quantity, fulfillment_status, time_purchased, sid, seller_firstname, seller_lastname
    '''
    @staticmethod
    def get_detailed_order_page(uid, time_purchased):
        rows = app.db.execute("""
                              SELECT Products.name as name,
                              SUM(Inventory.u_price) as total_price, 
                              SUM(Purchases.quantity) as total_quantity,
                              Purchases.fulfillment_status as fulfillment_status,
                              Purchases.time_purchased as time_purchased,
                              Purchases.sid as sid,
                              Users.firstname as seller_firstname,
                              Users.lastname as seller_lastname
                              FROM Purchases, Products, Users, Inventory
                              WHERE Purchases.uid = :uid and Purchases.time_purchased = :time_purchased and Purchases.pid = Products.id 
                              and Users.id = Purchases.sid and Products.id = Inventory.pid and Inventory.sid = Purchases.sid
                              GROUP BY name, time_purchased, fulfillment_status, Purchases.quantity, Purchases.sid, seller_firstname, seller_lastname
                              """,
                              uid = uid,
                              time_purchased = time_purchased)
        return rows

    '''
        get_address() gets the address of a user given their id
        @param: uid = user ID
        @return: address
    '''
    @staticmethod
    def get_address(uid):
        address = app.db.execute("""
                              SELECT address 
                              FROM Users
                              WHERE :uid = Users.id
                              """,
                              uid = uid)
        return address[0][0]


    '''
        get_all_seller_purchases(sid) gets all the purchases from a seller given the seller's id
        @param: sid = seller ID
        @return: Purchases with id,uid,sid,pid,quantity,full name,time_purchased,fulfillment_status
    '''
    @staticmethod
    def get_all_seller_purchases(sid):
        rows = app.db.execute("""
                              SELECT Purchases.id as id, 
                              Purchases.uid as uid,
                              Purchases.sid as sid,
                              Purchases.pid as pid,
                              Purchases.quantity as quantity,
                              Users.firstname as firstname,
                              Users.lastname as lastname,
                              Purchases.time_purchased as time_purchased,
                              Purchases.fulfillment_status as fulfillment_status
                              FROM Purchases, Users
                              WHERE sid = :sid AND Users.id = uid
                              ORDER BY time_purchased DESC
                              """,
                              sid = sid)
        return [Purchase(id,uid,sid,pid,quantity,firstname+" "+lastname,time_purchased,fulfillment_status, "") for id,uid,sid,pid,quantity,firstname,lastname, time_purchased,fulfillment_status in rows]


    '''
    *** change_fulfillment(sid, uid, pid, id, new_status) updates the fulfillment status for a product for a given seller and given buyer.
    @param: sid = seller ID, uid = unique user ID, pid = product ID, id = purchase ID, new_status = new fulfillment status
    @return: all fields of a purchase object for the seller
    '''
    @staticmethod
    def change_fulfillment(sid, uid, pid, id, new_status):
        app.db.execute('''
            UPDATE Purchases
            SET fulfillment_status = :new_status
            WHERE sid = :sid AND pid = :pid AND uid=:uid AND id = :id
        ''', new_status = new_status, sid = sid, pid=pid, uid=uid, id=id)
        return Purchase.get_all_seller_purchases(sid)