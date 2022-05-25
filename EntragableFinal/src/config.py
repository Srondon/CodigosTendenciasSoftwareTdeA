from distutils.debug import DEBUG


class Config:
    SECRET_KEY = 'abcdefghijklmn'

class DevelopmentConfig(Config):
    DEBUG= True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Angela.maria15'
    MYSQL_DB = 'tdeacursos'

config= {
    'development': DevelopmentConfig
}