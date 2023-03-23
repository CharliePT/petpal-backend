import pytest
import psycopg2
import os
import urllib.parse as up
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()

url = up.urlparse(os.environ["DATABASE_URL"])
up.uses_netloc.append("postgres")

con = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

