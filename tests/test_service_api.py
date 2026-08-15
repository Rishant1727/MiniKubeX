from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_service():

    response = client.post(
        "/services/register",
        json={
            "name": "test-service",
            "deployment_name": "test-deployment"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "registered"
    assert data["service"] == "test-service"


def test_add_service_instance():

    client.post(
        "/services/register",
        json={
            "name": "test-api"
        }
    )

    response = client.post(
        "/services/test-api/instances",
        json={
            "instance_id": "test-1",
            "host": "127.0.0.1",
            "port": 8001,
            "healthy": True
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "registered"
    assert data["service"] == "test-api"
    assert data["instance"] == "test-1"


def test_get_service():

    client.post(
        "/services/register",
        json={
            "name": "orders"
        }
    )

    response = client.get(
        "/services/orders"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "orders"


def test_get_missing_service():

    response = client.get(
        "/services/does-not-exist"
    )

    assert response.status_code == 404


def test_route_service():

    client.post(
        "/services/register",
        json={
            "name": "routing-test"
        }
    )

    client.post(
        "/services/routing-test/instances",
        json={
            "instance_id": "instance-1",
            "host": "127.0.0.1",
            "port": 8001,
            "healthy": True
        }
    )

    response = client.get(
        "/services/routing-test/route"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "routing-test"
    assert data["instance_id"] == "instance-1"


def test_route_service_without_healthy_instances():

    client.post(
        "/services/register",
        json={
            "name": "unhealthy-service"
        }
    )

    client.post(
        "/services/unhealthy-service/instances",
        json={
            "instance_id": "dead-1",
            "host": "127.0.0.1",
            "port": 8001,
            "healthy": False
        }
    )

    response = client.get(
        "/services/unhealthy-service/route"
    )

    assert response.status_code == 503