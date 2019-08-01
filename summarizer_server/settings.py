# TODO: separate dev and prod settings
class Settings:
    DB_NAME = "feedback.db"
    # Put the db file in source directory
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}".format(DB_NAME)
    DEBUG = True
