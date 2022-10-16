from flask import current_app as app


class Feedback:
    def __init__(self, id, uid, pid, time_submitted, review, rating):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_submitted = time_submitted
        self.review = review
        self.rating = rating

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_submitted, review, rating
FROM Feedback
WHERE id = :id
''',
                              id=id)
        return Feedback(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, time_submitted, review, rating
FROM Feedback
WHERE uid = :uid
AND time_submitted >= :since
ORDER BY time_submitted DESC
''',
                              uid=uid,
                              since=since)
        return [Feedback(*row) for row in rows]
