from controller.state import ClusterState


def test_cluster_state_tracks_containers():

    state = ClusterState()

    state.add_container(
        "payment-api",
        "container-1"
    )

    state.add_container(
        "payment-api",
        "container-2"
    )

    assert state.get_replica_count(
        "payment-api"
    ) == 2


def test_cluster_state_removes_container():

    state = ClusterState()

    state.add_container(
        "payment-api",
        "container-1"
    )

    state.remove_container(
        "payment-api",
        "container-1"
    )

    assert state.get_replica_count(
        "payment-api"
    ) == 0