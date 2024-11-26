import pytest
import sqlite3

@pytest.fixture(scope="session")
def db_conn():
    db = "university.db"
    connection = sqlite3.connect(db)
    try:
        yield connection.cursor()
    finally:
        connection.close()