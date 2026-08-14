class RecoveryManager:

    def needs_recovery(
        self,
        desired_replicas: int,
        healthy_replicas: int
    ) -> bool:

        return healthy_replicas < desired_replicas

    def calculate_missing_replicas(
        self,
        desired_replicas: int,
        healthy_replicas: int
    ) -> int:

        difference = (
            desired_replicas -
            healthy_replicas
        )

        return max(difference, 0)