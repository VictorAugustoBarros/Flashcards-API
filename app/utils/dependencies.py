"""Dependency Injection."""
from dataclasses import dataclass

from app.connections.mongo.mongo_db import MongoDB
from app.connections.mysql.mysql_db import MySQLDB


@dataclass
class Dependencies:
    # database: MongoDB = MongoDB()
    database: MySQLDB = MySQLDB()
