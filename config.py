import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = 'mysql+pymysql://{user}:{pw}@{host}:{port}/{db}?charset=utf8'.format(
    user=os.getenv('DB_USER'),
    pw=os.getenv('DB_PASS'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    db=os.getenv('DB_NAME')
)

SECRET_KEY = 'wlqdlsepwlqrkrhtlvek' # TODO 추후 변경
SQLALCHEMY_DATABASE_URI = DB_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False