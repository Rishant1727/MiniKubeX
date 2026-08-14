import time


class HealthLoop:

    def __init__(
        self,
        monitor,
        interval: int = 5
    ):

        self.monitor = monitor
        self.interval = interval
        self.running = False

    def start(self):

        self.running = True

        while self.running:

            self.monitor()

            time.sleep(
                self.interval
            )

    def stop(self):

        self.running = False