# Create dummy secrey key so we can use sessions
SECRET_KEY = '********'

# Create in-memory database
DATABASE_FILE = 'sample_db.sqlite'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
SQLALCHEMY_ECHO = True

# Flask-Security config
#SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "********"
SECURITY_PASSWORD_SALT = "********"

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CONFIRMABLE = True

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = 'user@example'
MAIL_PASSWORD = '********'
MAIL_DEFAULT_SENDER = 'user@example'
SECURITY_EMAIL_SENDER = 'user@example'