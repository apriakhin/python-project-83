from psycopg.errors import UniqueViolation
from psycopg.rows import dict_row


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM urls")
            return cur.fetchall()

    def find(self, id):
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            return cur.fetchone()

    def create(self, url_data):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO urls (name) VALUES (%s) RETURNING id",
                    (url_data["name"],),
                )
                url_data["id"] = cur.fetchone()[0]

            self.conn.commit()
            return url_data["id"]

        except UniqueViolation:
            self.conn.rollback()
            raise ValueError('Страница уже существует')
