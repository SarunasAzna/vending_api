import pytest
from flask import url_for


def test_buy(
    client, db, buyer_user, buyer_headers, seller_user, product, seller_headers
):
    user_url = url_for("api.buy")
    buyer_user.deposit_coin(100)
    seller_user.deposit = 0
    product.user_id = seller_user.id
    cost = 5
    product.cost = cost
    db.session.add(product)
    db.session.commit()
    amount_available = product.amountAvailable
    amount_to_buy = 2
    expected_change = [50, 20, 20]

    data = {
        "productId": product.id,
        "amount": amount_to_buy,
    }
    # test 403
    rep = client.post(user_url, json=data, headers=seller_headers)
    assert rep.status_code == 403
    # test 200

    rep = client.post(user_url, json=data, headers=buyer_headers)
    assert rep.status_code == 200

    db.session.refresh(product)
    db.session.refresh(buyer_user)
    db.session.refresh(seller_user)
    assert product.amountAvailable == amount_available - amount_to_buy
    assert buyer_user.deposit == 0
    assert rep.json["change"] == expected_change
    assert seller_user.deposit == amount_to_buy * cost


@pytest.mark.parametrize(
    "amount_available, deposit, amount_to_buy, product_cost, expected_in_error",
    [
        [0, 100, 2, 10, "Not enough products"],
        [4, 100, 5, 10, "Not enough products"],
        [10, 10, 1, 20, "Not enough deposit"],
    ],
)
def test_buy_error(
    amount_available,
    deposit,
    amount_to_buy,
    product_cost,
    expected_in_error,
    client,
    db,
    buyer_user,
    buyer_headers,
    seller_user,
    product,
):
    url = url_for("api.buy")
    buyer_user.reset()
    buyer_user.deposit_coin(deposit)
    product.user_id = seller_user.id
    product.cost = product_cost
    db.session.add(product)
    db.session.commit()
    product.amountAvailable = amount_available
    amount_to_buy = amount_to_buy

    data = {
        "productId": product.id,
        "amount": amount_to_buy,
    }

    rep = client.post(url, json=data, headers=buyer_headers)
    assert rep.status_code == 400

    db.session.refresh(product)
    db.session.refresh(buyer_user)
    assert product.amountAvailable == amount_available
    assert expected_in_error in rep.json["message"]
    assert buyer_user.deposit == deposit
