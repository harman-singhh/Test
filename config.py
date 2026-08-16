import os

class Config:
    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "codecraft-academy-secret-key-change-me")

    # MySQL / PyMySQL connection settings
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DB = os.environ.get("MYSQL_DB", "codecraft_academy_db")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))

    # File upload settings
    UPLOAD_FOLDER = os.path.join("static", "images")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
