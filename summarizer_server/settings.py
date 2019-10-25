import os

# Raises exception if database environment variables are not set
def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


# TODO: separate dev and prod settings
class Settings:
    DB_NAME = "feedback.db"
    # Put the db file in source directory
    # SQLALCHEMY_DATABASE_URI = "sqlite:///{0}".format(DB_NAME)
    # Default port for PostgreSQL is 5432
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}".format(
        dbuser=get_env_variable("POSTGRES_USER"),
        dbpass=get_env_variable("POSTGRES_PW"),
        dbhost=get_env_variable("POSTGRES_URL"),
        dbname=get_env_variable("POSTGRES_DB"),
    )
    # Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
    # SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://postgres:password@localhost:5432/feedback'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
