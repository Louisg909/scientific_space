
import requests
import xml.etree.ElementTree as ET
import numpy as np
import random


def get_all(max_results):
    max(5, max_results)
    max_results = max(8, max_results) # 8 is the amount needed to get the distribution
    numb = {'jbc': max_results // 3,
                  'cell': max_results // 2.25,
                  'jeb': max_results // 4.5}

    for paper in jbc(numb['jbc']):
        yield paper
    for paper in cell(numb['cell']):
        yield paper
    for paper in jeb(numb['jeb']):
        yield paper



# =============== JOURNAL OF BIOLOGICAL CHEMISTRY (JBC) ================ #
# ================================= 3% ================================== #

def jbc_fetch_papers(start, max_results, year):
    base_url = 'https://api.jbc.org/articles?'
    query = f'year={year}&start={start}&limit={max_results}'
    response = requests.get(base_url + query)
    return response.json()

def jbc_parse_response(response):
    for article in response['data']:
        title = article.get('title', 'No title')
        abstract = article.get('abstract', 'No abstract')
        authors = [author['name'] for author in article.get('authors', [])]
        year = article.get('year', 'No year')
        yield { 'id': article['id'], 'title': title, 'summary': abstract, 'year': year, 'authors': authors, 'citation_ids': None }

def jbc_get_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10)
    for _ in range(total_papers // batch_size):
        start = random.randint(0, 10000)
        response = jbc_fetch_papers(start, batch_size, year)
        for paper in jbc_parse_response(response):
            yield paper

def jbc_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def jbc(max_results):
    years = jbc_sample_years(num_samples=max_results)
    for year, count in years.items():
        for paper in jbc_get_random_papers(year, total_papers=count):
            yield paper



# ================================= CELL ================================= #
# ================================= 4% ================================== #

def cell_fetch_papers(start, max_results, year):
    base_url = 'https://api.cell.com/articles?'
    query = f'year={year}&start={start}&limit={max_results}'
    response = requests.get(base_url + query)
    return response.json()

def cell_parse_response(response):
    for article in response['data']:
        title = article.get('title', 'No title')
        abstract = article.get('abstract', 'No abstract')
        authors = [author['name'] for author in article.get('authors', [])]
        year = article.get('year', 'No year')
        yield { 'id': article['id'], 'title': title, 'summary': abstract, 'year': year, 'authors': authors, 'citation_ids': None }

def cell_get_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10)
    for _ in range(total_papers // batch_size):
        start = random.randint(0, 10000)
        response = cell_fetch_papers(start, batch_size, year)
        for paper in cell_parse_response(response):
            yield paper

def cell_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def cell(max_results):
    years = cell_sample_years(num_samples=max_results)
    for year, count in years.items():
        for paper in cell_get_random_papers(year, total_papers=count):
            yield paper




# ================ THE JOURNAL OF EXPERIMENTAL BIOLOGY ================= #
# ================================= 2% ================================== #

def jeb_fetch_papers(start, max_results, year):
    base_url = 'https://api.biologists.com/jeb/articles?'
    query = f'year={year}&start={start}&limit={max_results}'
    response = requests.get(base_url + query)
    return response.json()

def jeb_parse_response(response):
    for article in response['data']:
        title = article.get('title', 'No title')
        abstract = article.get('abstract', 'No abstract')
        authors = [author['name'] for author in article.get('authors', [])]
        year = article.get('year', 'No year')
        yield { 'id': article['id'], 'title': title, 'summary': abstract, 'year': year, 'authors': authors, 'citation_ids': None }

def jeb_get_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10)
    for _ in range(total_papers // batch_size):
        start = random.randint(0, 10000)
        response = jeb_fetch_papers(start, batch_size, year)
        for paper in jeb_parse_response(response):
            yield paper

def jeb_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def jeb(max_results):
    years = jeb_sample_years(num_samples=max_results)
    for year, count in years.items():
        for paper in jeb_get_random_papers(year, total_papers=count):
            yield paper




if __name__ == '__main__':
    for paper in jeb(5):
        print(paper)







































