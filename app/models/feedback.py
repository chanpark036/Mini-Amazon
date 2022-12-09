from flask import current_app as app


class Feedback:
    def __init__(self, id, uid, pid, sid, submitted_timestamp, review, rating, upvotes, image, pname= " ", firstname = " ", lastname = "last", email= " "):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.submitted_timestamp = submitted_timestamp
        self.review = review
        self.rating = rating
        self.upvotes = upvotes
        self.image = image
        self.pname = pname
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
    
    '''
    *** get_all() returns all entries from the Feedback table.
    @param: none
    @return: id, uid, pid, sid, submitted_timestamp, review, rating, upvotes, image 
    for every entry in Feedback table.
    '''
    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT id, uid, pid, sid, submitted_timestamp, review, rating, upvotes, image
FROM Feedback
'''
                              )
        return [Feedback(*row) for row in rows]

    '''
    *** get(id) takes in a review id and returns the entry matching it.
    @param: id = unique review id
    @return: id, uid, pid, sid, submitted_timestamp, review, rating, upvotes, image 
    for matching id.
    '''
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, sid, submitted_timestamp, review, rating, upvotes, image
FROM Feedback
WHERE id = :id
''',
                              id=id)
        return rows

    '''
    *** get_all_by_uid_since(uid, since) takes a uid and time and returns all matching entries from the Feedback table.
    @param: uid, since = unique user id, date and time
    @return: id, uid, pid, sid, submitted_timestamp, review, rating, upvotes, image 
    for every entry by that uid since the time in Feedback table.
    '''
    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, sid, submitted_timestamp, review, rating, upvotes, image
FROM Feedback
WHERE uid = :uid
AND submitted_timestamp >= :since
ORDER BY submitted_timestamp DESC
''',
                              uid=uid,
                              since=since)
        return [Feedback(*row) for row in rows]
    

    '''
    *** get_all_by_uid_pid_recent(uid) takes a uid and returns the product reviews for a certain user ordered by timestamp from the Feedback and Product tables.
    @param: uid = unique user id
    @return: id, uid, pid, sid, submitted_timestamp, review, rating, upvotes, image, name 
    for every entry by that uid and containing a pid in Feedback, Product tables.
    '''
    @staticmethod
    def get_all_by_uid_pid_recent(uid):
        rows = app.db.execute('''
SELECT F.id, F.uid, F.pid, F.sid, F.submitted_timestamp, F.review, F.rating, F.upvotes, F.image, P.name
FROM Feedback F, Products P
WHERE uid = :uid
AND F.pid = P.id
ORDER BY submitted_timestamp DESC
''',
                              uid=uid)
        return [Feedback(*row) for row in rows]

    '''
    *** get_all_by_uid_sid_recent(uid) takes a uid and returns the seller reviews for a certain user ordered by timestamp from the Feedback and User tables.
    @param: uid = unique user id
    @return: id, uid, pid, sid, submitted_timestamp, review, rating, upvotes, image, email, firstname, lastname
    for every entry by that uid and containing a sid in Feedback, User tables.
    '''
    @staticmethod
    def get_all_by_uid_sid_recent(uid):
        rows = app.db.execute('''
SELECT F.id, F.uid, F.pid, F.sid, F.submitted_timestamp, F.review, F.rating, F.upvotes, F.image, U.email, U.firstname, U.lastname
FROM Feedback F, Users U
WHERE uid = :uid
AND F.sid = U.id
ORDER BY submitted_timestamp DESC
''',
                              uid=uid)
        return [Feedback(*row) for row in rows]

    
    '''
    *** get_all_by_pid(pid) takes a pid and returns the reviews on this pid from the Feedback and Users tables.
    @param: pid = unique product id
    @return: id, uid, pid, sid, submitted_timestamp, review, rating, upvotes, image, email, firstname, lastname 
    for every entry matching that pid in Feedback, User tables ordered by upvotes.
    '''
    @staticmethod
    def get_all_by_pid(pid):
        rows = app.db.execute('''
