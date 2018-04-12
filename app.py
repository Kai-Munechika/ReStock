from flask import Flask, render_template, redirect, jsonify, request
import requests
from mongo_util import *
from meta import sectors_to_industries
from historical_data import HistoricalData
import sys
import json

app = Flask(__name__)
historical_data_client = HistoricalData("IEX", True)

# Note: this endpoint just checks that we can successfully pass data to some html template; Helen will work on the front-end templates
@app.route('/')
@app.route('/<name>')
def hello_world(name='World'):
    sort_keys = {'ROA', 'pe_ratio', 'rank'}
    return render_template('index.html', sectors_to_industries=sectors_to_industries, sort_keys=sort_keys)


# takes in user input from the landing page (sector & budget)
@app.route('/handleData', methods=['POST'])
def handleData():
    # for now, sort by (n=10, filter_attribute = sector, filter_value = user selected sector, sort_attribute = rank, order = ASCENDING)

    sector = request.form['sector']
    budget = int(request.form['budget'])
    n = 10
    filter_attribute = 'sector'
    filter_value = sector
    sort_attribute = 'rank'
    order = 'ASCENDING'
    data = json.loads(filter_and_sort(n,filter_attribute,filter_value,sort_attribute,order,budget).data)
    return render_template('results.html', companies=data, budget=budget,sector=filter_value, sectors_to_industries=sectors_to_industries)


@app.route('/profile/<string:symbol>')
def profile(symbol):
    data = historical_data_client.get_historical_data(symbol)
    return render_template('profile.html', data=data, symbol=symbol.upper())


# APIs

@app.route('/api/rank')
@app.route('/api/rank/<int:n>')
def rank(n=50):
    return jsonify(get_top_n_ranked_companies(n))


@app.route('/api/company/<string:_id>')
def company(_id):
    return jsonify(get_company(_id.upper()))


@app.route('/api/filter/<int:n>/<string:filter_attribute>/<string:filter_value>/<string:sort_attribute>/<string:order>')
def filter_and_sort(n, filter_attribute, filter_value, sort_attribute, order, price_cap):
    assert(order == 'ASCENDING' or order == 'DESCENDING')
    if order == 'ASCENDING':
        order = ASCENDING
    else:
        order = DESCENDING

    return jsonify(get_top_n_companies_filtered(n, filter_attribute, filter_value, sort_attribute, order, price_cap))


if __name__ == '__main__':
    app.run(debug=True)

