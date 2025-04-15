from locust import HttpUser, task
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SpikeUser(HttpUser):
    host = "https://jsonplaceholder.typicode.com"
    wait_time = 0  # No wait time, to simulate instant load

    @task
    def spike_load(self):
        with self.client.get("/posts", catch_response=True) as response:
            if response.status_code == 200:
                logger.info(f"Success {response.status_code} from {response.request.method} {response.url}")
                response.success()
            else:
                logger.error(f"Failure {response.status_code} from {response.request.method} {response.url}")
                response.failure(f"Unexpected status code {response.status_code}")
