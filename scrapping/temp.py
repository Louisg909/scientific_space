
import requests
import numpy as np
import random
import time


# =================== PHYSICAL REVIEW JOURNAL (APS) ==================== #

def aps_fetch_papers(start, max_results, year):
    base_url = 'https://api.aps.org/v1/articles?'  # Placeholder API URL
    query = f'year={year}&start={start}&limit={max_results}'
    response = requests.get(base_url + query)
    return response.json()

def aps_parse_response(response):
    for article in response['data']:
        title = article.get('title', 'No title')
        abstract = article.get('abstract', 'No abstract')
        authors = [author['name'] for author in article.get('authors', [])]
        year = article.get('year', 'No year')
        yield { 'id': article['id'], 'title': title, 'summary': abstract, 'year': year, 'authors': authors, 'citation_ids': None }

def aps_get_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10)
    for _ in range(total_papers // batch_size):
        start = random.randint(0, 10000)
        response = aps_fetch_papers(start, batch_size, year)
        for paper in aps_parse_response(response):
            yield paper

def aps_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def aps(max_results):
    years = aps_sample_years(num_samples=max_results)
    for year, count in years.items():
        for paper in aps_get_random_papers(year, total_papers=count):
            yield paper


# ======================= NATURE COMMUNICATIONS ======================== #

def natcomms_fetch_papers(start, max_results, year):
    base_url = 'https://api.nature.com/v1/articles?'  # Placeholder API URL
    query = f'year={year}&start={start}&limit={max_results}'
    response = requests.get(base_url + query)
    return response.json()

def natcomms_parse_response(response):
    for article in response['data']:
        title = article.get('title', 'No title')
        abstract = article.get('abstract', 'No abstract')
        authors = [author['name'] for author in article.get('authors', [])]
        year = article.get('year', 'No year')
        yield { 'id': article['id'], 'title': title, 'summary': abstract, 'year': year, 'authors': authors, 'citation_ids': None }

def natcomms_get_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10)
    for _ in range(total_papers // batch_size):
        start = random.randint(0, 10000)
        response = natcomms_fetch_papers(start, batch_size, year)
        for paper in natcomms_parse_response(response):
            yield paper

def natcomms_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def natcomms(max_results):
    years = natcomms_sample_years(num_samples=max_results)
    for year, count in years.items():
        for paper in natcomms_get_random_papers(year, total_papers=count):
            yield paper


# =============================== NATURE ================================ #

def nature_fetch_papers(start, max_results, year):
    base_url = 'https://api.nature.com/v1/articles?'  # Placeholder API URL
    query = f'year={year}&start={start}&limit={max_results}'
    response = requests.get(base_url + query)
    return response.json()

def nature_parse_response(response):
    for article in response['data']:
        title = article.get('title', 'No title')
        abstract = article.get('abstract', 'No abstract')
        authors = [author['name'] for author in article.get('authors', [])]
        year = article.get('year', 'No year')
        yield { 'id': article['id'], 'title': title, 'summary': abstract, 'year': year, 'authors': authors, 'citation_ids': None }

def nature_get_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10)
    for _ in range(total_papers // batch_size):
        start = random.randint(0, 10000)
        response = nature_fetch_papers(start, batch_size, year)
        for paper in nature_parse_response(response):
            yield paper

def nature_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def nature(max_results):
    years = nature_sample_years(num_samples=max_results)
    for year, count in years.items():
        for paper in nature_get_random_papers(year, total_papers=count):
            yield paper

# ================= GEOPHYSICAL RESEARCH LETTERS (GRL) ================== #

def grl_fetch_papers(start, max_results, year):
    base_url = 'https://api.agu.org/v1/articles?'  # Placeholder API URL
    query = f'year={year}&start={start}&limit={max_results}'
    response = requests.get(base_url + query)
    return response.json()

def grl_parse_response(response):
    for article in response['data']:
        title = article.get('title', 'No title')
        abstract = article.get('abstract', 'No abstract')
        authors = [author['name'] for author in article.get('authors', [])]
        year = article.get('year', 'No year')
        yield { 'id': article['id'], 'title': title, 'summary': abstract, 'year': year, 'authors': authors, 'citation_ids': None }

def grl_get_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10)
    for _ in range(total_papers // batch_size):
        start = random.randint(0, 10000)
        response = grl_fetch_papers(start, batch_size, year)
        for paper in grl_parse_response(response):
            yield paper

def grl_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def grl(max_results):
    years = grl_sample_years(num_samples=max_results)
    for year, count in years.items():
        for paper in grl_get_random_papers(year, total_papers=count):
            yield paper

# ========== JOURNAL OF THE AMERICAN CHEMICAL SOCIETY (JACS) =========== #

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Update this path to the location of your chromedriver
CHROME_DRIVER_PATH = r'.\chromedriver.exe'

def jacs_fetch_papers(page, batch_size, year):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("enable-automation")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--disable-gpu")

    url = f'https://pubs.acs.org/toc/jacsat/{year}/{page}'
    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=chrome_options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
        """
    })
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.issue-item"))
        )

        articles = driver.find_elements(By.CSS_SELECTOR, "div.issue-item")
        papers = []
        for article in articles:
            title = article.find_element(By.CSS_SELECTOR, "h5.issue-item_title").text
            link = article.find_element(By.CSS_SELECTOR, "h5.issue-item_title a").get_attribute('href')
            doi = link.split('/')[-1] if link else 'No DOI'
            summary = article.find_element(By.CSS_SELECTOR, "div.issue-item_description").text
            authors = article.find_element(By.CSS_SELECTOR, "ul.issue-item_authors").text.split(", ")
            papers.append({
                'id': doi,
                'title': title,
                'summary': summary,
                'year': year,
                'authors': authors,
                'citation_ids': None
            })

        driver.quit()
        return papers

    except Exception as e:
        print(f"Error fetching papers: {e}")
        driver.quit()
        return []

def jacs_get_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10)
    papers = []
    for _ in range(total_papers // batch_size):
        page = random.randint(1, 100)  # Adjust range as necessary
        papers.extend(jacs_fetch_papers(page, batch_size, year))
        time.sleep(random.uniform(1, 3))  # To avoid getting blocked
    return papers

def jacs_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def jacs(max_results):
    years = jacs_sample_years(num_samples=max_results)
    for year, count in years.items():
        papers = jacs_get_random_papers(year, total_papers=count)
        for paper in papers:
            yield paper

if __name__ == '__main__':
    for n in jacs(12):
        print(n)








