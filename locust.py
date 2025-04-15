from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 5)  # Simulate wait time between requests

    @task
    def get_posts(self):
        self.client.get("/posts")

    @task
    def get_users(self):
        self.client.get("/users")

    @task
    def create_post(self):
        self.client.post("/posts", json={"title": "Test", "body": "Test Body", "userId": 1})
