from flask import Flask, render_template, redirect, jsonify
from mongo_util import *
from meta import sectors_to_industries
from historical_data import HistoricalData

app = Flask(__name__)
historical_data_client = HistoricalData("IEX", True)

# Note: this endpoint just checks that we can successfully pass data to some html template; Helen will work on the front-end templates
@app.route('/')
@app.route('/<name>')
def hello_world(name='World'):
    sort_keys = {'ROA', 'pe_ratio', 'rank'}
    return render_template('index.html', sectors_to_industries=sectors_to_industries, sort_keys=sort_keys)


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
def filter_and_sort(n, filter_attribute, filter_value, sort_attribute, order):
    assert(order == 'ASCENDING' or order == 'DESCENDING')
    if order == 'ASCENDING':
        order = ASCENDING
    else:
        order = DESCENDING

    return jsonify(get_top_n_companies_filtered(n, filter_attribute, filter_value, sort_attribute, order))


if __name__ == '__main__':
    app.run(debug=True)