SELECT F.id, F.uid, F.pid, F.sid, F.submitted_timestamp, F.review, F.rating, F.upvotes, F.image, U.email, U.firstname, U.lastname
FROM Feedback F, Users U
WHERE pid = :pid
AND F.uid = U.id
ORDER BY upvotes DESC
''',
                              pid=pid)
        return [Feedback(*row) for row in rows]
    
    '''
    *** get_all_by_sid(sid) takes a sid and returns the reviews on this sid from the Feedback and Users tables.
    @param: sid = unique user id
    @return: id, uid, pid, sid, submitted_timestamp, review, rating, upvotes, image, email, firstname, lastname 
    for every entry matching that sid in Feedback, User tables ordered by upvotes.
    '''
    @staticmethod
    def get_all_by_sid(sid):
        rows = app.db.execute('''
SELECT F.id, F.uid, F.pid, F.sid, F.submitted_timestamp, F.review, F.rating, F.upvotes, F.image, U.email, U.firstname, U.lastname
FROM Feedback F, Users U
WHERE sid = :sid
AND F.uid = U.id
ORDER BY upvotes DESC
''',
                              sid=sid)
        return [Feedback(*row) for row in rows]

    '''
    *** get_p_stats(pid) takes a pid and returns the average rating and number of entries.
    @param: pid = unique product id
    @return: pid, AVG(rating), COUNT(*)
    for the matching pid.
    '''
    @staticmethod
    def get_p_stats(pid):
        rows = app.db.execute('''
SELECT pid, AVG(rating), COUNT(*)
FROM Feedback
WHERE pid = :pid
GROUP BY pid
''',
                              pid=pid)
        return rows

    '''
    *** get_s_stats(sid) takes a sid and returns the average rating and number of entries.
    @param: sid = unique user id
    @return: sid, AVG(rating), COUNT(*)
    for the matching sid.
    '''
    @staticmethod
    def get_s_stats(sid):
        rows = app.db.execute('''
SELECT sid, AVG(rating), COUNT(*)
FROM Feedback
WHERE sid = :sid
GROUP BY sid
''',
                              sid=sid)
        return rows

    '''
    *** get_p_ratings(pid) takes a pid and returns the number of entries in each rating category (1-5).
    @param: pid = unique product id
    @return: rating, COUNT(*)
    for the matching pid.
    '''
    @staticmethod
    def get_p_ratings(pid):
        rows = app.db.execute('''
SELECT rating, COUNT(*)
FROM Feedback
WHERE pid = :pid
GROUP BY rating
''',
                              pid=pid)
        return rows

    '''
    *** get_s_ratings(sid) takes a sid and returns the number of entries in each rating category (1-5).
    @param: sid = unique user id
    @return: rating, COUNT(*)
    for the matching sid.
    '''
    @staticmethod
    def get_s_ratings(sid):
        rows = app.db.execute('''
SELECT rating, COUNT(*)
FROM Feedback
WHERE sid = :sid
GROUP BY rating
''',
                              sid=sid)
        return rows

    '''
    *** get_p_u_ratings(pid, uid) takes a pid and uid returns the review for entries matching both.
    @param: pid, uid = unique product id, unique user id
    @return: review for entries with that pid and uid.
    '''
    @staticmethod
    def get_p_u_ratings(pid, uid):
        rows = app.db.execute('''
SELECT review
FROM Feedback
WHERE pid = :pid
AND uid = :uid
''',
                              pid=pid,
                              uid=uid)
        return rows

    '''
    *** get_s_u_ratings(sid, uid) takes a sid (user id of the seller) and uid returns the review for entries matching both.
    @param: sid, uid = unique user id, unique user id
    @return: review for entries with that sid and uid.
    '''
    @staticmethod
    def get_s_u_ratings(sid, uid):
        rows = app.db.execute('''
