from PaymentApplication import app
import pytest


@pytest.fixture(scope='module')
def test_client():
    flask_app = app

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


def test_login_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    print(response.data)
    assert b"Log In"  in response.data
   
    


def test_home_page_post_with_fixture(test_client):
    """
    GIVEN a Flask application
    WHEN the '/home' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post('/home')
    assert response.status_code == 405
    assert b"View Payment History" not in response.data