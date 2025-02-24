import mongoengine as me
from flask_login import UserMixin


class User(me.Document, UserMixin):
    meta = {"collection": "users"}

    first_name = me.StringField(required=True)
    last_name = me.StringField(required=True)
    username = me.StringField(required=True, unique=True)
    password = me.StringField(required=True)
    email = me.StringField(required=True, unique=True)
    roles = me.ListField(me.StringField(), default=["user"])

    def set_password(self, password):
        from werkzeug.security import generate_password_hash

        self.password = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash

        return check_password_hash(self.password, password)
