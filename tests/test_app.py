import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from testcontainers.postgres import PostgresContainer

postgres = PostgresContainer("postgres:16-alpine")


@pytest.fixture(scope="session")
def postgres_container():
    postgres = PostgresContainer("postgres:16.0")
    postgres.start()
    os.environ["DB_HOST"] = postgres.get_container_host_ip()
    os.environ["DB_PORT"] = str(postgres.get_exposed_port(5432))
    os.environ["DB_USERNAME"] = postgres.username
    os.environ["DB_PASSWORD"] = postgres.password
    os.environ["DB_NAME"] = postgres.dbname
    yield postgres
    postgres.stop()

@pytest.fixture
def client(postgres_container):
    from app import  app
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_non_existent_route(client):
    response = client.get('/non-existent')
    assert response.status_code == 404