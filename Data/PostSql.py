import psycopg2


class Pagination:
    def __init__(self, host, dbname, user, password, port: int):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.port = port
        self._password = password
        self.conn: psycopg2 = ""
        self.cur = ""

    @classmethod
    def validate(cls):
        pass

    def connect(self):
        self.conn = psycopg2.connect(
            host=self.host,
            dbname=self.dbname,
            user=self.user,
            password=self._password,
            port=self.port)

        self.cur = self.conn.cursor()

        print("Database connected")

    def execute(self, *args: list[str]):
        self.cur.execute(*args)

    def select(self, *args: list[str]):
        self.cur.execute(*args)
        result = []
        for data in self.cur.fetchall():
            result.append(data)

        return result

    def commit(self):
        self.conn.commit()

    def __repr__(self):
        return f"Pagination({self.host}, {self.dbname}, {self.user}, {self._password}, {self.port})"

    def __del__(self):
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    database = Pagination(
        "localhost", "example",
        "postgres", "1423", 5432
    )

    database.connect()

    data = """CREATE TABLE IF NOT EXISTS person(
        person_id SERIAL PRIMARY KEY,
        fname VARCHAR(50) NOT NULL,
        age INT CHECK(age > 0),
        gender CHAR NOT NULL
    );"""

    database.execute(data)

    data = """INSERT INTO person(fname, age, gender) VALUES 
        ('Jameson', 18, 'm'),
        ('Daniel', 20, 'm'),
        ('Nameless', 21, 'f');"""

    database.execute(data)

    data = """SELECT * FROM person WHERE fname = %s;""", ['Nameless']

    print(*database.select(*data))

    database.execute("""DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
        """)