import factory

from vending_api.models import User, Product


class UserFactory(factory.Factory):

    username = factory.Sequence(lambda n: "user%d" % n)
    password = "mypwd"
    role = "buyer"

    class Meta:
        model = User


class ProductFactory(factory.Factory):

    productName = factory.Sequence(lambda n: "product%d" % n)
    amountAvailable = 10
    cost = 50
    user_id = 1

    class Meta:
        model = Product
