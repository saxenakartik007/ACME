
from config import POSTGRES
from flask import Flask
from product_importer.routes.uploadProducts import upload_products
from product_importer.routes.index import home
from flask_sqlalchemy import SQLAlchemy
import config
from .models import db
app = Flask(__name__)


app.config['DEBUG'] = True
app.config["SQLALCHEMY_POOL_SIZE"]=50
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
print('postgresql://%(user)s:#%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES)
with app.app_context():
    db.init_app(app)
    db.app = app
app.app_context().push()


app.register_blueprint(upload_products)
app.register_blueprint(home)

if __name__ == '__main__':
    app.run()
