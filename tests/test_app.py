import pytest
from app import create_app
from models import db, Bike

# @pytest.fixture
# def app():
#     app = create_app()
#     app.config.update({
#         "TESTING": True,
#         "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
#     })

#     with app.app_context():
#         db.drop_all()
#         db.create_all()
#         yield app
#         db.session.remove()
#         db.drop_all()

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Motorbike Maintenance Tracker" in response.data


def test_add_bike(client, app):
    response = client.post("/bikes/add", data={
        "make": "Honda",
        "model": "CBR650R",
        "year": "2021",
        "nickname": "Red One",
        "current_mileage": "12000"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Bike added successfully" in response.data

    with app.app_context():
        bike = Bike.query.first()
        assert bike is not None
        assert bike.make == "Honda"