import os

basedir = os.path.abspath(os.path.dirname(__file__))



class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    app_dir = os.path.join(basedir, 'app')
    static_dir = os.path.join(app_dir, 'static')
    upload_dir = os.path.join(static_dir, 'upload')
    found_dir = os.path.join(upload_dir, 'found')       # The directory for storing the photos of found items
    avatar_dir = os.path.join(upload_dir, 'avatar')     # The directory for storing the avatars of users

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


# if __name__ == '__main__':
#     print(basedir)
#     print(Config.app_dir)
#     print(Config.static_dir)
#     print(Config.upload_dir)
#     print(Config.found_dir)
#     print(Config.avatar_dir)
