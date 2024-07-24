import requests
from bs4 import BeautifulSoup
import sqlite3
import random
import numpy as np
import time


"""
Basically, I think, as there isn't a random paper featre - I should instead have a number of kind of random methods, and pick one of these at random.
Methods:
    - Year search
    - Key word search (1000 of the most common words)


"""

# Database setup
conn = sqlite3.connect('scientific_papers.db')
cursor = conn.cursor()

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
            date = date_tag.text.strip().split()[-1] if date_tag else 'No date'
            authors = author_tag.text.strip() if author_tag else 'No authors'

            insert_into_db(title, abstract, authors, int(date), category)

            sampled_results.append([title, abstract, category, date, authors])
            if len(sampled_results) >= max_results:
                break

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

            insert_into_db(title, abstract, authors, int(date), category)

            sampled_results.append([title, abstract, category, date, authors])
            if len(sampled_results) >= max_results:
                break

def scrape_ieee(query, start_year, end_year, api_key):
    base_url = 'http://ieeexploreapi.ieee.org/api/v1/search/articles'
    headers = {'Accept': 'application/json'}

    for year in range(start_year, end_year + 1):
        params = {
            'apikey': api_key,
            'format': 'json',
            'querytext': query,
            'start_year': year,
            'end_year': year,
            'max_records': 100,
        }

        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Failed to retrieve data for year {year}. HTTP Status code: {response.status_code}")
            continue

        data = response.json()
        articles = data.get('articles', [])

        for article in articles:
            title = article.get('title', 'No title')
            abstract = article.get('abstract', 'No abstract')
            category = article.get('pubtitle', 'No category')
            date = article.get('publication_year', 'No date')

            insert_into_db(title, abstract, None, int(date), category)
            print(f"Added article from year {year}")

def scrape_jstor(query, start_year, end_year):
    base_url = 'https://www.jstor.org/action/doBasicSearch?Query='

    for year in range(start_year, end_year + 1):
        params = {
            'Query': query,
            'filter': f'year:{year}',
            'page': 1,
        }

        while True:
            response = requests.get(base_url, params=params)
            soup = BeautifulSoup(response.content, 'html.parser')

            papers = soup.find_all('div', class_='citation')

            if not papers:
                break

            for paper in papers:
                title_tag = paper.find('a', class_='title')
                abstract_tag = paper.find('div', class_='abstract')
                category_tag = paper.find('span', class_='discipline')
                date_tag = paper.find('div', class_='pubDate')

                title = title_tag.text.strip() if title_tag else 'No title'
                abstract = abstract_tag.text.strip() if abstract_tag else 'No abstract'
                category = category_tag.text.strip() if category_tag else 'No category'
                date = date_tag.text.strip() if date_tag else 'No date'

                insert_into_db(title, abstract, None, int(date), category)
                print(f"Added article from year {year}")

            params['page'] += 1

def scrape_google_scholar(query, start_year, end_year):
    base_url = 'https://scholar.google.com/scholar'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    for year in range(start_year, end_year + 1):
        params = {
            'q': query,
            'as_ylo': year,
            'as_yhi': year,
            'start': 0,
        }

        while True:
            response = requests.get(base_url, headers=headers, params=params)
            if response.status_code != 200:
                print(f"Failed to retrieve data for year {year}. HTTP Status code: {response.status_code}")
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            papers = soup.find_all('div', class_='gs_ri')

            if not papers:
                break

            for paper in papers:
                title_tag = paper.find('h3', class_='gs_rt')
                abstract_tag = paper.find('div', class_='gs_rs')
                category_tag = paper.find('div', class_='gs_a')
                date_tag = paper.find('div', class_='gs_a')

                title = title_tag.text.strip() if title_tag else 'No title'
                abstract = abstract_tag.text.strip() if abstract_tag else 'No abstract'
                category = category_tag.text.strip() if category_tag else 'No category'
                date = date_tag.text.strip().split('-')[-1].strip() if date_tag else 'No date'

                insert_into_db(title, abstract, None, int(date), category)
                print(f"Added article from year {year}")

            params['start'] += 10
            time.sleep(random.uniform(1, 3))  # Random sleep to avoid being blocked

