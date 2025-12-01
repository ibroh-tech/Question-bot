import psycopg2
from config import POSTGRES_CONFIG


def get_connection():
    return psycopg2.connect(**POSTGRES_CONFIG)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS answers (
        id SERIAL PRIMARY KEY,
        user_id BIGINT,
        question_id INT,
        answer TEXT
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


def save_answer(user_id, question_id, answer):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO answers (user_id, question_id, answer) VALUES (%s, %s, %s)",
        (user_id, question_id, answer),
    )

    conn.commit()
    cur.close()
    conn.close()
