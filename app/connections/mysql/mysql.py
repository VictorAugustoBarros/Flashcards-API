"""MySQL Database."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.utils.credencials import (
    mysql_database,
    mysql_host,
    mysql_password,
    mysql_port,
    mysql_user,
)

from app.entities.base_entity import mysql_base


class MySQLDB:
    """Classe para gerenciamento MySQL."""

    _instance = None
    session = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MySQLDB, cls).__new__(cls)
            cls._instance.init_db()
        return cls._instance

    def init_db(self):
        """Inicializa a conexão com o banco de dados."""
        engine = create_engine(
            f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
        )
        # mysql_base.metadata.drop_all(engine)
        mysql_base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)


if __name__ == "__main__":
    MySQLDB().init_db()
    print("OK")
