from flask import Flask, render_template, redirect, jsonify, request
import requests
from mongo_util import *
from meta import sectors_to_industries
from historical_data import HistoricalData
import sys
import json

app = Flask(__name__)
historical_data_client = HistoricalData("IEX", True)
DATA_SOURCE = "IEX"

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
    return render_template('results.html', companies=data, budget=budget,sector=filter_value, sectors_to_industries=sectors_to_industries, radio_index=0)


@app.route('/results/<sector>/<int:budget>/<sort_by>/<int:radio_index>', methods=['GET'])
def results(sector, budget, sort_by, radio_index):
    NUM_COMPANIES_TO_RETURN = 10

    sort_attribute = ""
    order = "DESCENDING"
    if sort_by == "Rankings":
        sort_attribute = "rank"
        order = "ASCENDING"
    elif sort_by ==  "Price (Ascending)":
        sort_attribute = "price"
        order = "ASCENDING"
    elif sort_by ==  "Price (Descending)":
        sort_attribute = "price"
    elif sort_by == "Performance Rating":
        sort_attribute = "ROA"
    elif sort_by == "Future Profit Potential":
        sort_attribute = "pe_ratio"
        order = "ASCENDING"
    else:
        return "something went wrong"

    data = json.loads(filter_and_sort(NUM_COMPANIES_TO_RETURN, 'sector', sector, sort_attribute, order, budget).data)
    return render_template('results.html', companies=data, budget=budget,sector=sector, sectors_to_industries=sectors_to_industries, radio_index=radio_index)

@app.route('/profile/<string:symbol>')
def profile(symbol):
    data = historical_data_client.get_historical_data(symbol)
    _company = json.loads(company(symbol).data)
    press = json.loads(get_press(symbol).data)
    market_cap = format_market_cap(_company['market_cap'])
    return render_template('profile.html', data=data, symbol=symbol.upper(), _company=_company, press=press, market_cap=market_cap)


# src: https://stackoverflow.com/questions/579310/formatting-long-numbers-as-strings-in-python
def format_market_cap(market_cap):
    if not market_cap:
        return "N/A"
    magnitude = 0
    while abs(market_cap) >= 1000:
        magnitude += 1
        market_cap /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (market_cap, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

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

@app.route('/api/news/<string:symbol>')
def get_press(symbol):
    if DATA_SOURCE == 'IEX':
        r = requests.get(url='https://api.iextrading.com/1.0/stock/{}/news'.format(symbol))
        as_list_of_dicts = json.loads(r.text)
        return jsonify(as_list_of_dicts)
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)

