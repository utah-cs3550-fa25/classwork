from locust import HttpUser, task, between

class SimpleLoadTest(HttpUser):
    # you can also omit this and pass --host on the command line
    wait_time = between(0.1, 0.5)  # adjust pause between requests

    @task
    def hit_root(self):
        self.client.get("/")
