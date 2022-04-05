class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_DB = 'api_flask_cursos'
#Estos son los parametros de conexión a la BDD

config = {
    'development': DevelopmentConfig
}