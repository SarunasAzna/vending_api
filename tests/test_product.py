from flask import url_for
from vending_api.models import Product
import pytest

def test_get_product(client, db, product, seller_headers, buyer_headers):
    # test 404
    product_url = url_for("api.product_by_id", product_id="1")
    rep = client.get(product_url, headers=seller_headers)
    assert rep.status_code == 404

    db.session.add(product)
    db.session.commit()

    # test get_product
    product_url = url_for("api.product_by_id", product_id=product.id)
    rep = client.get(product_url, headers=seller_headers)
    rep_buyer = client.get(product_url, headers=buyer_headers)
    assert rep.status_code == 200

    data = rep.get_json()["product"]
    data_buyer = rep_buyer.get_json()["product"]
    assert data_buyer == data
    assert data["productName"] == product.productName


def test_put_product(client, db, product, seller_headers, buyer_headers):
    # test 404
    product_url = url_for("api.product_by_id", product_id="100000")
    rep = client.put(product_url, headers=seller_headers)
    assert rep.status_code == 404

    db.session.add(product)
    db.session.commit()

    data = {"productName": "updated", "amountAvailable": 10, "cost": 10}

    product_url = url_for("api.product_by_id", product_id=product.id)
    # test update product
    rep = client.put(product_url, json=data, headers=seller_headers)
    assert rep.status_code == 200

    rep_data = rep.get_json()["product"]
    db.session.refresh(product)
    assert rep_data["productName"] == "updated" == product.productName
    assert rep_data["amountAvailable"] == 10 == product.amountAvailable
    assert rep_data["cost"] == 10 == product.cost


def test_delete_product(client, db, product, seller_headers):
    # test 404
    product_url = url_for("api.product_by_id", product_id="100000")
    rep = client.delete(product_url, headers=seller_headers)
    assert rep.status_code == 404

    db.session.add(product)
    db.session.commit()

    # test delete_product
    product_url = url_for("api.product_by_id", product_id=product.id)
    rep = client.delete(product_url, headers=seller_headers)
    assert rep.status_code == 200
    assert db.session.query(Product).filter_by(id=product.id).first() is None

@pytest.mark.parametrize("url, method", [
    ["api.product_by_id", "put"],
    ["api.product_by_id", "delete"],
])
def test_not_owner(url, method, client, db, product, seller_headers, buyer_headers):
    db.session.add(product)
    db.session.commit()
    # test 401
    product_url = url_for(url, product_id="100000")
    rep = getattr(client, method)(product_url)
    assert rep.status_code == 401
    # test 403 not seller
    product_url = url_for(url, product_id="100000")
    rep = getattr(client, method)(product_url, headers=buyer_headers)
    assert rep.status_code == 403
    # test 403 not owner
    product.user_id = 2
    db.session.commit()
    product_url = url_for(url, product_id=product.id)
    rep = getattr(client, method)(product_url, headers=seller_headers)
    assert rep.status_code == 403

