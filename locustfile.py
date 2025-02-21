from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://xey.gbo.mybluehost.me/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
    }

    @task
    def load_main_page(self):
        self.client.get("https://xey.gbo.mybluehost.me/index.html", headers=self.headers, allow_redirects=False)

    @task
    def load_schedule_page(self):
        self.client.get("/budva-sveti-stefan-budva.html", headers=self.headers, allow_redirects=False)
