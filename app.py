from dotenv import load_dotenv
from flask_bootstrap import Bootstrap

from config.constants import SecurityConstants
from config.db import init_db
from config.factory import AppFlask


if __name__ == "__main__":
    load_dotenv()
    init_db()
    app = AppFlask().instance
    Bootstrap(app)
    app.config['SECRET_KEY'] = SecurityConstants.APP_SECRET_KEY
    app.run(debug=True)
