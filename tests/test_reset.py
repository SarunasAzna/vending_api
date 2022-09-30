from flask import url_for


def test_reset(client, db, buyer_user, buyer_headers):
    user_url = url_for("api.reset")
    buyer_user.deposit_coin(100)
    db.session.commit()
    rep = client.post(user_url, headers=buyer_headers)
    assert rep.status_code == 200
    db.session.refresh(buyer_user)
    assert buyer_user.deposit == 0


def test_reset_only_buyer(client, db, seller_headers):
    user_url = url_for("api.reset")
    rep = client.post(user_url, headers=seller_headers)
    assert rep.status_code == 403
