"""Credencials."""

import os

environment = os.getenv("ENVIRONMENT", "LOCAL")

if environment == "LOCAL":
    from dotenv import load_dotenv

    load_dotenv()  # type: ignore

    mongo_host = os.getenv("MONGO_HOST_LOCAL")
    mongo_port = os.getenv("MONGO_PORT_LOCAL")
    mongo_database = os.getenv("MONGO_DATABASE_LOCAL")
    mongo_user = os.getenv("MONGO_USER_LOCAL")
    mongo_password = os.getenv("MONGO_PASSWORD_LOCAL")

    mysql_host = os.getenv("MYSQL_HOST_LOCAL")
    mysql_port = os.getenv("MYSQL_PORT_LOCAL")
    mysql_database = os.getenv("MYSQL_DATABASE_LOCAL")
    mysql_user = os.getenv("MYSQL_USER_LOCAL")
    mysql_password = os.getenv("MYSQL_PASSWORD_LOCAL")

else:
    mysql_host = os.getenv("MYSQL_HOST_PROD")
    mysql_port = os.getenv("MYSQL_PORT_PROD")
    mysql_database = os.getenv("MYSQL_DATABASE_PROD")
    mysql_user = os.getenv("MYSQL_USER_PROD")
    mysql_password = os.getenv("MYSQL_PASSWORD_PROD")

    mongo_host = os.getenv("MONGO_HOST_PROD")
    mongo_port = os.getenv("MONGO_PORT_PROD")
    mongo_database = os.getenv("MONGO_DATABASE_PROD")
    mongo_user = os.getenv("MONGO_USER_PROD")
    mongo_password = os.getenv("MONGO_PASSWORD_PROD")

if mongo_port and isinstance(mongo_port, str):  # type: ignore
    mongo_port = int(mongo_port)  # type: ignore

if mysql_port and isinstance(mysql_port, str):  # type: ignore
    mysql_port = int(mysql_port)  # type: ignore

jwt_secret_key = os.getenv("JWT_SECRET_KEY")
