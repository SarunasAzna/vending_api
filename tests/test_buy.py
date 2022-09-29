from flask import url_for


def test_buy(client, db, buyer_user, buyer_headers, seller_user, product):
    user_url = url_for("api.buy")
    buyer_user.deposit_coin(100)
    product.user_id = seller_user.id
    product.cost = 5
    db.session.add(product)
    db.session.commit()
    amount_available = product.amountAvailable
    amount_to_buy = 2
    expected_change = [50, 20, 20]

    data = {
        "productId": product.id,
        "amount": amount_to_buy,
    }

    rep = client.post(user_url, json=data, headers=buyer_headers)
    assert rep.status_code == 200

    db.session.refresh(product)
    assert product.amountAvailable == amount_available - amount_to_buy
    assert buyer_user.deposit == 0
    assert rep.json["change"] == expected_change


