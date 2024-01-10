from conftest import client


def test_register():
    response = client.post("/auth/register", json={
          "email": "trippyfren@gmail.com",
          "password": "string",
          "is_active": True,
          "is_superuser": False,
          "is_verified": False,
    })

    assert response.status_code == 201

