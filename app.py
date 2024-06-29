import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from rest.newsFetcherREST import news_fetcher_blueprint
from rest.priceInfoREST import price_info_blueprint
from rest.tradeREST import trade_blueprint
from rest.positionRest import position_blueprint
from rest.historyRest import history_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set up logging
if not app.debug:
    # Create a file handler object
    file_handler = RotatingFileHandler('app2.log', maxBytes=10240, backupCount=10)
    
    # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    file_handler.setLevel(logging.INFO)
    
    # Create a logging format
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)
    
    # Add the file handler to the app's logger
    app.logger.addHandler(file_handler)
    
    # Create a console handler to also log to the terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Add the console handler to the app's logger
    app.logger.addHandler(console_handler)
    
    # Add the same handlers to the custom loggers
    logger = logging.getLogger('logger_info')
    #logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)

app.register_blueprint(news_fetcher_blueprint, url_prefix='/api')
app.register_blueprint(price_info_blueprint, url_prefix='/api')
app.register_blueprint(trade_blueprint, url_prefix='/api')
app.register_blueprint(position_blueprint, url_prefix='/api')
app.register_blueprint(history_blueprint, url_prefix='/api')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
