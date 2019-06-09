from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class Products(BaseModel, db.Model):
    """Model for the products table"""
    __tablename__ = 'products'

    name = db.Column(db.String(200))
    sku = db.Column(db.String(200), primary_key = True)
    description = db.Column(db.String(4000))

    def __init__(self,name,sku,description):
        self.name=name
        self.sku=sku
        self.description=description