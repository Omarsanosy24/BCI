from faker import Faker
from authentication.models import User
fake = Faker()
email = fake.email()


def test_create_user(client, db):
    rp = client.post(
        '/auth/register/',
        format="json",
        data={
            "email": "email@gmail.com",
            "first_name": fake.first_name(),
            "password": "123456789",
            "last_name": fake.last_name(),
        }
    )
    print(rp.data)
    assert rp.status_code == 200, rp.data
    assert "password" not in rp.data
    assert "status" in rp.data and "message" in rp.data


def test_login(client, db):
    test_create_user(client, db)
    rp = client.post(
        '/auth/login/',
        format="json",
        data={
            "email": "email@gmail.com",
            "password": "123456789",
        }
    )
    assert rp.status_code == 200, rp.data
    assert "password" not in str(rp.data)
    assert "status" in rp.data and "message" in rp.data
    assert "token" in rp.data['data']
    # for Email Error
    rp_ = client.post(
        '/auth/login/',
        format="json",
        data={
            "email": "emaisl@gmail.com",
            "password": "123456789",
        }
    )
    assert rp_.status_code == 400, rp_.data
    assert "password" not in str(rp_.data)
    assert "status" in rp_.data and "message" in rp_.data
    # For password error
    rp2 = client.post(
        '/auth/login/',
        format="json",
        data={
            "email": "email@gmail.com",
            "password": "1234567829",
        }
    )
    assert rp2.status_code == 400, rp2.data
    assert "status" in rp2.data and "message" in rp2.data


def test_user_info(client, db):
    test_create_user(client, db)
    user = User.objects.first()
    access_token = user.get_tokens_for_user()['access']
    rp = client.get(
        '/auth/profile/',
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )
    assert rp.status_code == 200, rp.data
    assert "status" in rp.data and "message" in rp.data
    assert "first_name" in rp.data['data']
    assert "last_name" in rp.data['data']
    assert "email" in rp.data['data']

