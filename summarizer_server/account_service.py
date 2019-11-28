from models import database, Account
from serializers import AccountSchema


class AccountService:
    def __init__(self):
        self.anonymous_email = "anonymous@jent.ly"
        self.anonymous_gaia = "ewpewawn"

        self.user_single = AccountSchema()
        self.user_multiple = AccountSchema(many=True)

    def serialize_single(self, account):
        return self.user_single.dump(account)

    def serialize_multiple(self, users):
        return self.user_multiple.dump(users)

    def get_or_create(self, email, gaia):
        account = self.get(email)
        if account is not None:
            print("Account <'email={0} gaia={1}'> already exists.".format(email, gaia))
            return account

        account = Account(email=email, gaia=gaia)
        database.session.add(account)
        database.session.commit()
        return account

    def get(self, email):
        account = Account.query.filter_by(email=email).first()
        if account is None:
            print("Account <'email={0}'> does not exist yet.".format(email))
            return None
        return account

    def get_all(self):
        return Account.query.order_by(Account.create_time.desc()).all()

    def get_anonymous(self):
        return self.get_or_create(self.anonymous_email, self.anonymous_gaia)