# Example usage: Scrape Google Scholar papers on "artificial intelligence" from 2010 to 2023
scrape_google_scholar('artificial intelligence', 2010, 2023)

# Example usage: Scrape JSTOR papers on "artificial intelligence" from 2010 to 2023
scrape_jstor('artificial intelligence', 2010, 2023)

# Example usage: Scrape IEEE papers on "artificial intelligence" from 2010 to 2023
scrape_ieee('artificial intelligence', 2010, 2023, 'your_api_key')

# Example usage: Scrape 100 random papers from arXiv
scrape_arxiv(10)

# Example usage: Scrape 100 random papers from PubMed
scrape_pubmed(10)

# Close the database connection
conn.close()



import requests
from Bio import Entrez
import xml.etree.ElementTree as ET

def simplify_text(text:str):
    return text.encode('ascii', 'ignore').decode('ascii')

def semantic_scholar(query, limit=10):
    url = f'https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={limit}&fields=title,abstract,authors,year'
    response = requests.get(url)
    data_unformatted = response.json()['data']
    data = [(paper['title'],
            paper['abstract'],
            ' ,'.join([author['name'] for author in paper['authors']]),
            int(paper['year']),
            'Unknown',
            b'') for paper in data_unformatted]
    return data

def pubmed(query, limit=10):
    Entrez.email = 'lwg376@student.bham.ac.uk'
    handle = Entrez.esearch(db='pubmed', term=query, retmax=limit)
    record = Entrez.read(handle)
    id_list = record['IdList']

    data = []
    for paper_id in id_list:
        handle = Entrez.efetch(db='pubmed', id=paper_id, retmode='xml')
        records = Entrez.read(handle)
        paper = records['PubmedArticle'][0]['MedlineCitation']['Article']
        data_point = (simplify_text(paper['ArticleTitle']),
                      simplify_text(paper.get('Abstract', {}).get('AbstractText', [''])[0]),
                      simplify_text(', '.join([author['LastName'] + ' ' + author['ForeName'] for author in paper.get('AuthorList', [])])),
                      int(paper['Journal']['JournalIssue']['PubDate'].get('Year')),
                      'PubMed',
                      b'')
        data.append(data_point)
    return data
    
def ieee(query, limit=10):
    # Need ieee key!!
    api_key = None
    
    response = request.get(f'https://ieeexploreapi.ieee.org/api/v1/search/articles?querytext={query}&apikey={api_key}&max_records=10')
    return [(paper['title'],
             paper.get('abstract', ''),
             ', '.join([author['full_name'] for author in paper.get('authors', {}).get('authors', [])]),
             paper['publication_year'],
             paper.get('publication_title', 'Unknown'),
             b'') for paper in response.json()['articles']]
    # title, abstract, authors, year, category 

def arxiv(query):
    # take the code you have already written and adapt it as it was a bit more developed than these snippets
    return




def arXiv(query, limit=10):
    base_url = "http://export.arxiv.org/api/query"
    query_params = {
        "search_query": query,
        "start": 0,  # Start at the first result
        "max_results": limit
    }

    response = requests.get(base_url, params=query_params)
    root = ET.fromstring(response.text)

    papers = []
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }

    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        
        authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        authors_str = ", ".join(authors)
        
        published = entry.find('{http://www.w3.org/2005/Atom}published').text
        year = int(published.split('-')[0])  # Extracting the year from the published date

        primary_category = entry.find('arxiv:primary_category', ns).attrib['term'] if entry.find('arxiv:primary_category', ns) is not None else ''

        data_point = (
            simplify_text(title),
            simplify_text(summary),
            simplify_text(authors_str),
            year,
            simplify_text(primary_category),
            b''
        )
        papers.append(data_point)

    return papers


if __name__ == '__main__':
    data = arXiv('all')
    print(data)

