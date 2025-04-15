import time
from locust import HttpUser, task, between


class FailureUser(HttpUser):
    """
    A Locust user class that simulates both normal and failure scenarios for load testing.

    This class defines tasks that simulate standard API requests (such as fetching posts
    or users) as well as various types of failures (e.g., invalid endpoints, delayed requests,
    and simulated server errors). The goal is to test how the system handles normal traffic
    alongside error conditions, such as timeouts or bad requests.

    Attributes:
        host (str): The base URL of the API to be tested.
        wait_time (between): The simulated wait time between each request for this user.
        failure_weight (int): The weight determining how often failure tasks should run.
                              Lower values mean the failure tasks are less frequent than
                              regular tasks.
    Usage:
        This class is intended for load testing scenarios where both normal and failure
        conditions need to be simulated simultaneously.
    """
    host = "https://jsonplaceholder.typicode.com"
    wait_time = between(1, 5)
    failure_weight = 1

    @task
    def get_posts(self):
        """ Fetch posts from /posts endpoint """
        print("GET /posts")
        self.client.get("/posts")

    @task
    def get_users(self):
        """ Fetch users from /users endpoint """
        print("GET /users")
        self.client.get("/users")

    @task
    def create_post(self):
        """ Create a new post with valid data """
        print("POST /posts with valid data")
        self.client.post("/posts", json={"title": "Test", "body": "Test Body", "userId": 1})

    @task
    def update_post(self):
        """ Update a post using PUT """
        print("PUT /posts/1 with updated data")
        self.client.put("/posts/1", json={"id": 1, "title": "Updated", "body": "Updated Body", "userId": 1})

    @task
    def patch_post(self):
        """ Partially update a post using PATCH """
        print("PATCH /posts/1 with partial data")
        self.client.patch("/posts/1", json={"title": "Partially Updated"})

    @task
    def delete_post(self):
        """ Delete a post using DELETE """
        print("DELETE /posts/1")
        self.client.delete("/posts/1")

    @task(failure_weight)
    def invalid_endpoint(self):
        """ Simulate 404 error by accessing an invalid endpoint """
        print("GET /invalid-endpoint (expecting 404)")
        with self.client.get("/invalid-endpoint", catch_response=True) as response:
            if response.status_code != 404:
                response.failure("Expected 404 Not Found")

    @task(failure_weight)
    def create_post_with_invalid_data(self):
        """ Simulate 400/500 error by sending malformed data """
        print("POST /posts with invalid data (expecting 4xx/5xx)")
        with self.client.post("/posts", json={"invalidField": "value"}, catch_response=True) as response:
            if response.status_code < 400:
                response.failure(f"Expected client/server error, got {response.status_code}")

    @task(failure_weight)
    def delayed_request(self):
        """ Simulate a delay (timeout) by sleeping before sending a request """
        print("Sleeping 5 seconds before GET /posts")
        time.sleep(5)
        self.client.get("/posts")

    @task(failure_weight)
    def simulated_exception(self):
        """ Simulate an application-level exception within request context """
        print("GET /posts followed by simulated exception")
        with self.client.get("/posts", catch_response=True) as response:
            try:
                raise Exception("Simulated failure for testing purposes")
            except Exception as e:
                response.failure(str(e))


class NormalUser(FailureUser):
    """ Normal tasks that run continuously """

    @task(10)
    def get_posts(self):
        """ Fetch posts from /posts endpoint """
        print("GET /posts (NormalUser, weight=10)")
        self.client.get("/posts")

    @task(10)
    def get_users(self):
        """ Fetch users from /users endpoint """
        print("GET /users (NormalUser, weight=10)")
        self.client.get("/users")

    @task(10)
    def create_post(self):
        """ Create a new post with valid data """
        print("POST /posts (NormalUser, weight=10)")
        self.client.post("/posts", json={"title": "Test", "body": "Test Body", "userId": 1})

    @task(5)
    def update_post(self):
        """ Update a post using PUT """
        print("PUT /posts/1 (NormalUser)")
        self.client.put("/posts/1", json={"id": 1, "title": "Updated", "body": "Updated Body", "userId": 1})

    @task(5)
    def patch_post(self):
        """ Partially update a post using PATCH """
        print("PATCH /posts/1 (NormalUser)")
        self.client.patch("/posts/1", json={"title": "Partially Updated"})

    @task(5)
    def delete_post(self):
        """ Delete a post using DELETE """
        print("DELETE /posts/1 (NormalUser)")
        self.client.delete("/posts/1")
