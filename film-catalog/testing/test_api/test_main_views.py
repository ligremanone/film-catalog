from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_view() -> None:
    # TODO: fake data
    name = "John"
    query = {"name": name}
    response = client.get(
        "/",
        params=query,
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    expected_message = f"Hello {name}! Welcome to film catalog!"
    assert response_data["message"] == expected_message, response_data
