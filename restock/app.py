import json
import logging.config

from flask import Flask, render_template, jsonify, request
from pymongo import ASCENDING, DESCENDING

from restock.controller.Company import Companies
from restock.model.historical_data import HistoricalData
from restock.util.meta import sectors_to_industries


class LoggerConfig:
    dictConfig = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': { 'format': '%(asctime)s - %(name)s - %(levelname)s - '
                          '%(message)s - [in %(pathname)s:%(lineno)d]'},
            'short': { 'format': '%(message)s' }
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'restock.log',
                'maxBytes': 5000000,
                'backupCount': 10
            },
            'debug': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler'
            },
           'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG'
           },
        },
        'loggers': {
            'restock': {
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': True},
            'werkzeug': { 'propagate': True },
        },
        # 'root': { 'level': 'DEBUG', 'handlers': ['console'] }
    }


app = Flask(__name__)

# 'always' (default), 'never',  'production', 'debug'
app.config['LOGGER_HANDLER_POLICY'] = 'always'
# define which logger to use for Flask
app.config['LOGGER_NAME'] = 'restock'
#  initialise logger
app.logger
logging.config.dictConfig(LoggerConfig.dictConfig)

#TODO: clean me up! it is just an example
# example using log in diff levels
app.logger.debug('debug message')
app.logger.info('info message')
app.logger.warn('warn message')
app.logger.error('error message')
app.logger.critical('critical message')

historical_data_client = HistoricalData("IEX", True)

# Note: this endpoint just checks that we can successfully pass data to some
# html template; Helen will work on the front-end templates
@app.route('/')
@app.route('/<name>')
def hello_world(name='World'):
    sort_keys = {'ROA', 'pe_ratio', 'rank'}
    return render_template('index.html',
                           sectors_to_industries=sectors_to_industries,
                           sort_keys=sort_keys)


# takes in user input from the landing page (sector & budget)
@app.route('/handleData', methods=['POST'])
def handleData():
    # for now, sort by (n=10, filter_attribute = sector,
    # filter_value = user selected sector,
    # sort_attribute = rank, order = ASCENDING)

    sector = request.form['sector']
    budget = request.form['budget']
    n = 10
    filter_attribute = 'sector'
    filter_value = sector
    sort_attribute = 'rank'
    order = 'ASCENDING'
    data = json.loads(filter_and_sort(n, filter_attribute, filter_value,
                                      sort_attribute, order).data)
    return render_template('results.html', companies=data, budget=budget,
                           sector=filter_value,
                           sectors_to_industries=sectors_to_industries)


@app.route('/profile/<string:symbol>')
def profile(symbol):
    data = historical_data_client.get_historical_data(symbol)
    return render_template('profile.html', data=data, symbol=symbol.upper())


# APIs

@app.route('/api/rank')
@app.route('/api/rank/<int:n>')
def rank(n=50):
    companies = Companies()
    return jsonify(companies.get_top_n_ranked_companies(n))


@app.route('/api/company/<string:_id>')
def company(_id):
    companies = Companies()
    return jsonify(companies.get_company(_id.upper()))


@app.route('/api/filter/<int:n>/<string:filter_attribute>/\
            <string:filter_value>/<string:sort_attribute>/<string:order>')
def filter_and_sort(n, filter_attribute, filter_value, sort_attribute, order):
    assert (order == 'ASCENDING' or order == 'DESCENDING')
    if order == 'ASCENDING':
        order = ASCENDING
    else:
        order = DESCENDING

    companies = Companies()
    return jsonify(companies.get_top_n_companies_filtered(n,
                                                          filter_attribute,
                                                          filter_value,
                                                          sort_attribute,
                                                          order))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
