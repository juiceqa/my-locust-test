from locust import HttpUser, task, between


class APIUser(HttpUser):
    # Set the base URL for all requests
    host = "https://jsonplaceholder.typicode.com"

    wait_time = between(1, 5)  # Simulate wait time between requests

    @task
    def get_posts(self):
        self.client.get("/posts")  # This will now resolve to https://jsonplaceholder.typicode.com/posts

    @task
    def get_users(self):
        self.client.get("/users")  # This will now resolve to https://jsonplaceholder.typicode.com/users

    @task
    def create_post(self):
        # This will now resolve to https://jsonplaceholder.typicode.com/posts
        self.client.post("/posts", json={"title": "Test", "body": "Test Body", "userId": 1})
