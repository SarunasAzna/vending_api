from sqlalchemy.orm import validates

from vending_api.extensions import db


class Product(db.Model):
    """Product model"""

    id = db.Column(db.Integer, primary_key=True)
    amountAvailable = db.Column(db.Integer, nullable=False, default=0)
    productName = db.Column(db.String(100), unique=True, nullable=False)
    cost = db.Column(db.Integer, nullable=False, default=5)
    user_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)

    def __repr__(self):
        return (
            f"{self.productName}, available: {self.amountAvailable}, cost: {self.cost}"
        )
        return "<User %s>" % self.username

    @validates("cost")
    def validate_cost(self, key, cost):
        if cost == 0:
            raise ValueError("Cost cannot be 0")
        if cost % 5 != 0:
            raise ValueError("Cost must be a multiple of 5")
        return cost
