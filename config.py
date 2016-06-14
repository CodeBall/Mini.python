import os


class Config:

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (
        os.environ.get('DATABASE_USERNAME', 'root'),
        os.environ.get('DATABASE_PASSWORD', 'BIG BEN'),
        os.environ.get('DATABASE_HOST', 'localhost'),
        os.environ.get('DATABASE_DB', 'chaoge'),
    )