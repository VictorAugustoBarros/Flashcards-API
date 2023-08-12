import pymysql


class MySQLDB:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                return cursor.fetchall()
        except Exception as e:
            print("Error:", e)
            self.connection.rollback()
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
