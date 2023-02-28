from PaymentApplication.models import User
import pytest

@pytest.fixture(scope='module')
def new_user():
    user = User(id=1,username='Kavya', email='kavya@gmail.com',rollnumber='1602-19-733-075',branch='CSE',password='testing')
    return user


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    assert new_user.email == 'kavya@gmail.com'
    assert new_user.password == 'testing'
    assert new_user.branch== 'CSE'
