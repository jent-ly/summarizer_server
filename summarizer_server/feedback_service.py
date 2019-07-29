from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from serializers import FeedbackSchema

database = SQLAlchemy()


class Feedback(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    url = database.Column(database.String(255), nullable=False)
    score = database.Column(database.Integer, nullable=False)
    description = database.Column(database.String(10000), nullable=False)
    timestamp = database.Column(database.DateTime, default=datetime.utcnow)
    email = database.Column(database.String(255), nullable=False)
    gaia = database.Column(database.String(255), nullable=False)

    def __repr__(self):
        return "<Feedback '{0} {1} {2} at {3} for {4} rated {5} {6}'>".format(
            self.id,
            self.email,
            self.gaia,
            self.timestamp,
            self.url,
            self.score,
            self.description,
        )


class FeedbackService:
    def __init__(self):
        self.feedback_single = FeedbackSchema()
        self.feedback_multiple = FeedbackSchema(many=True)

    def submit(self, url, score, description, email, gaia):
        feedback = Feedback(
            url=url, score=score, description=description, email=email, gaia=gaia
        )
        database.session.add(feedback)
        database.session.commit()
        return {
            "message": "Successfully saved feedback",
            "feedback": self.feedback_single.dump(feedback),
        }

    def get_all(self):
        all_feedback = Feedback.query.order_by(Feedback.timestamp.desc()).all()
        return self.feedback_multiple.dump(all_feedback)
