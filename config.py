import datetime
import os

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with (SQLite)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
# For debugging SqlAlchemy queries
SQLALCHEMY_ECHO = True
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "csrf-secret"

# Secret key for signing cookies
SECRET_KEY = 'secret-key-goes-here'

# JWT
JWT_SECRET_KEY = 'secret-key-for-jwt-tokens-goes-here'
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)

# Bootstrap
BOOTSTRAP_BTN_STYLE = 'primary w-100 btn btn-lg btn-primary'
