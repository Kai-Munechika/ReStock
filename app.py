from flask import Flask, render_template, redirect
from mongo_util import *
app = Flask(__name__)


@app.route('/')
@app.route('/<name>')
def hello_world(name='World'):
    return render_template('hello.html', name=name)


@app.route('/rank')
@app.route('/rank/<int:n>')
def top_ranked_stocks(n=10):
    docs = get_top_n_ranked_companies(n)
    return render_template('rank.html', docs=docs)


if __name__ == '__main__':
    app.run(debug=True)