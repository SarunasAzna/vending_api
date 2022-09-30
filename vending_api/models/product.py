from sqlalchemy.orm import validates

from vending_api.extensions import db
from vending_api.models.user import ALLOWED_COINS, User, RoleEnum


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

    @validates("cost")
    def validate_cost(self, key, cost):
        if cost <= 0:
            raise ValueError("Cost must be a positive amount")
        if cost % 5 != 0:
            raise ValueError("Cost must be a multiple of 5")
        return cost

    @validates("amountAvailable")
    def validate_amount_available(self, key, amount_available):
        if amount_available < 0:
            raise ValueError("amountAvailable cannot be negative")
        return amount_available

    def buy(self, amount, buyer):
        if buyer.role == RoleEnum.seller:
            raise PermissionError("Role of the buying user must be buyer")
        if amount > self.amountAvailable:
            raise ValueError(
                f"Not enough products. Requested: {amount}, available: {self.amountAvailable}"
            )
        total_cost = self.cost * amount
        if total_cost > buyer.deposit:
            raise ValueError(
                f"Not enough deposit. Please add at least {total_cost - buyer.deposit} to acquire the products."
            )
        self.amountAvailable -= amount
        change_amount = buyer.deposit - total_cost
        buyer.deposit = 0
        seller = User.query.get(self.user_id)
        seller.deposit += total_cost
        return self.give_change(change_amount)

    @staticmethod
    def give_change(change_amount):
        ALLOWED_COINS.sort(reverse=True)
        change = []
        for coin in ALLOWED_COINS:
            coint_amount = change_amount // coin
            change.extend([coin] * coint_amount)
            change_amount -= coin * coint_amount
            if change_amount <= 0:
                break
        return change
