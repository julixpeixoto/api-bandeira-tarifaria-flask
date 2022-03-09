import os

debug_mode = os.environ.get("DEBUG", False)
url_source = os.environ.get("URL_SOURCE")
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_database = os.environ.get("DB_DATABASE")
db_port = os.environ.get("DB_PORT")
