import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('HOST')
port = 3306
user = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')

connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database)