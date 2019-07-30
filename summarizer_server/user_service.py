from models import database, User
from serializers import UserSchema


class UserService:
    def __init__(self):
        self.anonymous_email = "anonymous@jent.ly"
        self.anonymous_gaia = "ewpewawn"

        self.user_single = UserSchema()
        self.user_multiple = UserSchema(many=True)

    def serialize_single(self, user):
        return self.user_single.dump(user)

    def serialize_multiple(self, users):
        return self.user_multiple.dump(users)

    def get_or_create(self, email, gaia):
        user = self.get(email)
        if user is not None:
            print("User <'email={0} gaia={1}'> already exists.".format(email, gaia))
            return user

        user = User(email=email, gaia=gaia)
        database.session.add(user)
        database.session.commit()
        return user

    def get(self, email):
        user = User.query.filter_by(email=email).first()
        if user is None:
            print("User <'email={0}'> does not exist yet.".format(email))
            return None
        return user

    def get_all(self):
        return User.query.order_by(User.create_time.desc()).all()

    def get_anonymous(self):
        return self.get_or_create(self.anonymous_email, self.anonymous_gaia)
