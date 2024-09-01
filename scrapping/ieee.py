
import requests
import time
import random
from datetime import datetime, timedelta

from .. import paper_manager as pm

class IEEEScraper:
    def __init__(self, api_key, max_records_per_call=100):
        self.api_key = api_key
        self.base_url = "https://ieeexploreapi.ieee.org/api/v1/search/articles"
        self.max_records_per_call = max_records_per_call # TODO decide this or how to determine this
        self.sleep_time = 0.1  # 10 calls per second, 200 calls per day - so just run it 200 times at the start tbh, and then just scrape for the rest of it?
        self.max_calls = 200
        self.last_request_time = datetime.now() - timedelta(seconds=sleep_time)
        self.start_record_log = []

    def _get_start_record(self)->int:
        """ Gets a start number to index from, and ensures to avoid duplicates - although I doubt this will be a problem"""
        # get random start number
        new_start = random.randint(0,1000) # TODO get the upper of this
        # check if this has any overlap
        for prev_start in self.start_record_log:
            if abs(new_start - prev_start) <= self.max_records_per_call:
                new_Start = prev_start + (random.choice([-1,1]) * self.max_records_per_call)  # either goes the maximum records bellow or above
                print('Collision in start value detected. Adjusted for.') # I put this just so I can see if there is too many collisions - which would suggest something wrong with how I am sampling (most likely tahe new_start random.randint's upper value is too low, not taking in all the papers


    def get_papers(self, api_key):
        """Generator function that yields one paper at a time."""
        max_calls = 200
        time_spacing = 0.1
        t1 = time.time()

        while max_calls > 0:
            max_calls -= 1
            params = {
                "apikey": api_key,
                "content_type": "Journals",
                "start_record": _get_start_record(),
                "max_records": self.max_records_per_call
            }

            # Dynamic sleep
            t2 = time.time()
            if t2 - t1 < time_spacing:
                time.sleep(0.1 - t2 + t1)

            response = requests.get(self.base_url, params=params)

            t1 = time.time()

            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
                break

            data = response.json()
            articles = data.get('articles', [])

            if articles:
                for article in articles:
                    yield {
                        "title": article.get("title"),
                        "authors": ', '.join([author.get("name") for author in article.get("authors", [])])
                        "publication_year": article.get("publication_year"),
                        "journal_title": article.get("publication_title"),
                        "doi": article.get("doi"),
                        "summary": article.get("abstract")
                    }

# Example usage:
api_key = "your_api_key_here"
scraper = IEEEScraper(api_key)

with pm.db() as db:
    for paper in scraper.get_papers(max_iterations=1):
        db.insert(paper, input_format='dict'),
        



