from flask import Flask, render_template, redirect, jsonify
from mongo_util import *
app = Flask(__name__)


@app.route('/')
@app.route('/<name>')
def hello_world(name='World'):
    return render_template('hello.html', name=name)


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