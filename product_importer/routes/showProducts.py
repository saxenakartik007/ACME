from flask_paginate import Pagination, get_page_args
from flask import Blueprint, request, render_template
from sqlalchemy import or_

from ..models import Products,db
show_products = Blueprint('home',  __name__,
                        template_folder='templates')
users = list(range(100))

@show_products.route('/')
def homepage():
    page, per_page, offset = get_page_args(page_parameter='page',
                                          per_page_parameter='per_page')
    total= db.session.query(Products).count()
    pagination_users = get_users(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('products.html',
                           users=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

@show_products.route('/search/<name>')
def search(name):
    print(name)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = db.session.query(Products).filer(or_(Products.name.like('%'+search+'%'),Products.sku.like('%'+search+'%'))).count()
    pagination_users = get_users(offset=offset, per_page=per_page,search=name)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('products.html',
                           users=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


def get_users(offset=0, per_page=10,search=None):
    if search is None:
        products = Products.query.with_entities(Products.name, Products.sku,Products.description).order_by(Products.name).offset(offset).limit(per_page).all()
    else:
        products = Products.query.filer(or_(Products.name.like('%'+search+'%'),Products.sku.like('%'+search+'%'))).with_entities(Products.name, Products.sku,Products.description).order_by(Products.name).offset(offset).limit(per_page).all()

    products = [list(elem) for elem in products]
    return products