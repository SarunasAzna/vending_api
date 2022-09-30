from vending_api.extensions import ma


class BuySchema(ma.Schema):

    productId = ma.Int(required=True)
    amount = ma.Int(required=True)
