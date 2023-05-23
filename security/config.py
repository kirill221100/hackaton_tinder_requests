import os
from dotenv import load_dotenv

load_dotenv('./.env')


class Config:
    PSQL_URL = os.environ.get('PSQL_URL')
