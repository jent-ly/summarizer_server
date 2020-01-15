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
    def __init__(self):
        # Default port for PostgreSQL is 5432
        self.SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}".format(
            dbuser=get_env_variable("POSTGRES_USER"),
            dbpass=get_env_variable("POSTGRES_PASSWORD"),
            dbhost=get_env_variable("POSTGRES_URL"),
            dbname=get_env_variable("POSTGRES_DB"),
        )
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.DEBUG = True
