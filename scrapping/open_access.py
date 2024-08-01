from bs4 import BeautifulSoup
import numpy as np
import random
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import xml.etree.ElementTree as ET

from common_words import words


def get_all(max_results):
    max_results = max(8, max_results) # 8 is the amount needed to get the distribution
    numb = {'arxiv': max_results // 3,
                  'biorxiv': max_results // 5,
                  'chemrxiv': max_results // 7.5,
                  'pubmed': max_results // 3}

    for paper in arxiv(numb['arxiv']):
        yield paper
    for paper in biorxiv(numb['biorxiv']):
        yield paper
    for paper in chemrxiv(numb['chemrxiv']):
        yield paper
    for paper in pubmed(numb['pubmed']):
        yield paper


# =============================== ARXIV ================================ #

def arxiv_fetch_papers(start, max_results, year):
    base_url = 'http://export.arxiv.org/api/query?'
    query = f'search_query=submittedDate:[{year}01010000+TO+{year}12312359]&start={start}&max_results={max_results}'
    response = requests.get(base_url + query)
    return response.content

def arxiv_parse_response(response, year):
    root = ET.fromstring(response)
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        yield { 'id': entry.find('{http://www.w3.org/2005/Atom}id').text, 'title': entry.find('{http://www.w3.org/2005/Atom}title').text, 'summary': summary, 'year': year, 'authors': authors, 'citation_ids': None, 'source': 'arxiv'}

def arxiv_get_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10) 
    for _ in range(total_papers // batch_size):
        start = random.randint(0, 10000)  
        response = arxiv_fetch_papers(start, batch_size, year)
        for paper in arxiv_parse_response(response, year):
            yield paper

def arxiv_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def arxiv(max_results):
    years = arxiv_sample_years(num_samples=max_results)
    for year, count in years.items():
        for paper in arxiv_get_random_papers(year, total_papers=count):
            yield paper

# ============================== BIORXIV =============================== #

def biorxiv_fetch_papers(start, max_results, year):
    base_url = 'https://api.biorxiv.org/details/biorxiv/'
    query = f'{year}-01-01/{year}-12-31/{start}/{max_results}'
    response = requests.get(base_url + query)
    return response.json()

def biorxiv_parse_response(response, year):
    for item in response['collection']:
        authors = item['authors'].split('; ')
        yield { 'id': item['doi'], 'title': item['title'], 'summary': item['abstract'], 'year': year, 'authors': authors, 'citation_ids': None, 'source': 'biorxiv'}

def biorxiv_get_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10) 
    for _ in range(total_papers // batch_size):
        start = random.randint(0, 10000)  
        response = biorxiv_fetch_papers(start, batch_size, year)
        for paper in biorxiv_parse_response(response, year):
            yield paper

def biorxiv_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def biorxiv(max_results):
    years = biorxiv_sample_years(num_samples=max_results)
    for year, count in years.items():
        for paper in biorxiv_get_random_papers(year, total_papers=count):
            yield paper

# ============================== CHEMRXIV =============================== #

def chemrxiv_fetch_papers(page, batch_size, year):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uncomment if you want to run headless
    chrome_options.add_argument("--disable-gpu")

    url = f'https://chemrxiv.org/engage/chemrxiv/public-dashboard?sort=published_desc&page={page}&rows={batch_size}&subtype=preprint&category=chemistry&dateFilter={year}'
    driver = webdriver.Chrome(service=Service(r'C:\Users\Student\Documents\Uni_Birmingham\project\scientific_space\software\current\scrapping\chromedriver.exe'), options=chrome_options)
    driver.get(url)

    # Wait for the page to load and display the articles
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.ArticleSummary"))
    )

    articles = driver.find_elements(By.CSS_SELECTOR, "a.ArticleSummary")
    for article in articles:
        title_tag = article.find_element(By.CSS_SELECTOR, "div.height-64 h3 span")
        title = title_tag.text if title_tag else 'No title'
        link = article.get_attribute('href')
        doi = link.split('/')[-1] if link else 'No DOI'
        abstract = 'No abstract'
        authors = article.find_element(By.CSS_SELECTOR, "div.pt-2").text.split(", ")

        # Extract citation IDs from the abstract or other available fields if present
        citation_ids = re.findall(r'ChemRxiv:\d+\.\d+', abstract)

        yield { 'id': doi, 'title': title, 'summary': abstract, 'year': year, 'authors': authors, 'citation_ids': citation_ids, 'source': 'chemrxiv'}
    
    driver.quit()

