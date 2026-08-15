class RollingUpdater:

    def __init__(
        self,
        max_unavailable: int = 1
    ):
        self.max_unavailable = max_unavailable

    def create_plan(
        self,
        replicas: int
    ):
        plan = []

        for replica in range(
            1,
            replicas + 1
        ):
            plan.append(
                {
                    "step": replica,
                    "action": "replace",
                    "replica": replica,
                    "max_unavailable": self.max_unavailable
                }
            )

        return plan