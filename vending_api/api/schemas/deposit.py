from vending_api.extensions import ma


class DepositSchema(ma.Schema):

    coin = ma.Int(required=True)
