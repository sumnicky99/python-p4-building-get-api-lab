#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    # Query all bakeries from the database
    bakeries = Bakery.query.all()
    # Serialize the data using a list comprehension
    bakeries_json = [bakery.to_dict() for bakery in bakeries]
    return make_response(jsonify(bakeries_json), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    # Query a single bakery by its ID
    bakery = Bakery.query.get_or_404(id)
    # Serialize the data, including nested baked goods
    bakery_json = bakery.to_dict(nested=True)
    return make_response(jsonify(bakery_json), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # Query baked goods sorted by price in descending order
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    # Serialize the data using a list comprehension
    baked_goods_json = [baked_good.to_dict() for baked_good in baked_goods]
    return make_response(jsonify(baked_goods_json), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # Query the most expensive baked good
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    # Serialize the data
    baked_good_json = baked_good.to_dict()
    return make_response(jsonify(baked_good_json), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
