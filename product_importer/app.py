
from config import POSTGRES
from flask import Flask
from product_importer.routes.uploadProducts import upload_products
from product_importer.routes.index import home
from product_importer.routes.showProducts import show_products
from uploadFileTask import createdramtatiq
from .models import db
import os

app = Flask(__name__)


app.config['DEBUG'] = True
app.config["SQLALCHEMY_POOL_SIZE"]=50
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
print('postgresql://%(user)s:#%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES)

app.config["DRAMATIQ_BROKER"]="dramatiq.brokers.rabbitmq.RabbitmqBroker"
#app.config["DRAMATIQ_BROKER_URL"]="redis://localhost:6379/0"
app.config["DRAMATIQ_BROKER_URL"]=os.environ.get('BROKER_URL', 'redis://localhost:6379/0')

#createdramtatiq(app)
with app.app_context():
    db.init_app(app)
    db.app = app
app.app_context().push()


app.register_blueprint(upload_products)
# app.register_blueprint(home)
app.register_blueprint(show_products)

if __name__ == '__main__':
    app.run()
