import requests
import xml.etree.ElementTree as ET
import random
import numpy as np
import re
import time


def rate_limiter(cps=None, spc=None):
    if cps and spc:
        min_interval = min(float(spc), 1.0/float(cps))
    elif cps:
        min_interval = 1.0/float(cps)
    elif spc:
        min_interval = float(spc)
    else:
        raise ValueError("At least one of 'cps' or 'spc' must be provided and not be None.")


    def decorator(func):
        last_call_time = [0.0]

        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call_time[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            last_call_time[0] = time.time()
            return func(*args, **kwargs)

        return wrapper
    return decorator


@rate_limiter(spc=1)
def fetch_arxiv_papers(start, max_results):
    base_url = 'http://export.arxiv.org/api/query?'
    year = 2024
    query = f'search_query=submittedDate:[{year}01010000+TO+{year}12312359]&start={start}&max_results={max_results}'
    response = requests.get(base_url + query)
    return response.content

def parse_arxiv_response(response):
    root = ET.fromstring(response)
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        paper_id = entry.find('{http://www.w3.org/2005/Atom}id').text
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        
        # Get the primary category
        primary_category = entry.find('{http://arxiv.org/schemas/atom}primary_category').attrib['term']
        
        content = fetch_arxiv_content(paper_id)
        
        yield {
            'id': paper_id,
            'title': title,
            'summary': summary,
            'year': 2024,
            'authors': authors,
            'content': content,
            'primary_category': primary_category  # Include the primary category
        }


@rate_limiter(spc=3)
def fetch_arxiv_content(paper_id):
    # Fetch HTML content
    html_url = f"https://arxiv.org/html/{paper_id.split('/')[-1]}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(html_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch HTML for paper {paper_id}: Status code {response.status_code}")
        return None
    
    content = response.text
    
    # Extract content after the first <section> or similar HTML section tag
    section_match = re.search(r'<section.*?>', content, re.IGNORECASE)
    if section_match:
        content = content[section_match.end():]
    else:
        print(f"No <section> tag found in HTML for paper {paper_id}. Using the full HTML content.")
    
    # Return first 1000 words of HTML content
    content_words = re.split(r'\s+', re.sub(r'<[^>]+>', '', content))
    first_1000_words = ' '.join(content_words[:1000])
    return first_1000_words

def arxiv_random_papers(total_papers=100):
    batch_size = max(1, min(total_papers, 100))  # Limit batch size to a max of 100
    for _ in range(total_papers // batch_size):
        start = random.randint(0, 10000)  
        response = fetch_arxiv_papers(start, batch_size)
        for paper in parse_arxiv_response(response):
            yield paper

def arxiv_papers(max_results=1000):
    count = 1
    for paper in arxiv_random_papers(total_papers=max_results):
        print(f'Fetching paper {count}')
        try:
            yield paper
        except Exception as e:
            print(f'Error: {e}')
        count += 1
