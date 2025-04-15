from locust import HttpUser, task, between
import time
import random

class FailureUser(HttpUser):
    # Set the base URL for all requests
    host = "https://jsonplaceholder.typicode.com"

    wait_time = between(1, 5)  # Simulate wait time between requests

    # Control the number of failure tasks
    failure_weight = 1  # Set a lower weight to run failures less frequently

    @task
    def get_posts(self):
        """ Fetch posts from /posts endpoint """
        self.client.get("/posts")

    @task
    def get_users(self):
        """ Fetch users from /users endpoint """
        self.client.get("/users")

    @task
    def create_post(self):
        """ Create a new post with valid data """
        self.client.post("/posts", json={"title": "Test", "body": "Test Body", "userId": 1})

    # Failure simulation tasks (set to run only a few times)
    @task(failure_weight)
    def invalid_endpoint(self):
        """ Simulate 404 error by accessing an invalid endpoint """
        self.client.get("/invalid-endpoint")  # This will return 404 error

    @task(failure_weight)
    def create_post_with_invalid_data(self):
        """ Simulate 400/500 error by sending malformed data """
        self.client.post("/posts", json={"invalidField": "value"})  # Likely to return 400 or 500 error

    @task(failure_weight)
    def delayed_request(self):
        """ Simulate a delay (timeout) by sleeping before sending a request """
        time.sleep(5)  # Simulating a delay of 5 seconds
        self.client.get("/posts")

    @task(failure_weight)
    def random_failure(self):
        """ Simulate a random failure """
        if random.choice([True, False]):  # Randomly simulate a failure
            self.client.get("/posts")
        else:
            raise Exception("Simulated failure for testing purposes")  # Raise an exception to simulate failure

class NormalUser(FailureUser):
    """ Normal tasks that run continuously """

    # Increase the weight of normal tasks to ensure they run throughout the entire test
    @task(10)  # These tasks will run 10 times more frequently than failure tasks
    def get_posts(self):
        """ Fetch posts from /posts endpoint """
        self.client.get("/posts")

    @task(10)
    def get_users(self):
        """ Fetch users from /users endpoint """
        self.client.get("/users")

    @task(10)
    def create_post(self):
        """ Create a new post with valid data """
        self.client.post("/posts", json={"title": "Test", "body": "Test Body", "userId": 1})
