from flask import Flask, request, jsonify
from rest.newsFetcherREST import news_fetcher_blueprint
from rest.priceInfoREST import price_info_blueprint


app = Flask(__name__)

app.register_blueprint(news_fetcher_blueprint, url_prefix='/api')
app.register_blueprint(price_info_blueprint, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True)
