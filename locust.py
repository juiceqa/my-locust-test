from locust import HttpUser, task, between


class APIUser(HttpUser):
    host = "https://jsonplaceholder.typicode.com"
    wait_time = between(1, 5)

    @task
    def get_posts(self):
        self.client.get("/posts")

    @task
    def get_users(self):
        self.client.get("/users")

    @task
    def update_post_put(self):
        self.client.put("/posts/1", json={
            "id": 1,
            "title": "Updated Title",
            "body": "Updated Body",
            "userId": 1
        })

    @task
    def update_post_patch(self):
        self.client.patch("/posts/1", json={
            "title": "Partially Updated Title"
        })

    @task
    def delete_post(self):
        self.client.delete("/posts/1")

    @task
    def create_post(self):
        self.client.post("/posts", json={
            "title": "Test",
            "body": "Test Body",
            "userId": 1
        })
