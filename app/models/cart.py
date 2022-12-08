from flask import current_app as app


class Cart:
    '''
    Cart class represents a cart object. A new cart object is made for every product in a cart.
    Cart objects store the following information: user ID, product ID, quantity of product, unit price,
    product name, and whether or not a product is saved for later.
    '''
    def __init__(self, uid, pid, quantity, u_price, name, sid, saved):
        self.uid = uid
        self.pid = pid
        self.quantity = quantity
        self.u_price = u_price
        self.name = name
        self.sid = sid
        self.saved = saved

    '''
    *** get(uid) takes a user ID and returns all fields of all active cart objects associated with the user.
    @param: uid = unique user ID
    @return: UID, PID, Quantity, unit price, product name, seller ID, and 
    saved status for every item in an active cart
    '''
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
    
    '''
    *** getSaved(uid) takes a user ID and returns all fields of all saved cart objects associated with the user.
    @param: uid = unique user ID
    @return: UID, PID, Quantity, unit price, product name, seller ID, and 
    saved status for every saved item
    '''
    @staticmethod
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
    
    
    '''
    *** updateCount(uid, pid, newValue) takes a user ID, product ID, and new value to update the quantity of a
    product in the cart.
    @param: uid = unique user ID, pid = product ID, newValue = the new quantity to be purchased
    @return: UID, PID, Quantity, unit price, product name, seller ID, and 
    saved status for every item in a cart after the change is made to the database
    '''
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
    
    '''
    *** delete_product(uid, pid) takes a user ID and product ID to remove that product from a user's cart.
    @param: uid = unique user ID, pid = product ID
    @return: UID, PID, Quantity, unit price, product name, seller ID, and 
    saved status for every item in a cart after the change is made to the database
    '''
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
   
    '''
    *** emptyCart(uid) takes a user ID and deletes all entries in an active cart for that user.
    @param: uid = unique user ID
    @return: UID, PID, Quantity, unit price, product name, seller ID, and 
    saved status for every item in a cart after the change is made to the database (rows are empty for 
    all unsaved cart objects).
    '''
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
   
   '''
    *** addProduct(uid, pid, price, sid) adds product with pid, price, and corresponding seller ID to an active cart.
    @param: uid = unique user ID, pid = product id, price = product price, sid = seller ID of product added
    @return: none
    '''
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
        
    '''
    *** saveForLater(uid, pid, saved) takes a product for a given user's cart and changes saved status to True
    @param: uid = unique user ID, pid = product ID, saved = saved status
    @return: UID, PID, Quantity, unit price, product name, seller ID, and 
    saved status for every item in a "saved for later" cart after the change is made to the database.
    '''
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
    
    
    '''
    *** moveItem(uid, pid, saved) changes saved status to false for a given product in a given user's cart.
    In effect, unsaves a product to move it to an active cart.
    @param: uid = unique user ID, pid = product ID, saved = saved status
    @return: UID, PID, Quantity, unit price, product name, seller ID, and 
    saved status for every item in a "saved for later" cart after the change is made to the database.
    '''
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
    
    