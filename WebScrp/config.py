import os

APP_ENV = os.getenv('APP_ENV', 'development')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'krzc')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'krzc')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'webscrp')
TEST_DATABASE_NAME = os.getenv('DATABASE_NAME', 'WebScrp_test')
