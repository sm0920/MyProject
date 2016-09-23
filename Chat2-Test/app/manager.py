from bcrypt import hashpw, gensalt
from .db import db_session, User


def input_data(*args, **kwargs):
    kwargs['password'] = Password().encrypt(kwargs['password'])
    user = User(kwargs.get('userid'), kwargs.get('password'), kwargs.get('username'))

    db_session.add(user)
    db_session.commit()


class Password(object):
    def encrypt(self, password):
        password = password.encode('utf-8')
        return hashpw(password, gensalt())
    
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    def __eq__(self, other):
        self._password = self._password.encode('utf-8')
        other = other.encode('utf-8')
        return hashpw(self._password, other) == other
