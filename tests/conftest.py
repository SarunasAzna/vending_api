import json

import pytest
from dotenv import load_dotenv
from pytest_factoryboy import register

from tests.factories import ProductFactory, UserFactory
from vending_api.app import create_app
from vending_api.extensions import db as _db
from vending_api.models import User

register(UserFactory)
register(ProductFactory)


@pytest.fixture
def seller_password():
    return "seller12345"


@pytest.fixture
def buyer_password():
    return "buyer12345"


@pytest.fixture(scope="session")
def app():
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def seller_user(db, seller_password):
    user = User(username="seller", password=seller_password, role="seller")

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def buyer_user(db, buyer_password):
    user = User(username="buyer", password=buyer_password, role="buyer")

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def seller_headers(seller_user, client, seller_password):
    data = {"username": seller_user.username, "password": seller_password}
    rep = client.post(
        "/auth/login",
        data=json.dumps(data),
        headers={"content-type": "application/json"},
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        "content-type": "application/json",
        "authorization": "Bearer %s" % tokens["access_token"],
    }


@pytest.fixture
def buyer_headers(buyer_user, client, buyer_password):
    data = {"username": buyer_user.username, "password": buyer_password}
    rep = client.post(
        "/auth/login",
        data=json.dumps(data),
        headers={"content-type": "application/json"},
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        "content-type": "application/json",
        "authorization": "Bearer %s" % tokens["access_token"],
    }


@pytest.fixture
def seller_refresh_headers(seller_user, client):
    data = {"username": seller_user.username, "password": "seller12345"}
    rep = client.post(
        "/auth/login",
        data=json.dumps(data),
        headers={"content-type": "application/json"},
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        "content-type": "application/json",
        "authorization": "Bearer %s" % tokens["refresh_token"],
    }
