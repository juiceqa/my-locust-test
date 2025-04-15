import time
import random
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
