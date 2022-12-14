import pytest
from flask import url_for


@pytest.mark.parametrize("coins", [[5], [10], [20], [100], [5, 100]])
def test_deposit(coins, client, db, buyer_user, buyer_headers):
    user_url = url_for("api.deposit")
    db.session.refresh(buyer_user)
    expected_amount = 0
    for coin in coins:
        rep = client.post(user_url, json={"coin": coin}, headers=buyer_headers)
        assert rep.status_code == 200
        expected_amount += coin
        db.session.refresh(buyer_user)
        assert buyer_user.deposit == expected_amount


@pytest.mark.parametrize(
    "coin, explanation",
    [
        [-1, "Negative coin"],
    ],
)
def test_false_amount(coin, explanation, client, db, buyer_headers):
    user_url = url_for("api.deposit")
    rep = client.post(user_url, json={"coin": coin}, headers=buyer_headers)
    assert rep.status_code == 400


def test_deposit_only_buyer(client, db, seller_headers):
    user_url = url_for("api.deposit")
    rep = client.post(user_url, json={"coin": 5}, headers=seller_headers)
    assert rep.status_code == 403
