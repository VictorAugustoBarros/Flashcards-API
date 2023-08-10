"""Credencials."""

import os

environment = os.getenv("ENVIRONMENT")

if environment == "LOCAL":
    from dotenv import load_dotenv

    load_dotenv()  # type: ignore

    mongo_host = os.getenv("MONGO_HOST_LOCAL")
    mongo_port = os.getenv("MONGO_PORT_LOCAL")
    mongo_database = os.getenv("MONGO_DATABASE_LOCAL")
    mongo_user = os.getenv("MONGO_USER_LOCAL")
    mongo_password = os.getenv("MONGO_PASSWORD_LOCAL")

else:
    mongo_host = os.getenv("MONGO_HOST_PROD")
    mongo_port = os.getenv("MONGO_PORT_PROD")
    mongo_database = os.getenv("MONGO_DATABASE_PROD")
    mongo_user = os.getenv("MONGO_USER_PROD")
    mongo_password = os.getenv("MONGO_PASSWORD_PROD")


if mongo_port and isinstance(mongo_port, str):  # type: ignore
    mongo_port = int(mongo_port)  # type: ignore
