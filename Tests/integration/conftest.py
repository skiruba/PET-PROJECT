import pytest

from app import app
from models import db

@pytest.fixture(scope='module')
def test_app():
    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.test_client() as test_app:
        yield test_app
