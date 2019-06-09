import os
from flask import render_template, Blueprint

home = Blueprint('home',  __name__,
                        template_folder='templates')


@home.route('/')
def homepage():
    # Route to serve the upload form
    return render_template('index.html')