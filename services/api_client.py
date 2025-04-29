import requests
import time
from functools import wraps
from config.settings import Config

class APIClient:
    def __init__(self):
        self.last_request = 0
        self.rate_limit = 1  # Seconds between requests

    def rate_limited(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            elapsed = time.time() - self.last_request
            if elapsed < self.rate_limit:
                time.sleep(self.rate_limit - elapsed)
            result = func(self, *args, **kwargs)
            self.last_request = time.time()
            return result
        return wrapper

    @rate_limited
    def fetch_cve(self, last_hours=24):
        url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
        params = {
            "resultsPerPage": 50,
            "pubStartDate": f"NOW-{last_hours}HOURS",
            "pubEndDate": "NOW"
        }
        headers = {"apiKey": Config.API_KEYS["cve"]}
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"CVE API Error: {str(e)}")
            return None

    @rate_limited
    def fetch_github_security(self):
        url = "https://api.github.com/search/repositories"
        params = {
            "q": "topic:cybersecurity",
            "sort": "updated",
            "order": "desc"
        }
        headers = {
            "Authorization": f"token {Config.API_KEYS['github']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"GitHub API Error: {str(e)}")
            return None
