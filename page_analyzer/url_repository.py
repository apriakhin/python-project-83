from psycopg.errors import UniqueViolation
from psycopg.rows import dict_row


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_urls(self):
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT
                    urls.id,
                    urls.name,
                    checks.created_at AS last_check,
                    checks.status_code
                FROM urls
                LEFT JOIN LATERAL (
                    SELECT
                        created_at,
                        status_code
                    FROM url_checks
                    WHERE url_checks.url_id = urls.id
                    ORDER BY created_at DESC
                    LIMIT 1
                ) AS checks ON TRUE
                ORDER BY urls.id DESC;
            """)
            return cur.fetchall()

    def find_url(self, id):
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            return cur.fetchone()

    def find_checks(self, url_id):
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM url_checks WHERE url_id = %s", (url_id,))
            return cur.fetchall()

    def create_url(self, url_data):
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

    def create_check(self, check_data):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO url_checks (
                            url_id, 
                            status_code, 
                            h1, 
                            title, 
                            description
                        ) 
                        VALUES (%s, %s, %s, %s, %s) 
                        RETURNING id
                    """,
                    (check_data["url_id"], 
                     check_data["status_code"],
                     check_data["h1"], 
                     check_data["title"], 
                     check_data["description"]),
                )
                check_data["id"] = cur.fetchone()[0]

            self.conn.commit()
            return check_data["id"]
        
        except Exception as error:
            print(error)
            self.conn.rollback()
            raise ValueError('Произошла ошибка при проверке')
