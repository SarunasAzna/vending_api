from vending_api.extensions import db, ma


class DepositSchema(ma.Schema):

    coin = ma.Int()

