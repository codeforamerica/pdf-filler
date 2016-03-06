from peewee import SqliteDatabase
db = SqliteDatabase('my_default.db')

from flask_marshmallow import Marshmallow
ma = Marshmallow()

from flask_migrate import Migrate
migrate = Migrate()
