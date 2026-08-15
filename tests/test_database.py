from database.repository import DeploymentRepository


def test_deployment_persistence():

    repository = DeploymentRepository()

    test_name = "database-test"

    repository.delete(test_name)

    repository.create(
        name=test_name,
        image="nginx",
        replicas=2
    )

    result = repository.get(test_name)

    assert result is not None
    assert result.name == test_name
    assert result.image == "nginx"
    assert result.replicas == 2

    repository.delete(test_name)