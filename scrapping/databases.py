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





# ========================== SEMANTIC SCHOLAR =========================== #




def semantic_scholar_papers(api_key, num_papers=10):
    """ Retrieve random papers from Semantic Scholar using the API. """
    url = 'https://api.semanticscholar.org/graph/v1/paper/search'
    headers = {'x-api-key': api_key} # TODO try to get API key
    
    query_params = {
        'query': 'random',  
        'limit': num_papers
    }
    
    response = requests.get(url, params=query_params, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        for paper in response_data.get('data', []):
            yield {
                    'title' : paper.get('title', 'N/A'),
                    'abstract' : paper.get('abstract', 'N/A'),
                    'year' : paper.get('year', 'N/A'),
                    'primary_category' : paper.get('fieldsOfStudy', ['N/A'])[0]
                    }
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")













