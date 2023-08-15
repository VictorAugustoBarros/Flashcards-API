from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.connections.mysql.mysql_base import Base
from app.utils.credencials import (mysql_database, mysql_host, mysql_password,
                                   mysql_port, mysql_user)


class MySQLDB:
    def __init__(self):
        engine = create_engine(
            f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
        )

        # Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)

    def execute_query(self, query, params=None):
        try:
            session = self.session()
            result = session.execute(query, params)
            session.commit()
            return result.fetchall()
        except Exception as e:
            print("Error:", e)
            return []

    def fetch_one(self, query, params=None):
        result = self.execute_query(query, params)
        if result:
            return result[0]
        return None

    def fetch_all(self, query, params=None):
        return self.execute_query(query, params)

    def insert(self, query, params=None):
        return self.execute_query(query, params)

    def update(self, query, params=None):
        return self.execute_query(query, params)

    def delete(self, query, params=None):
        return self.execute_query(query, params)
