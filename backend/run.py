import logging
import os
from datetime import datetime as dt

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api

from src.resources import status

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.logger.info("Enabling CORS...")
CORS(app)
if 'LOG_FOLDER' in os.environ:
    app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "file")
    app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")

    # File Logging Setup
    app.config['LOG_DIR'] = os.environ.get("LOG_FOLDER", "/")
    app.config['APP_LOG_NAME'] = os.environ.get("APP_LOG_NAME", "praizl.log")
    app.config['WWW_LOG_NAME'] = os.environ.get("WWW_LOG_NAME", "praizl_www.log")
    app.config['LOG_MAX_BYTES'] = os.environ.get("LOG_MAX_BYTES", 500_000_000)  # 100MB in bytes
    app.config['LOG_COPIES'] = os.environ.get("LOG_COPIES", 5)

    from src.common.flask_logs import LogSetup

    logs = LogSetup()
    logs.init_app(app)


    @app.after_request
    def after_request(response):
        """ Logging after every request. """
        logger = logging.getLogger("app.access")
        logger.info(
            "%s [%s] %s %s %s %s %s %s %s",
            request.remote_addr,
            dt.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
            request.method,
            request.path,
            request.scheme,
            response.status,
            response.content_length,
            request.referrer,
            request.user_agent,
        )
        return response

api = Api(app)

#Resources
api.add_resource(status.Status, '/status')

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 80)))
    #DOCKER DEPLOYMENT
    #app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 80)))