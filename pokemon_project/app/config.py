class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1234567890@localhost:5432/pokemon"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
