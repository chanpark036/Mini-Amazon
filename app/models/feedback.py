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
        if (len(rows) >= 5):
            return [Feedback(rows[row]) for row in range(k)]
        else :
            return [Feedback(*row) for row in rows]
        