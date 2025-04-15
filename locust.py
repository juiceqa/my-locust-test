import time
import random
import logging
from locust import HttpUser, task, between


# Configure logger for stdout visibility in GitHub Actions
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FailureUser(HttpUser):
    """
    Simulates both normal and failure scenarios for load testing.
    """
    host = "https://jsonplaceholder.typicode.com"
    wait_time = between(1, 5)
    failure_weight = 1

    def _log_and_check(self, response, expect_failure=False):
        # Check for successful responses or expected failures
        if expect_failure:
            if response.status_code < 400:
                logger.warning(f"Expected failure, got {response.status_code} from {response.request.method} {response.url}")
                response.failure(f"Expected client/server error, got {response.status_code}")
                raise Exception(f"Expected failure, got {response.status_code}")
            else:
                logger.info(f"Expected failure confirmed: {response.status_code} from {response.request.method} {response.url}")
                response.success()
        else:
            if response.status_code >= 400:
                logger.error(f"Unexpected error {response.status_code} from {response.request.method} {response.url}")
                response.failure(f"Unexpected status code {response.status_code}")
                raise Exception(f"Unexpected status code {response.status_code}")
            else:
                logger.info(f"Success {response.status_code} from {response.request.method} {response.url}")
                response.success()

    @task
    def get_posts(self):
        with self.client.get("/posts", catch_response=True) as r:
            self._log_and_check(r)

    @task
    def get_users(self):
        with self.client.get("/users", catch_response=True) as r:
            self._log_and_check(r)

    @task
    def create_post(self):
        with self.client.post("/posts", json={"title": "Test", "body": "Test Body", "userId": 1}, catch_response=True) as r:
            self._log_and_check(r)

    @task(failure_weight)
    def invalid_endpoint(self):
        # Request a deliberately invalid endpoint that triggers a 404 error
        with self.client.get("/invalid-endpoint", catch_response=True) as r:
            self._log_and_check(r, expect_failure=True)

    @task(failure_weight)
    def create_post_with_invalid_data(self):
        with self.client.post("/posts", json={"invalidField": "value"}, catch_response=True) as r:
            self._log_and_check(r)

    @task(failure_weight)
    def delayed_request(self):
        time.sleep(5)
        with self.client.get("/posts", catch_response=True) as r:
            self._log_and_check(r)

    @task(failure_weight)
    def patch_post(self):
        with self.client.patch("/posts/1", json={"title": "Patched Title"}, catch_response=True) as r:
            self._log_and_check(r)

    @task(failure_weight)
    def put_post(self):
        with self.client.put("/posts/1", json={"id": 1, "title": "Updated Title", "body": "Updated Body", "userId": 1}, catch_response=True) as r:
            self._log_and_check(r)

    @task(failure_weight)
    def delete_post(self):
        with self.client.delete("/posts/1", catch_response=True) as r:
            self._log_and_check(r)


class NormalUser(FailureUser):
    """
    Simulates normal API usage more frequently than failures
    """

    @task(10)
    def get_posts(self):
        with self.client.get("/posts", catch_response=True) as r:
            self._log_and_check(r)

    @task(10)
    def get_users(self):
        with self.client.get("/users", catch_response=True) as r:
            self._log_and_check(r)

    @task(10)
    def create_post(self):
        with self.client.post("/posts", json={"title": "Test", "body": "Test Body", "userId": 1}, catch_response=True) as r:
            self._log_and_check(r)

    @task(5)
    def put_post(self):
        with self.client.put("/posts/1", json={"id": 1, "title": "Updated Title", "body": "Updated Body", "userId": 1}, catch_response=True) as r:
            self._log_and_check(r)

    @task(3)
    def patch_post(self):
        with self.client.patch("/posts/1", json={"title": "Patched Title"}, catch_response=True) as r:
            self._log_and_check(r)

    @task(3)
    def delete_post(self):
        with self.client.delete("/posts/1", catch_response=True) as r:
            self._log_and_check(r)
