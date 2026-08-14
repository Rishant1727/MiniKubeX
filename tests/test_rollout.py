from deployment.rollout import (
    RollingUpdater
)


def test_rolling_update_plan():

    updater = RollingUpdater()

    plan = updater.create_plan(
        replicas=3
    )

    assert len(plan) == 3

    assert plan[0]["replica"] == 1
    assert plan[1]["replica"] == 2
    assert plan[2]["replica"] == 3