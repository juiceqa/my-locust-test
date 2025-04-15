from locust import HttpUser, task, between


class APIUser(HttpUser):
    """
    Simulates a user interacting with the JSONPlaceholder test API.
    Each method simulates a specific kind of HTTP request.
    """
    host = "https://jsonplaceholder.typicode.com"
    wait_time = between(1, 5)

    @task
    def get_posts(self):
        """Simulates retrieving a list of all posts."""
        response = self.client.get("/posts")
        print(f"[GET] /posts => Status: {response.status_code}, {len(response.json())} posts retrieved")

    @task
    def get_users(self):
        """Simulates retrieving a list of all users."""
        response = self.client.get("/users")
        print(f"[GET] /users => Status: {response.status_code}, {len(response.json())} users retrieved")

    @task
    def update_post_put(self):
        """Simulates fully updating a post using PUT (replaces the entire object)."""
        payload = {
            "id": 1,
            "title": "Updated Title",
            "body": "Updated Body",
            "userId": 1
        }
        response = self.client.put("/posts/1", json=payload)
        print(f"[PUT] /posts/1 => Status: {response.status_code}, Title: {response.json().get('title')}")

    @task
    def update_post_patch(self):
        """Simulates partially updating a post using PATCH (modifies part of the object)."""
        response = self.client.patch("/posts/1", json={"title": "Partially Updated Title"})
        print(f"[PATCH] /posts/1 => Status: {response.status_code}, Title: {response.json().get('title')}")

    @task
    def delete_post(self):
        """Simulates deleting a post."""
        response = self.client.delete("/posts/1")
        print(f"[DELETE] /posts/1 => Status: {response.status_code}")

    @task
    def create_post(self):
        """Simulates creating a new post with dummy content."""
        payload = {
            "title": "Test",
            "body": "Test Body",
            "userId": 1
        }
        response = self.client.post("/posts", json=payload)
        print(f"[POST] /posts => Status: {response.status_code}, ID: {response.json().get('id')}")
