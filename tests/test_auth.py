import json

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

def test_already_an_active_session(seller_user, client):
    data = {"username": seller_user.username, "password": "seller"}
    for i in range(2):
        rep = client.post(
            "/auth/login",
            data=json.dumps(data),
            headers={"content-type": "application/json"},
        )
    assert rep.json["message"] == "There is already an active session using your account"
