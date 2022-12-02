from flask import current_app as app

class Inventory:
    def __init__(self, sid, pid, quantity, price, firstname = " ", lastname = " "):
        self.sid = sid 
        self.pid = pid
        self.price = price
        self.quantity = quantity
        self.firstname = firstname
        self.lastname = lastname

    @staticmethod
    def get(sid):
        rows = app.db.execute('''
            SELECT *
            FROM Inventory
            WHERE sid = :sid
            ORDER BY pid
            ''',
                              sid=sid)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def add(sid, pid, quantity, u_price):
        app.db.execute('''
        DO
        $do$
        BEGIN
            IF NOT EXISTS (SELECT FROM Inventory WHERE pid = :pid and sid = :sid) THEN
            INSERT INTO Inventory (sid, pid, quantity, u_price)
            VALUES (:sid, :pid, :quantity, :u_price);
            END IF;
        END
        $do$
        ''', sid = sid, pid = pid, quantity = quantity, u_price = u_price)
        return Inventory.get(sid)

    @staticmethod
    def remove(sid, pid):
        app.db.execute('''
            DELETE FROM Inventory
            WHERE sid = :sid AND pid = :pid
            ''', sid=sid, pid=pid)
        return Inventory.get(sid)
    
    @staticmethod
    def change_q(sid, pid, quantity):
        app.db.execute('''
            UPDATE Inventory
            SET quantity = :quantity
            WHERE sid = :sid AND pid = :pid
        ''', quantity = quantity, sid = sid, pid=pid)
        return Inventory.get(sid)

    #change later to include seller_id
    @staticmethod
    def decreaseInventory(pid, change, sid):
        app.db.execute('''
            UPDATE Inventory
            SET quantity = quantity-:change
            WHERE pid = :pid AND sid = :sid
        ''', change = change, pid=pid, sid = sid)

    @staticmethod
    def get_from_pid(pid):
        rows = app.db.execute('''
            SELECT I.sid, I.pid, I.quantity, I.u_price, U.firstname, U.lastname
            FROM Inventory I, Users U
            WHERE I.pid = :pid AND I.sid = U.id
            ORDER BY I.sid
            ''',
                              pid=pid)
        return [Inventory(*row) for row in rows]
    def get_from_pid_specific(pid, sid):
        rows = app.db.execute('''
            SELECT I.sid, I.pid, I.quantity, I.u_price, U.firstname, U.lastname
            FROM Inventory I, Users U
            WHERE I.pid = :pid AND I.sid = :sid
            ORDER BY I.sid
            ''',
                              pid=pid,
                              sid = sid)
        return rows[0]

    # @staticmethod
    # def get_name_from_pid(pid):
    #     rows = app.db.execute('''
    #         SELECT *
    #         FROM Inventory
    #         WHERE pid = :pid
    #         ORDER BY sid
    #         ''',
    #                           pid=pid)
    #     return [Inventory(*row) for row in rows]