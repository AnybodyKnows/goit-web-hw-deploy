from unittest.mock import Mock, patch

import pytest

from src.services.auth import auth_service

test_contact = {"full_name": "TestTest", "email": "TestTest@gmail.com",
                "phone_number": "1236547890", "birthday": "2024-08-17"}


def test_get_contacts(client, get_token):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 0


def test_create_contact(client, get_token):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("api/contacts", headers=headers, json=test_contact)
        assert response.status_code == 201, response.text
        data = response.json()
        assert len(data) > 0
        assert data["full_name"] == test_contact["full_name"]
        assert data["email"] == test_contact["email"]
        assert "id" in data



