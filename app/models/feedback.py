from flask import current_app as app


class Feedback:
    def __init__(self, id, uid, pid, sid, submitted_timestamp, review, rating):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.submitted_timestamp = submitted_timestamp
        self.review = review
        self.rating = rating

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT id, uid, pid, sid, submitted_timestamp, review, rating
FROM Feedback
'''
                              )
        return [Feedback(*row) for row in rows]

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, sid, submitted_timestamp, review, rating
FROM Feedback
WHERE id = :id
''',
                              id=id)
        return Feedback(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, sid, submitted_timestamp, review, rating
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
SELECT id, uid, pid, sid, submitted_timestamp, review, rating
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
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT id, uid, pid, sid, submitted_timestamp, review, rating
FROM Feedback
WHERE uid = :uid
ORDER BY submitted_timestamp DESC
''',
                              uid=uid)
        return [Feedback(*row) for row in rows]
    
    @staticmethod
    def get_all_by_pid(pid):
        rows = app.db.execute('''
SELECT id, uid, pid, sid, submitted_timestamp, review, rating
FROM Feedback
WHERE pid = :pid
ORDER BY rating DESC
''',
                              pid=pid)
        return [Feedback(*row) for row in rows]
    
    @staticmethod
    def get_all_by_sid(sid):
        rows = app.db.execute('''
SELECT id, uid, pid, sid, submitted_timestamp, review, rating
FROM Feedback
WHERE sid = :sid
ORDER BY rating DESC
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
    def add_p_review(uid, pid, review, rating):
        try:
            rows = app.db.execute('''
INSERT INTO Feedback(uid, pid, review, rating)
VALUES(:uid, :pid, :review,:rating)
RETURNING id
''',
                            uid=uid,
                            pid=pid,
                            review=review,
                            rating=rating)
            id = rows[0][0]
            return feedback.get(id)
        except Exception as e:
            print(str(e))
            return None
    
    @staticmethod
    def add_s_review(uid, sid, review, rating):
        try:
            rows = app.db.execute('''
INSERT INTO Feedback(uid, sid, review, rating)
VALUES(:uid, :sid, :review,:rating)
RETURNING id
''',
                            uid=uid,
                            sid=sid,
                            review=review,
                            rating=rating)
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
    def get(id):
        rows = app.db.execute("""
SELECT id, review, rating
FROM Feedback
WHERE id = :id
""",
                              id=id)
        return Feedback(*(rows[0])) if rows else None

        