SELECT review
FROM Feedback
WHERE sid = :sid
AND uid = :uid
''',
                              sid=sid,
                              uid=uid)
        return rows
    
    '''
    *** check_s_u(sid, uid) takes a sid (user id of the seller) and uid returns the id for entries matching both in the purchases table.
    @param: sid, uid = unique user id, unique user id
    @return: id for purchases with that sid and uid.
    '''
    @staticmethod
    def check_s_u(sid, uid):
        rows = app.db.execute('''
SELECT id
FROM Purchases
WHERE sid = :sid
AND uid = :uid
''',
                              sid=sid,
                              uid=uid)
        return rows
    
    '''
    *** add_p_review(uid, pid, review, rating, upvotes, image) takes in information for a product review and adds it to the table.
    @param: uid, pid, review, rating, upvotes, image = unique user id, unique product id, review text, rating (1-5), upvotes (0 to start), image url
    @return: unique id of review.
    '''
    @staticmethod
    def add_p_review(uid, pid, review, rating, upvotes, image):
        try:
            rows = app.db.execute('''
INSERT INTO Feedback(uid, pid, review, rating, upvotes, image)
VALUES(:uid, :pid, :review,:rating,:upvotes,:image)
RETURNING id
''',
                            uid=uid,
                            pid=pid,
                            review=review,
                            rating=rating,
                            upvotes=upvotes,
                            image=image)
            id = rows[0][0]
            return feedback.get(id)
        except Exception as e:
            print(str(e))
            return None
    
    '''
    *** add_s_review(uid, sid, review, rating, upvotes, image) takes in information for a seller review and adds it to the table.
    @param: uid, sid, review, rating, upvotes, image = unique user id, unique user id of seller, review text, rating (1-5), upvotes (0 to start), image url
    @return: unique id of review.
    '''
    @staticmethod
    def add_s_review(uid, sid, review, rating, upvotes, image):
        try:
            rows = app.db.execute('''
INSERT INTO Feedback(uid, sid, review, rating, upvotes, image)
VALUES(:uid, :sid, :review,:rating,:upvotes,:image)
RETURNING id
''',
                            uid=uid,
                            sid=sid,
                            review=review,
                            rating=rating,
                            upvotes=upvotes,
                            image=image)
            id = rows[0][0]
            return feedback.get(id)
        except Exception as e:
            print(str(e))
            return None
    
    '''
    *** update_review(id, review) takes in review id and review text and updates the entry.
    @param: id, review = unique review id, review text
    '''
    @staticmethod
    def update_review(id, review):
        rows = app.db.execute('''
UPDATE Feedback
SET review = :review
WHERE id= :id
''',
                              review=review,
                              id=id)
    
    '''
    *** update_rating(id, rating) takes in review id and rating and updates the entry.
    @param: id, rating = unique review id, rating (1-5)
    '''
    @staticmethod
    def update_rating(id, rating):
        rows = app.db.execute('''
UPDATE Feedback
SET rating = :rating
WHERE id= :id
''',
                              rating=rating,
                              id=id)

    '''
    *** update_image(id, image) takes in review id and image url and updates the entry.
    @param: id, image = unique review id, image url
    '''
    @staticmethod
    def update_image(id, image):
        rows = app.db.execute('''
UPDATE Feedback
SET image = :image
WHERE id= :id
''',
                              image=image,
                              id=id)
    
    '''
    *** delete_review(id) takes in review id and deletes the matching entry.
    @param: id = unique review id
    '''
    @staticmethod
    def delete_review(id):
       rows = app.db.execute('''
DELETE FROM Feedback
WHERE id= :id
''',
                              id=id) 
    
    '''
    *** update_votes(id, upvotes) takes in review id and upvotes and updates the entry.
    @param: id, upvotes = unique review id, number of upvotes
    '''
    @staticmethod
    def update_votes(id, upvotes):
        rows = app.db.execute('''
UPDATE Feedback
SET upvotes = :upvotes
WHERE id= :id
''',
                              upvotes=upvotes,
                              id=id)



        