from datetime import datetime

from models import database, Feedback, User
from serializers import FeedbackSchema


class FeedbackService:
    def __init__(self):
        self.feedback_single = FeedbackSchema()
        self.feedback_multiple = FeedbackSchema(many=True)

    def serialize_single(self, feedback):
        return self.feedback_single.dump(feedback)

    def serialize_multiple(self, feedback_multiple):
        return self.feedback_multiple.dump(feedback_multiple)

    def submit(self, url, score, description, user_id):
        feedback = Feedback(
            url=url, score=score, description=description, user_id=user_id
        )
        database.session.add(feedback)
        database.session.commit()
        return feedback

    def get_all(self):
        return Feedback.query.order_by(Feedback.timestamp.desc()).all()
