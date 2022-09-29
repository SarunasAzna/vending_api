from flask import url_for


def test_get_product(client, db, product):
    # test 404
    user_url = url_for("api.product_by_id", product_id="1")
    rep = client.get(user_url)
    assert rep.status_code == 404

    db.session.add(product)
    db.session.commit()

    # test get_user
    user_url = url_for("api.product_by_id", product_id=product.id)
    rep = client.get(user_url)
    assert rep.status_code == 200

    data = rep.get_json()["product"]
    assert data["productName"] == product.productName
