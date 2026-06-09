import pytest

from pomodoro import create_app
from pomodoro.models import db as _db


@pytest.fixture
def app():
    app = create_app("testing")

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
