import classwork
import config
from flask import current_app, Flask, redirect, request, session, url_for
app = classwork.create_app(config)

##app.register_blueprint(crud, url_prefix='/mathsym')
# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run( host="0.0.0.0",port=82, debug=True)
