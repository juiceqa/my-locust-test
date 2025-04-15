from locust import HttpUser, task
import logging
import random

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SpikeUser(HttpUser):
    host = "https://jsonplaceholder.typicode.com"

    # Define the wait_time method to return 0 (no wait time)
    def wait_time(self):
        return 0  # No wait time, to simulate instant load

    @task
    def spike_load(self):
        with self.client.get("/posts", catch_response=True) as response:
            if response.status_code == 200:
                logger.info(f"Success {response.status_code} from {response.request.method} {response.url}")
                response.success()  # Mark as success in the report
            else:
                logger.error(f"Failure {response.status_code} from {response.request.method} {response.url}")
                response.failure(f"Unexpected status code {response.status_code}")  # Mark as failure in the report