def chemrxiv_get_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10)
    for _ in range(total_papers // batch_size):
        page = random.randint(0, 100)  # Adjust range as necessary
        for paper in chemrxiv_fetch_papers(page, batch_size, year):
            yield paper

def chemrxiv_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def chemrxiv(max_results):
    years = chemrxiv_sample_years(num_samples=max_results)
    for year, count in years.items():
        for paper in chemrxiv_get_random_papers(year, total_papers=count):
            yield paper

# =============================== PUBMED ================================ #
def pubmed_fetch_papers(start, max_results, year):
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
    query = f'db=pubmed&term={year}[PDAT]&retstart={start}&retmax={max_results}&usehistory=y'
    response = requests.get(base_url + query)
    root = ET.fromstring(response.content)
    webenv = root.find('WebEnv').text
    query_key = root.find('QueryKey').text
    return webenv, query_key

def pubmed_fetch_details(webenv, query_key, start, max_results):
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'
    query = f'db=pubmed&query_key={query_key}&WebEnv={webenv}&retstart={start}&retmax={max_results}&retmode=xml'
    response = requests.get(base_url + query)
    return response.content

def pubmed_parse_response(response):
    root = ET.fromstring(response)
    for article in root.findall('.//PubmedArticle'):
        pmid = article.find('.//PMID').text
        title = article.find('.//ArticleTitle').text
        abstract = article.find('.//Abstract/AbstractText').text if article.find('.//Abstract/AbstractText') is not None else 'No abstract'
        authors = [author.find('LastName').text + ' ' + author.find('ForeName').text for author in article.findall('.//Author')]
        year = article.find('.//PubDate/Year').text if article.find('.//PubDate/Year') is not None else 'No year'
        yield { 'id': pmid, 'title': title, 'summary': abstract, 'year': year, 'authors': authors, 'citation_ids': None, 'source': 'pubmed' }

def pubmed_get_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10)
    webenv, query_key = pubmed_fetch_papers(0, total_papers, year)
    for _ in range(total_papers // batch_size):
        start = random.randint(0, 10000)
        response = pubmed_fetch_details(webenv, query_key, start, batch_size)
        for paper in pubmed_parse_response(response):
            yield paper

def pubmed_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def pubmed(max_results):
    years = pubmed_sample_years(num_samples=max_results)
    for year, count in years.items():
        for paper in pubmed_get_random_papers(year, total_papers=count):
            yield paper




if __name__ == '__main__':
    cheese = pubmed(5)
    for n in cheese:
        print(n)





























# ============================== OLD CODE =============================== #



"""

from Bio import Entrez
import numpy as np
import random

Entrez.email = 'lwg376@student.bham.ac.uk'  # Replace with your email

# Function to fetch PubMed papers given a search query
def fetch_pubmed_papers(start, max_results, year):
    handle = Entrez.esearch(db="pubmed", term=f"{year}[dp]", retstart=start, retmax=max_results)
    record = Entrez.read(handle)
    id_list = record["IdList"]
    papers = []
    if id_list:
        handle = Entrez.efetch(db="pubmed", id=",".join(id_list), rettype="abstract", retmode="xml")
        records = Entrez.read(handle)
        for article in records['PubmedArticle']:
            paper = {
                'id': article['MedlineCitation']['PMID'],
                'title': article['MedlineCitation']['Article']['ArticleTitle'],
                'abstract': article['MedlineCitation']['Article']['Abstract']['AbstractText'] if 'Abstract' in article['MedlineCitation']['Article'] else '',
                'year': year,
                'authors' : None,
                'citation_ids': None
            }
            papers.append(paper)
    return papers

# Function to estimate the number of papers in a specific year (based on the growth rate)
def numb_papers_year(year):
    initial_year = 1990
    initial_papers = 10000  # Assume an initial number of papers in 1990
    annual_growth_rate = 0.05  # 5% annual growth rate
    return int(initial_papers * ((1 + annual_growth_rate) ** (year - initial_year)))

# Function to get a list of random PubMed papers from a specific year
def get_random_pubmed_papers(year, total_papers=100, batch_size=100):
    batch_size = max(1, min(total_papers, numb_papers_year(year)) // 10)
    random_papers = []
    while len(random_papers) < total_papers:
        start = random.randint(0, min(numb_papers_year(year), 9998) - batch_size)
        papers = fetch_pubmed_papers(start, batch_size, year)
        random_papers.extend(papers)
        if len(random_papers) > total_papers:
            random_papers = random_papers[:total_papers]
    return random_papers

# Function to sample years based on growth rates and probabilities
def sample_years(start_year=1990, end_year=2024, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.05 * ((1 + 0.05) ** (years - start_year))
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities)
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

# Function to get papers across sampled years
def get_papers(max_results):
    years = sample_years(num_samples=max_results)
    all_papers = []
    for year, count in years.items():
        papers = get_random_pubmed_papers(year, total_papers=count)
        all_papers.extend(papers)
    return all_papers



if __name__ == '__main__':
    # Example usage
    max_results = 100  # Number of random papers to fetch
    random_papers = get_papers(max_results)
    
    # Print the titles of the random papers
    for i, paper in enumerate(random_papers):
        print(f"{i+1}. {paper['title']}")








"""












