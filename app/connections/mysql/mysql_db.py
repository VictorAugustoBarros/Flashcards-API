"""MySQL Database."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.connections.mysql.mysql_base import Base
from app.utils.credencials import (
    mysql_database,
    mysql_host,
    mysql_password,
    mysql_port,
    mysql_user,
)


class MySQLDB:
    """Classe para gerenciamento MySQL."""

    def __init__(self):
        """Construtor da classe."""
        engine = create_engine(
            f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
        )

        # Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)
