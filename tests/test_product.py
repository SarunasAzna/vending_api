from flask import url_for


def test_get_product(client, db, product):
    # test 404
    product_url = url_for("api.product_by_id", product_id="1")
    rep = client.get(product_url)
    assert rep.status_code == 404

    db.session.add(product)
    db.session.commit()

    # test get_product
    product_url = url_for("api.product_by_id", product_id=product.id)
    rep = client.get(product_url)
    assert rep.status_code == 200

    data = rep.get_json()["product"]
    assert data["productName"] == product.productName


def test_put_product(client, db, product, admin_headers):
    # test 404
    product_url = url_for("api.product_by_id", product_id="100000")
    rep = client.put(product_url, headers=admin_headers)
    assert rep.status_code == 404
    # test 401
    product_url = url_for("api.product_by_id", product_id="100000")
    rep = client.put(product_url)
    assert rep.status_code == 401

    db.session.add(product)
    db.session.commit()

    data = {"productName": "updated", "amountAvailable": 10, "cost": 10}

    product_url = url_for("api.product_by_id", product_id=product.id)
    # test update product
    rep = client.put(product_url, json=data, headers=admin_headers)
    assert rep.status_code == 200

    rep_data = rep.get_json()["product"]
    db.session.refresh(product)
    assert rep_data["productName"] == "updated" == product.productName
    assert rep_data["amountAvailable"] == 10 == product.amountAvailable
    assert rep_data["cost"] == 10 == product.cost

