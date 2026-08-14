from controller.models.deployment import Deployment


class Reconciler:

    def calculate_difference(
        self,
        desired_replicas: int,
        actual_replicas: int
    ) -> int:

        return desired_replicas - actual_replicas

    def reconcile(
        self,
        deployment: Deployment,
        actual_replicas: int
    ):

        difference = self.calculate_difference(
            deployment.replicas,
            actual_replicas
        )

        if difference > 0:

            return {
                "action": "create",
                "count": difference
            }

        if difference < 0:

            return {
                "action": "remove",
                "count": abs(difference)
            }

        return {
            "action": "none",
            "count": 0
        }