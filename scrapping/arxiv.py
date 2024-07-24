import requests
from xml.etree import ElementTree
from bs4 import BeautifulSoup
import random
import numpy as np
import time

from common_words import words



def sample_year(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    
    probabilities = growth_rates / np.sum(growth_rates)
    
    # Sample years based on the probabilities
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    
    return sampled_years

"""
# List of categories and their approximate weights
categories_weights = [('physics', 50), ('astro-ph', 40), ('cond-mat', 40), ('gr-qc', 20), ('hep-ex', 30), 
                      ('hep-lat', 20), ('hep-ph', 40), ('hep-th', 40), ('nucl-ex', 20), ('nucl-th', 20), 
                      ('quant-ph', 30), ('math', 50), ('math.AG', 20), ('math.AT', 10), ('math.AP', 15), 
                      ('math.CA', 15), ('math.CO', 20), ('math.CT', 10), ('math.CV', 10), ('cs.AI', 30), 
                      ('cs.CL', 20), ('cs.CC', 15), ('cs.CE', 10), ('cs.CG', 15), ('cs.CV', 25), ('cs.CR', 20)]

categories, weights = zip(*categories_weights)

def query_arxiv(search_query, max_results=10):
    base_url = "http://export.arxiv.org/api/query"
    query_params = {
        "search_query": search_query,
        "start": 0,  # Start at the first result
        "max_results": max_results
    }
    
    response = requests.get(base_url, params=query_params)
    return response.text

def parse_xml(xml_data):
    root = ElementTree.fromstring(xml_data)
    
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        # Extracting title
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        
        # Extracting summary
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        
        # Extracting authors
        authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        
        # Extracting DOI
        doi = None
        for link in entry.findall('{http://www.w3.org/2005/Atom}link'):
            if link.get('title') == 'doi':
                doi = link.get('href')
        
        # Extracting category
        category = entry.find('{http://www.w3.org/2005/Atom}category').get('term')
        
        # Extracting published year
        published_date = entry.find('{http://www.w3.org/2005/Atom}published').text
        published_year = published_date[:4]  # Assumes the date is in the format YYYY-MM-DD
        
        yield {'title': title, 'summary':summary, 'authors':authors, 'doi': doi, 'category': category, 'year': published_year}

def get_papers(max_results=10):
    word = random.choice(words)
    date = 

    xml_data = query_arxiv(search_query, max_results)
    for paper in parse_xml(xml_data):
        yield paper



if __name__ == '__main__':
    for paper in get_papers('physics', 10):
        print(paper)





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

            sampled_results.append({
                'title': title,
                'abstract': abstract,
                'category': category,
                'date': date,
                'authors': authors
            })
            if len(sampled_results) >= max_results:
                break

    return sampled_results
"""
