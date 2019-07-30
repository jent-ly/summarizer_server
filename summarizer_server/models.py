from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    create_time = database.Column(database.DateTime, default=datetime.utcnow)
    email = database.Column(database.String(255), nullable=False)
    gaia = database.Column(database.String(255), nullable=False)

    def __repr__(self):
        return "<User 'id={0} email={1} gaia={2} create_time={3}'>".format(
            self.id, self.email, self.gaia, self.create_time
        )


class Feedback(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    url = database.Column(database.String(255), nullable=False)
    score = database.Column(database.Integer, nullable=False)
    description = database.Column(database.String(10000), nullable=False)
    timestamp = database.Column(database.DateTime, default=datetime.utcnow)
    user_id = database.Column(
        database.Integer, database.ForeignKey("user.id"), nullable=True
    )

    def __repr__(self):
        return "<Feedback 'id={0} time={3} url={4} score={5} description={6}'> from <User 'id={5}'>".format(
            self.id,
            self.timestamp,
            self.url,
            self.score,
            self.description,
            self.user_id,
        )
