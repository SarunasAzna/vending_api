import json

from vending_api.models import TokenBlocklist


def test_revoke_access_token(client, seller_headers):
    resp = client.delete("/auth/revoke_access", headers=seller_headers)
    assert resp.status_code == 200

    resp = client.get("/api/v1/user", headers=seller_headers)
    assert resp.status_code == 401


def test_revoke_refresh_token(client, seller_refresh_headers):
    resp = client.delete("/auth/revoke_refresh", headers=seller_refresh_headers)
    assert resp.status_code == 200

    resp = client.post("/auth/refresh", headers=seller_refresh_headers)
    assert resp.status_code == 401


def test_already_an_active_session(seller_user, client, seller_password):
    data = {"username": seller_user.username, "password": seller_password}
    for _ in range(2):
        rep = client.post(
            "/auth/login",
            data=json.dumps(data),
            headers={"content-type": "application/json"},
        )
    assert (
        rep.json["message"] == "There is already an active session using your account"
    )


def test_logout_all_tokens(db, seller_user, client, seller_headers):
    data = {"username": seller_user.username, "password": "seller"}
    for _ in range(2):
        client.post(
            "/auth/login",
            data=json.dumps(data),
            headers={"content-type": "application/json"},
        )
    # can get info
    rep = client.get(
        f"/api/v1/user/{seller_user.id}",
        headers=seller_headers,
    )
    assert rep.status_code == 200
    # Check that we have active tokens
    active_tokens = TokenBlocklist.query.filter_by(
        user_id=seller_user.id, revoked=False
    ).all()
    assert len(active_tokens) > 0
    # logout from all
    rep = client.delete(
        "/auth/logout/all",
        headers=seller_headers,
    )
    assert rep.status_code == 200
    active_tokens = TokenBlocklist.query.filter_by(
        user_id=seller_user.id, revoked=False
    ).all()
    assert len(active_tokens) == 0

    # cannot get info
    rep = client.get(
        f"/api/v1/user/{seller_user.id}",
        headers=seller_headers,
    )
    assert rep.status_code == 401
