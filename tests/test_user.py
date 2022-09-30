from flask import url_for

from vending_api.extensions import pwd_context
from vending_api.models import User


def test_get_user(client, db, user, seller_headers):
    # test 404
    user_url = url_for("api.user_by_id", user_id="100000")
    rep = client.get(user_url, headers=seller_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user
    user_url = url_for("api.user_by_id", user_id=user.id)
    rep = client.get(user_url, headers=seller_headers)
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    assert data["username"] == user.username
    assert data["role"] == "buyer"


def test_put_user(client, db, user, seller_user, seller_headers):
    # test 404
    user_url = url_for("api.user_by_id", user_id="100000")
    rep = client.put(user_url, headers=seller_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    data = {"username": "updated", "password": "new_password"}

    user_url = url_for("api.user_by_id", user_id=user.id)
    # cannot change not self
    rep = client.put(user_url, json=data, headers=seller_headers)
    assert rep.status_code == 403
    # test update user
    user_url = url_for("api.user_by_id", user_id=seller_user.id)
    rep = client.put(user_url, json=data, headers=seller_headers)
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    assert data["username"] == "updated"

    db.session.refresh(seller_user)
    assert pwd_context.verify("new_password", seller_user.password)


def test_no_deposit_on_user_edit(client, db, seller_user, seller_headers):
    data = {
        "username": "updated",
        "password": "new_password",
        "deposit": 100,
        "role": "buyer",
    }

    user_url = url_for("api.user_by_id", user_id=seller_user.id)
    # test update user
    rep = client.put(user_url, json=data, headers=seller_headers)
    assert rep.status_code == 400
    assert rep.json["message"] == "deposit cannot be updated with this action"
    # test create user
    user_url = url_for("api.user")
    rep = client.post(user_url, json=data, headers=seller_headers)
    assert rep.status_code == 400
    assert rep.json["message"] == "deposit cannot be updated with this action"


def test_no_role_on_user_edit(client, db, seller_user, seller_headers):
    data = {"username": "updated", "password": "new_password", "role": "buyer"}

    user_url = url_for("api.user_by_id", user_id=seller_user.id)
    # test update user
    rep = client.put(user_url, json=data, headers=seller_headers)
    assert rep.status_code == 400
    assert rep.json["message"] == "Role cannot be changed"


def test_delete_user(client, db, user, seller_headers, seller_user):
    # test 404
    user_url = url_for("api.user_by_id", user_id="100000")
    rep = client.delete(user_url, headers=seller_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # delete not yourself
    user_url = url_for("api.user_by_id", user_id=user.id)
    rep = client.delete(user_url, headers=seller_headers)
    assert rep.status_code == 403
    # test get_user

    user_url = url_for("api.user_by_id", user_id=seller_user.id)
    rep = client.delete(user_url, headers=seller_headers)
    assert rep.status_code == 200
    assert db.session.query(User).filter_by(id=seller_user.id).first() is None


def test_allow_unauthenticated_user_creation(client, db):
    data = {"username": "Sir TestAlot", "password": "much secure", "role": "buyer"}
    users_url = url_for("api.user")
    resp = client.post(users_url, json=data)
    assert resp.status_code == 201
    resp_data = resp.get_json()
    user = db.session.query(User).filter_by(id=resp_data["user"]["id"]).first()

    assert user.username == data["username"]


def test_create_user(client, db, seller_headers):
    # test bad data
    users_url = url_for("api.user")
    data = {"username": "created"}
    rep = client.post(users_url, json=data, headers=seller_headers)
    assert rep.status_code == 400

    data["password"] = "adminadmin"
    data["role"] = "buyer"

    rep = client.post(users_url, json=data, headers=seller_headers)
    assert rep.status_code == 201

    data = rep.get_json()
    user = db.session.query(User).filter_by(id=data["user"]["id"]).first()

    assert user.username == "created"


def test_get_all_user(client, db, user_factory, seller_headers):
    users_url = url_for("api.user")
    users = user_factory.create_batch(30)

    db.session.add_all(users)
    db.session.commit()

    rep = client.get(users_url, headers=seller_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for user in users:
        assert any(u["id"] == user.id for u in results["results"])
