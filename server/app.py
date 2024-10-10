#!/usr/bin/env python3

from flask import Flask, jsonify
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

@app.route('/bakeries', methods=['GET'])
def bakeries():
    """Returns a list of JSON objects for all bakeries in the database."""
    bakeries = Bakery.query.all()
    return jsonify([bakery.to_dict() for bakery in bakeries])

@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    """Returns a single bakery as JSON with its baked goods nested in a list."""
    bakery = Bakery.query.get_or_404(id)
    return jsonify(bakery.to_dict())

@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    """Returns a list of baked goods as JSON, sorted by price in descending order."""
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([baked_good.to_dict() for baked_good in baked_goods])

@app.route('/baked_goods/most_expensive', methods=['GET'])
def most_expensive_baked_good():
    """Returns the single most expensive baked good as JSON."""
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return jsonify(most_expensive.to_dict()) if most_expensive else jsonify({})

if __name__ == '__main__':
    app.run(port=5555, debug=True)
