from flask import current_app as app


class Feedback:
    def __init__(self, id, uid, pid, submitted_timestamp, review, rating):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.submitted_timestamp = submitted_timestamp
        self.review = review
        self.rating = rating

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT id, uid, pid, submitted_timestamp, review, rating
FROM Feedback
'''
                              )
        return [Feedback(*row) for row in rows]

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, submitted_timestamp, review, rating
FROM Feedback
WHERE id = :id
''',
                              id=id)
        return Feedback(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, submitted_timestamp, review, rating
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
SELECT id, uid, pid, submitted_timestamp, review, rating
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
    def add_review(uid, review, rating):
        try:
            rows = app.db.execute('''
    INSERT INTO Feedback(uid, review, rating)
    VALUES(:uid, :review,:rating)
    RETURNING id
    ''',
                            uid=uid,
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
SET review = review
WHERE id=id
''',
                              review=review,
                              id=id)
    
    @staticmethod
    def update_rating(id, rating):
        rows = app.db.execute('''
UPDATE Feedback
SET rating = rating
WHERE id=id
''',
                              rating=rating,
                              id=id)
    
    @staticmethod
    def delete_review(id):
       rows = app.db.execute('''
DELETE FROM Feedback
WHERE id=id
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

        