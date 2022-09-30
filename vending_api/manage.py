import click
from flask.cli import with_appcontext


@click.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from vending_api.extensions import db
    from vending_api.models import Product, User

    for name in ["buyer", "seller"]:
        click.echo(f"create {name} user")
        user = User(username=name, password=f"{name}12345", role=name)
        db.session.add(user)
    for product in [
        {"productName": "coke", "user_id": 2, "cost": 15, "amountAvailable": 16},
        {"productName": "chocolate", "user_id": 2, "cost": 20, "amountAvailable": 42},
    ]:
        click.echo(f"create {product['productName']} user")
        prod = Product(**product)
        db.session.add(prod)
    db.session.commit()
    click.echo("created user admin")
