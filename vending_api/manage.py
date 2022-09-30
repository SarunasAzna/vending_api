import click
from flask.cli import with_appcontext


@click.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from vending_api.extensions import db
    from vending_api.models import User

    click.echo("create user")
    user = User(username="admin", password="adminadmin", active=True, role="seller")
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")
