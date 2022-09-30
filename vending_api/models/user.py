import enum

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from vending_api.extensions import db, pwd_context


class RoleEnum(enum.Enum):
    buyer = "buyer"
    seller = "seller"


ALLOWED_COINS = [5, 10, 20, 50, 100]


class User(db.Model):
    """Basic user model"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    deposit = db.Column(db.Integer, default=0)
    role = db.Column(db.Enum(RoleEnum))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return "<User %s>" % self.username

    @validates("deposit")
    def validate_deposit(self, key, deposit):
        if deposit < 0:
            raise ValueError("Deposit must be greater than 0")
        if deposit % 5 != 0:
            raise ValueError("Deposit must be a multiple of 5")
        return deposit

    def deposit_coin(self, coin):
        if self.role != RoleEnum.buyer:
            raise PermissionError("Only buyer can deposit coins")
        if coin not in ALLOWED_COINS:
            raise ValueError(f"Only coins {ALLOWED_COINS} are allowed")
        self.deposit += coin

    def reset(self):
        if self.role != RoleEnum.buyer:
            raise PermissionError("Only buyer can deposit coins")
        self.deposit = 0
