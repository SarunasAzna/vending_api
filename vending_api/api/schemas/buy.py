from vending_api.extensions import db, ma


class BuySchema(ma.Schema):

    productId = ma.Int(required=True)
    amount = ma.Int(required=True)
