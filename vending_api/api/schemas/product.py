from vending_api.extensions import db, ma
from vending_api.models import Product


class ProductSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = Product
        sqla_session = db.session
        load_instance = True
