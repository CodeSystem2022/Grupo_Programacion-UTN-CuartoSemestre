class Config:
    SECRET_KEY = '7811cb752097e9ea4a8ca184582ef8649a27aaab6648fc41'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'ecommerce'

config = {
    'development': DevelopmentConfig
}