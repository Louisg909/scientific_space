

BASE_URL = "https://journals.aps.org"
journals = ["prl", "pra", "prb", "prc", "prd", "pre", "prx", "rmp"]

def get_largest_issue_id(journal):
    issues_url = f"{BASE_URL}/{journal}/issues"
    response = requests.get(issues_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    h4_tags = soup.find_all('h4', id=re.compile('^v\d+'))
    largest_id = max(int(tag['id'][1:]) for tag in h4_tags)
    
    return largest_id

def get_random_issue_page(journal, largest_id):
    while True:
        random_id = random.randint(1, largest_id)
        random_issue_url = f"{BASE_URL}/{journal}/issues/{random_id}#v{random_id}"
        response = requests.get(random_issue_url)
        if response.status_code == 200:
            return response.content, random_id

def get_issue_list(html_content, id_number):
    soup = BeautifulSoup(html_content, 'html.parser')
    issue_div = soup.find('h4', id=f'v{id_number}')
    if not issue_div:
        return None
    
    issue_list = issue_div.find_next('ul').find_all('li')
    if not issue_list:
        return None
    
    return issue_list

def get_random_paper_url(issue_list):
    issue_url = BASE_URL + issue_list[random.randint(0, len(issue_list) - 1)].find('a')['href']
    response = requests.get(issue_url)
    if response.status_code == 200:
        return response.content, issue_url
    else:
        raise ValueError("Failed to fetch issue page.")

def get_article_list(issue_html_content, issue_url):
    soup = BeautifulSoup(issue_html_content, 'html.parser')
    article_sections = soup.find_all('div', class_='article panel article-result')
    if not article_sections:
        raise ValueError("No articles found in the issue")
    
    articles = []
    for section in article_sections:
        group_title_tag = section.find_previous('h4', class_='title')
        if group_title_tag:
            group_title = group_title_tag.text.strip()
        else:
            group_title = "Unknown"

        article_link = section.find('h5', class_='title').find('a')['href']
        articles.append((BASE_URL + article_link, group_title))
    
    return articles

def get_paper_details(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    paper_details = {}

    main_div = soup.find('div', class_='medium-9 columns')
    if not main_div:
        raise ValueError("No main content div found")

    title_tag = main_div.find('h3')
    if not title_tag:
        raise ValueError("No title found")
    paper_details['title'] = title_tag.text.strip()

    authors_tag = main_div.find('h5', class_='authors')
    if not authors_tag:
        raise ValueError("No authors found")
    paper_details['authors'] = authors_tag.text.strip()

    pub_info_tag = main_div.find('h5', class_='pub-info')
    if not pub_info_tag:
        raise ValueError("No publication info found")
    pub_info_text = pub_info_tag.text.strip()
    year_match = re.search(r'\d{4}', pub_info_text)
    paper_details['year'] = year_match.group(0) if year_match else "Unknown"

    abstract_div = soup.find('div', class_='content')
    if not abstract_div:
        raise ValueError("No abstract found")
    abstract_paragraph = abstract_div.find('p')
    abstract_text = ' '.join(abstract_paragraph.stripped_strings)
    abstract_text = re.sub(r'<span>[^<]*</span>', '{equation}', abstract_text)
    paper_details['summary'] = abstract_text.strip()

    return paper_details

def get_aps_papers(numb_papers=1500):
    journal_issue_map = {journal: get_largest_issue_id(journal) for journal in journals}
    
    articles_collected = 0
    while articles_collected < numb_papers:
        selected_journal = random.choice(journals)
        largest_id = journal_issue_map[selected_journal]
        html_content, random_id = get_random_issue_page(selected_journal, largest_id)
        issue_list = get_issue_list(html_content, random_id)

        if issue_list:
            issue_html_content, issue_url = get_random_paper_url(issue_list)
            article_list = get_article_list(issue_html_content, issue_url)
            
            t1 = time.time()
            for article_url, group_title in article_list:
                if articles_collected >= numb_papers:
                    break
                if t2 - t1 > 1:
                    time.sleep(t2 - t1)
                t2 = time.time()
                paper_html_content = requests.get(article_url).content
                t1 = time.time()
                paper_details = get_paper_details(paper_html_content)
                paper_details['subtitle'] = group_title
                paper_details['source'] = f'aps-{selected_journal}'
                yield paper_details
                articles_collected += 1

# Example usage
if __name__ == "__main__":
    numb_papers = 5
    for paper in get_aps_papers(numb_papers):
        print(paper)




import time
import random
import numpy as np
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xml.etree.ElementTree as ET


def get_all_papers(max_results):
    max_results = max(8, max_results) # 8 is the amount needed to get the distribution
    source_distribution = {
            'arxiv': max_results // 3,
            'biorxiv': max_results // 5,
            'chemrxiv': max_results // 7.5,
            'pubmed': max_results // 3
            }

    for paper in arxiv(source_distribution['arxiv']):
        yield paper
    for paper in biorxiv(source_distribution['biorxiv']):
        yield paper
    for paper in chemrxiv(source_distribution['chemrxiv']):
        yield paper
    for paper in pubmed(source_distribution['pubmed']):
        yield paper


# =============================== ARXIV ================================ #

def fetch_arxiv_papers(start, max_results, year):
    base_url = 'http://export.arxiv.org/api/query?'
    query = f'search_query=submittedDate:[{year}01010000+TO+{year}12312359]&start={start}&max_results={max_results}'
    response = requests.get(base_url + query)
    return response.content

def parse_arxiv_response(response, year):
    root = ET.fromstring(response)
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        yield {
                'id': entry.find('{http://www.w3.org/2005/Atom}id').text,
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text,
                'summary': summary,
                'year': year,
                'authors': authors,
                'citation_ids': None,
                'source': 'arxiv'
                }

def arxiv_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10)
    for _ in range(total_papers // batch_size):
        start = random.randint(0, 10000)  
        response = fetch_arxiv_papers(start, batch_size, year)
        for paper in parse_arxiv_response(response, year):
            yield paper

def arxiv_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def arxiv_papers(max_results=1000):
    years = arxiv_sample_years(num_samples=max_results)
    for year, count in years.items():
        for paper in arxiv_random_papers(year, total_papers=count):
            yield paper

# ============================== BIORXIV =============================== #

def fetch_biorxiv_papers(start, max_results, year):
    base_url = 'https://api.biorxiv.org/details/biorxiv/'
    query = f'{year}-01-01/{year}-12-31/{start}/{max_results}'
    response = requests.get(base_url + query)
    return response.json()

def parse_biorxiv_response(response, year):
    for item in response['collection']:
        authors = item['authors'].split('; ')
        yield {
                'id': item['doi'],
                'title': item['title'],
                'summary': item['abstract'],
                'year': year,
                'authors': authors,
                'citation_ids': None,
                'source': 'biorxiv'
                }

def biorxiv_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10)   # TODO update according to data about bioRxiv
    for _ in range(total_papers // batch_size):
        start = random.randint(0, 10000)  
        response = fetch_biorxiv_papers(start, batch_size, year)
        for paper in parse_biorxiv_response(response, year):
            yield paper

def biorxiv_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14 # TODO update with bioRxiv data
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def biorxiv_papers(max_results=1000):
    years = biorxiv_sample_years(num_samples=max_results)
    for year, count in years.items():
        for paper in biorxiv_random_papers(year, total_papers=count):
            yield paper

# ============================== CHEMRXIV =============================== #

def fetch_chemrxiv_papers(page, batch_size, year):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Stopps the UI from popping up
    chrome_options.add_argument("--disable-gpu")

    url = f'https://chemrxiv.org/engage/chemrxiv/public-dashboard?sort=published_desc&page={page}&rows={batch_size}&subtype=preprint&category=chemistry&dateFilter={year}'
    driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=chrome_options)
    driver.get(url)

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

        citation_ids = re.findall(r'ChemRxiv:\d+\.\d+', abstract)

        yield { 
               'id': doi,
               'title': title,
               'summary': abstract,
               'year': year,
               'authors': authors,
               'citation_ids': citation_ids,
               'source': 'chemrxiv'
               }
    
    driver.quit()

def chemrxiv_get_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10) # TODO get this for chemRxiv specifically
    for _ in range(total_papers // batch_size):
        page = random.randint(0, 100) 
        for paper in fetch_chemrxiv_papers(page, batch_size, year):
            yield paper

def chemrxiv_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def chemrxiv_papers(max_results=1000):
    years = chemrxiv_sample_years(num_samples=max_results)
    for year, count in years.items():
        for paper in chemrxiv_get_random_papers(year, total_papers=count):
            yield paper




# =============================== PUBMED ================================ #
def fetch_pubmed_papers(start, max_results, year):
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
    query = f'db=pubmed&term={year}[PDAT]&retstart={start}&retmax={max_results}&usehistory=y'
    response = requests.get(base_url + query)
    root = ET.fromstring(response.content)
    webenv = root.find('WebEnv').text
    query_key = root.find('QueryKey').text
    return webenv, query_key

def fetch_pubmed_details(webenv, query_key, start, max_results):
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'
    query = f'db=pubmed&query_key={query_key}&WebEnv={webenv}&retstart={start}&retmax={max_results}&retmode=xml'
    response = requests.get(base_url + query)
    return response.content

def parse_pubmed_response(response):
    root = ET.fromstring(response)
    for article in root.findall('.//PubmedArticle'):
        pmid = article.find('.//PMID').text
        title = article.find('.//ArticleTitle').text
        abstract = article.find('.//Abstract/AbstractText').text if article.find('.//Abstract/AbstractText') is not None else 'No abstract'
        authors = [author.find('LastName').text + ' ' + author.find('ForeName').text for author in article.findall('.//Author')]
        year = article.find('.//PubDate/Year').text if article.find('.//PubDate/Year') is not None else 'No year'
        yield { 
               'id': pmid,
               'title': title,
               'summary': abstract,
               'year': year,
               'authors': authors,
               'citation_ids': None,
               'source': 'pubmed'
               }

def pubmed_random_papers(year, total_papers=100):
    batch_size = max(1, min(total_papers, round(40 * np.exp(0.2 * year) + 3140)) // 10) # TODO get actual values for PUBMED
    webenv, query_key = fetch_pubmed_papers(0, total_papers, year)
    for _ in range(total_papers // batch_size):
        start = random.randint(0, 10000)
        response = pubmed_fetch_details(webenv, query_key, start, batch_size)
        for paper in parse_pubmed_response(response):
            yield paper

def pubmed_sample_years(start_year=0, end_year=34, num_samples=1000):
    years = np.arange(start_year, end_year + 1)
    growth_rates = 0.04 * np.exp(0.2 * years) + 3.14
    probabilities = growth_rates / np.sum(growth_rates)
    sampled_years = np.random.choice(years, size=num_samples, p=probabilities) + 1990
    return dict(zip(*np.unique(sampled_years, return_counts=True)))

def pubmed_papers(max_results=1500):
    years = pubmed_sample_years(num_samples=max_results)
    for year, count in years.items():
        for paper in pubmed_random_papers(year, total_papers=count):
            yield paper






























# ============================== OLD CODE =============================== #



"""

from Bio import Entrez
import numpy as np
import random

Entrez.email = ''

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




import random
import time

from crossref_commons.iteration import iterate_publications_as_json

def extract_crossref_metadata(publication_data):
    """Extract metadata from a CrossRef publication JSON."""
    title = publication_data.get('title', [''])[0]
    abstract = publication_data.get('abstract', '')
    publication_year = publication_data.get('published-print', {}).get('date-parts', [[None]])[0][0]
    source = publication_data.get('container-title', [''])[0]
    authors = [f"{author.get('given', '')} {author.get('family', '')}" for author in publication_data.get('author', [])]
    return {
        'doi': publication_data.get('DOI', ''),
        'title': title,
        'summary': abstract,
        'year': publication_year,
        'source': source,
        'authors': ', '.join(authors)
    }

def retrieve_crossref_publications(max_results_per_query=1000, total_iterations=500, source_filter=None):
    """Retrieve publications from CrossRef with metadata, using various queries."""
    max_results_per_query = min(1000, max_results_per_query)
    request_buffer_seconds = 1  # Minimum delay between requests XXX check
    timer = 0
    if source_filter is None:
        source_filter = {
                'type': 'journal-article',
                'has-abstract': 'true',
                }

    queries = [
        # General Science Fields
        'science OR technology OR biology OR physics OR chemistry OR engineering OR geology OR environmental OR mathematics OR neuroscience OR astronomy OR computer science',
        # High-Impact Journals
        'Nature', 'Science', 'PNAS', 'PLOS', 'Physical Review', 'Journal of Applied Physics', 'Journal of High Energy Physics',
        'Journal of the American Chemical Society', 'Angewandte Chemie', 'Chemical Science', 'Journal of Biological Chemistry', 'Cell', 
        'Journal of Experimental Biology', 'Geophysical Research Letters', 'Journal of Geophysical Research', 
        'Environmental Science & Technology', 'Nature Communications', 'Science Advances', 'Journal of Interdisciplinary Science Topics',
        # Specific Scientific Fields
        'quantum mechanics OR particle physics OR condensed matter physics OR astrophysics OR nuclear physics',
        'organic chemistry OR inorganic chemistry OR physical chemistry OR analytical chemistry OR biochemistry OR materials science',
        'molecular biology OR cellular biology OR genetics OR microbiology OR immunology OR biotechnology',
        'geology OR geophysics OR climate science OR oceanography OR environmental science',
        'mechanical engineering OR electrical engineering OR civil engineering OR chemical engineering OR aerospace engineering',
        'applied mathematics OR pure mathematics OR statistics OR computational science OR artificial intelligence',
        'interdisciplinary research OR multidisciplinary science OR scientific reviews OR technology and innovation',
        'complex systems OR systems biology OR nanotechnology OR bioinformatics OR biophysics OR chemical biology'
    ]

    query_weights = [
        0.065,  # General Science Fields
        0.032, 0.032, 0.032, 0.032,  # High-Impact Journals (Nature, Science, PNAS, PLOS)
        0.019, 0.019, 0.019, 0.019, 0.019,  # High-Impact Journals (Physical Review, JAP, JHEP, Journal of the American Chemical Society, Angewandte Chemie)
        0.019, 0.019, 0.019, 0.019, 0.019,  # High-Impact Journals (Chemical Science, Journal of Biological Chemistry, Cell, Journal of Experimental Biology, Geophysical Research Letters)
        0.019, 0.019, 0.019, 0.019, 0.019,  # High-Impact Journals (Journal of Geophysical Research, Environmental Science & Technology, Nature Communications, Science Advances, Journal of Interdisciplinary Science Topics)
        0.065, 0.065, 0.065, 0.065, 0.065, 0.065, 0.065, 0.065  # Specific Scientific Fields
    ]

    processed_dois = set()

    max_results = int(max_results_per_query / max(query_weights))

    for iteration in range(total_iterations):
        for query, weight in zip(queries, query_weights):
            # Request with buffering to be polite (but also take advantage of any time spent doing other things)
            if delta_time := (time.time() - timer - request_buffer_seconds) > 0:
                time.sleep(delta_time)
            publications = list(iterate_publications_as_json(max_results=int(max_results * weight), filter=source_filter, queries={'query': query}))
            timer = time.time()

            for publication in publications:
                doi = publication['DOI']
                if doi not in processed_dois:
                    metadata = extract_crossref_metadata(publication)
                    processed_dois.add(doi)
                    yield metadata

def main():
    max_results_per_query = 1000  # Max is 1000 for the free API.
    total_iterations = 5  # Number of times to repeat queries for diversity

    for pub in retrieve_crossref_publications(max_results_per_query=max_results_per_query, total_iterations=total_iterations):
        print(f"DOI: {pub['doi']}")
        print(f"Title: {pub['title']}")
        print(f"Summary: {pub['summary']}")
        print(f"Year: {pub['year']}")
        print(f"Source: {pub['source']}")
        print(f"Authors: {pub['authors']}")
        print('-' * 80)

if __name__ == "__main__":
    main()





import random
from scholarly import scholarly
import requests

def get_all(num_papers):
    for paper in google_query(round(num_papers)*1): # NOTE : Get weights to counteract any biases in the sources that worked.
        yield paper



# =========================== WEB OF SCIENCE ============================ #





# =============================== SCOPUS ================================ #




# =========================== GOOGLE SCHOLAR ============================ #

def google_scholar_papers(num_papers=2500):
    """ Retrieve papers from Google Scholar using a weighted random selection of queries. """
    queries_and_weights = [
        ("site:scholar.google.com physics OR theoretical physics OR experimental physics OR particle physics OR quantum mechanics OR condensed matter physics", 0.25),
        ("site:scholar.google.com chemistry OR organic chemistry OR inorganic chemistry OR physical chemistry OR analytical chemistry OR biochemistry OR materials science", 0.20),
        ("site:scholar.google.com biology OR molecular biology OR cellular biology OR genetics OR microbiology OR immunology OR neurobiology", 0.15),
        ("site:scholar.google.com earth science OR geology OR geophysics OR environmental science OR climate science OR oceanography", 0.10),
        ("site:scholar.google.com engineering OR mechanical engineering OR electrical engineering OR civil engineering OR chemical engineering OR materials engineering OR aerospace engineering", 0.10),
        ("site:scholar.google.com mathematics OR applied mathematics OR pure mathematics OR computer science OR computational science OR artificial intelligence", 0.10),
        ("site:scholar.google.com multidisciplinary science OR interdisciplinary research OR applied sciences OR scientific reviews OR technology and innovation", 0.10)
    ]
    queries = [query for query, weight in queries_and_weights for _ in range(int(weight * 100))]

    for _ in range(num_papers):
        search_query = random.choice(queries)

        search_results = scholarly.search_pubs(search_query)

        count = 1000
        for paper in search_results:
            count -= 1
            bib = paper.get('bib', {})
            yield {
                    'title': bib.get('title', 'No title available'),
                    'abstract': bib.get('abstract', 'No abstract available'),
                    'year': bib.get('pub_year', 'No year available'),
                    'authors': bib.get('author', 'No authors available')
                }
            if count <= 0:
                break


