from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class Account(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    create_time = database.Column(database.DateTime, default=datetime.utcnow)
    email = database.Column(database.String, nullable=False)
    gaia = database.Column(database.String, nullable=False)

    def __repr__(self):
        return "<Account 'id={0} email={1} gaia={2} create_time={3}'>".format(
            self.id, self.email, self.gaia, self.create_time
        )


class Feedback(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    url = database.Column(database.String, nullable=False)
    score = database.Column(database.Integer, nullable=False)
    description = database.Column(database.String(8000), nullable=False)
    timestamp = database.Column(database.DateTime, default=datetime.utcnow)
    account_id = database.Column(
        database.Integer, database.ForeignKey("account.id"), nullable=True
    )

    def __repr__(self):
        return "<Feedback 'id={0} time={3} url={4} score={5} description={6}'> from <Account 'id={5}'>".format(
            self.id,
            self.timestamp,
            self.url,
            self.score,
            self.description,
            self.account_id,
        )
