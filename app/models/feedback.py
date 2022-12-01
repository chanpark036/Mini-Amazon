from flask import current_app as app


class Feedback:
    def __init__(self, id, uid, pid, sid, submitted_timestamp, review, rating, upvotes, pname= " ", firstname = " ", lastname = "last", email= " "):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.submitted_timestamp = submitted_timestamp
        self.review = review
        self.rating = rating
        self.upvotes = upvotes
        self.pname = pname
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT id, uid, pid, sid, submitted_timestamp, review, rating, upvotes
FROM Feedback
'''
                              )
        return [Feedback(*row) for row in rows]

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, sid, submitted_timestamp, review, rating, upvotes
FROM Feedback
WHERE id = :id
''',
                              id=id)
        return rows

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, sid, submitted_timestamp, review, rating, upvotes
FROM Feedback
WHERE uid = :uid
AND submitted_timestamp >= :since
ORDER BY submitted_timestamp DESC
''',
                              uid=uid,
                              since=since)
        return [Feedback(*row) for row in rows]
    
    @staticmethod
    def get_recent_k(uid, k):
        rows = app.db.execute('''
SELECT id, uid, pid, sid, submitted_timestamp, review, rating, upvotes
FROM Feedback
WHERE uid = :uid
ORDER BY submitted_timestamp DESC
''',
                              uid=uid,
                              k=k)
        if (len(rows) > k):
            return [Feedback(*(rows[i])) for i in range(k)]
        else :
            return [Feedback(*row) for row in rows]
    
    @staticmethod
    def get_all_by_uid_pid_help(uid):
        rows = app.db.execute('''
SELECT F.id, F.uid, F.pid, F.sid, F.submitted_timestamp, F.review, F.rating, F.upvotes, P.name
FROM Feedback F, Products P
WHERE uid = :uid
AND F.pid = P.id
ORDER BY upvotes DESC
''',
                              uid=uid)
        return [Feedback(*row) for row in rows]

    @staticmethod
    def get_all_by_uid_sid_help(uid):
        rows = app.db.execute('''
SELECT F.id, F.uid, F.pid, F.sid, F.submitted_timestamp, F.review, F.rating, F.upvotes, U.email, U.firstname, U.lastname
FROM Feedback F, Users U
WHERE uid = :uid
AND F.sid = U.id
ORDER BY upvotes DESC
''',
                              uid=uid)
        return [Feedback(*row) for row in rows]

    
    @staticmethod
    def get_all_by_pid(pid):
        rows = app.db.execute('''
SELECT F.id, F.uid, F.pid, F.sid, F.submitted_timestamp, F.review, F.rating, F.upvotes, U.email, U.firstname, U.lastname
FROM Feedback F, Users U
WHERE pid = :pid
AND F.uid = U.id
ORDER BY upvotes DESC
''',
                              pid=pid)
        return [Feedback(*row) for row in rows]
    
    @staticmethod
    def get_all_by_sid(sid):
        rows = app.db.execute('''
SELECT F.id, F.uid, F.pid, F.sid, F.submitted_timestamp, F.review, F.rating, F.upvotes, U.email, U.firstname, U.lastname
FROM Feedback F, Users U
WHERE sid = :sid
AND F.uid = U.id
ORDER BY upvotes DESC
''',
                              sid=sid)
        return [Feedback(*row) for row in rows]

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
    
    @staticmethod
    def add_p_review(uid, pid, review, rating, upvotes):
        try:
            rows = app.db.execute('''
INSERT INTO Feedback(uid, pid, review, rating, upvotes)
VALUES(:uid, :pid, :review,:rating,:upvotes)
RETURNING id
''',
                            uid=uid,
                            pid=pid,
                            review=review,
                            rating=rating,
                            upvotes=upvotes)
            id = rows[0][0]
            return feedback.get(id)
        except Exception as e:
            print(str(e))
            return None
    
    @staticmethod
    def add_s_review(uid, sid, review, rating, upvotes):
        try:
            rows = app.db.execute('''
INSERT INTO Feedback(uid, sid, review, rating, upvotes)
VALUES(:uid, :sid, :review,:rating,:upvotes)
RETURNING id
''',
                            uid=uid,
                            sid=sid,
                            review=review,
                            rating=rating,
                            upvotes=upvotes)
            id = rows[0][0]
            return feedback.get(id)
        except Exception as e:
            print(str(e))
            return None
    
    @staticmethod
    def update_review(id, review):
        rows = app.db.execute('''
UPDATE Feedback
SET review = :review
WHERE id= :id
''',
                              review=review,
                              id=id)
    
    @staticmethod
    def update_rating(id, rating):
        rows = app.db.execute('''
UPDATE Feedback
SET rating = :rating
WHERE id= :id
''',
                              rating=rating,
                              id=id)
    
    @staticmethod
    def delete_review(id):
       rows = app.db.execute('''
DELETE FROM Feedback
WHERE id= :id
''',
                              id=id) 
    
    @staticmethod
    def update_votes(id, upvotes):
        rows = app.db.execute('''
UPDATE Feedback
SET upvotes = :upvotes
WHERE id= :id
''',
                              upvotes=upvotes,
                              id=id)



        