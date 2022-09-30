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
def seller_user(db):
    user = User(username="seller", password="seller", role="seller")

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def buyer_user(db):
    user = User(username="buyer", password="buyer", role="buyer")

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def seller_headers(seller_user, client):
    data = {"username": seller_user.username, "password": "seller"}
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
def buyer_headers(buyer_user, client):
    data = {"username": buyer_user.username, "password": "buyer"}
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
    data = {"username": seller_user.username, "password": "seller"}
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
