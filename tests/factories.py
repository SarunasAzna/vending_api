import factory

from vending_api.models import User


class UserFactory(factory.Factory):

    username = factory.Sequence(lambda n: "user%d" % n)
    password = "mypwd"
    role = "buyer"

    class Meta:
        model = User
