import requests
from bs4 import BeautifulSoup
import csv
import random
import numpy as np

# List of categories and their approximate weights
categories_weights = [ ('physics', 50), ('astro-ph', 40), ('cond-mat', 40), ('gr-qc', 20), ('hep-ex', 30), ('hep-lat', 20), ('hep-ph', 40), ('hep-th', 40), ('nucl-ex', 20), ('nucl-th', 20), ('quant-ph', 30), ('math', 50), ('math.AG', 20), ('math.AT', 10), ('math.AP', 15), ('math.CA', 15), ('math.CO', 20), ('math.CT', 10), ('math.CV', 10), ('cs.AI', 30), ('cs.CL', 20), ('cs.CC', 15), ('cs.CE', 10), ('cs.CG', 15), ('cs.CV', 25), ('cs.CR', 20), ]

categories, weights = zip(*categories_weights)

def scrape_arxiv(max_results):
    base_url = 'https://arxiv.org/list/{category}/pastweek?skip='
    results_per_page = 100

    sampled_results = []
    while len(sampled_results) < max_results:
        category = random.choices(categories, weights)[0]
        skip = random.randint(0, 1000)  # Arbitrary high number to cover more pages

        url = f'{base_url}{skip}&show={results_per_page}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        papers = soup.find_all('div', class_='meta')
        if not papers:
            continue

        for paper in papers:
            title_tag = paper.find('div', class_='list-title')
            abstract_tag = paper.find('p', class_='abstract')
            category_tag = paper.find('span', class_='primary-subject')
            date_tag = paper.find('div', class_='list-dateline')
            author_tag = paper.find('div', class_='list-authors')

            title = title_tag.text.strip() if title_tag else 'No title'
            abstract = abstract_tag.text.strip() if abstract_tag else 'No abstract'
            category = category_tag.text.strip() if category_tag else 'No category'
            date = date_tag.text.strip() if date_tag else 'No date'
            authors = author_tag.text.strip() if author_tag else 'No authors'

            sampled_results.append([title, abstract, category, date, authors])
            if len(sampled_results) >= max_results:
                break

    with open('arxiv_papers.csv', mode='w', newline='', encoding='utf-8', errors='ignore') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Abstract', 'Category', 'Date', 'Authors'])
        writer.writerows(sampled_results)


def scrape_pubmed(max_results):
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    fetch_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    years = list(range(2000, 2024))  # Add more years if needed

    sampled_results = []
    while len(sampled_results) < max_results:
        year = random.choice(years)
        params = {
            'db': 'pubmed',
            'term': f'{year}[DP]',
            'retmax': 100,
            'retmode': 'json',
            'usehistory': 'y'
        }
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"Failed to retrieve data for year {year}. HTTP Status code: {response.status_code}")
            continue

        data = response.json()
        if 'esearchresult' not in data or 'idlist' not in data['esearchresult']:
            print(f"No results found for year {year}.")
            continue

        id_list = data['esearchresult']['idlist']
        if not id_list:
            print(f"No articles found for year {year}.")
            continue

        fetch_params = {
            'db': 'pubmed',
            'retmode': 'xml',
            'rettype': 'abstract',
            'id': ','.join(id_list)
        }
        fetch_response = requests.get(fetch_url, params=fetch_params)
        if fetch_response.status_code != 200:
            print(f"Failed to fetch details for year {year}. HTTP Status code: {fetch_response.status_code}")
            continue

        soup = BeautifulSoup(fetch_response.content, 'xml')
        articles = soup.find_all('PubmedArticle')

        for article in articles:
            title_tag = article.find('ArticleTitle')
            abstract_tag = article.find('AbstractText')
            category_tag = article.find('Journal')
            date_tag = article.find('PubDate').find('Year')
            author_tags = article.find_all('Author')
            authors = ', '.join([author.find('LastName').text for author in author_tags if author.find('LastName')])

            title = title_tag.text if title_tag else 'No title'
            abstract = abstract_tag.text if abstract_tag else 'No abstract'
            category = category_tag.find('Title').text if category_tag else 'No category'
            date = date_tag.text if date_tag else 'No date'

            sampled_results.append([title, abstract, category, date, authors])
            if len(sampled_results) >= max_results:
                break

    with open('pubmed_papers.csv', mode='w', newline='', encoding='utf-8', errors='ignore') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Abstract', 'Category', 'Date', 'Authors'])
        writer.writerows(sampled_results)


# Example usage: Scrape 100 random papers from arXiv
scrape_arxiv(10)

# Example usage: Scrape 100 random papers from PubMed
scrape_pubmed(10)
