

def get_all(num_papers):
    for paper in google_query(round(num_papers)*1): # NOTE : Get weights to counteract any biases in the sources that worked.
        yield paper



# =========================== WEB OF SCIENCE ============================ #





# =============================== SCOPUS ================================ #




# =========================== GOOGLE SCHOLAR ============================ #
# ============================= COMPLETED ============================== #

import random
from scholarly import scholarly

def google_query(num_papers=10):
    # Define search queries and weights for hard science fields
    queries_and_weights = [
        ("site:scholar.google.com physics OR theoretical physics OR experimental physics OR particle physics OR quantum mechanics OR condensed matter physics", 0.25),
        ("site:scholar.google.com chemistry OR organic chemistry OR inorganic chemistry OR physical chemistry OR analytical chemistry OR biochemistry OR materials science", 0.20),
        ("site:scholar.google.com biology OR molecular biology OR cellular biology OR genetics OR microbiology OR immunology OR neurobiology", 0.15),
        ("site:scholar.google.com earth science OR geology OR geophysics OR environmental science OR climate science OR oceanography", 0.10),
        ("site:scholar.google.com engineering OR mechanical engineering OR electrical engineering OR civil engineering OR chemical engineering OR materials engineering OR aerospace engineering", 0.10),
        ("site:scholar.google.com mathematics OR applied mathematics OR pure mathematics OR computer science OR computational science OR artificial intelligence", 0.10),
        ("site:scholar.google.com multidisciplinary science OR interdisciplinary research OR applied sciences OR scientific reviews OR technology and innovation", 0.10)
    ]

    

    # Weighted selection of queries
    queries = [query for query, weight in queries_and_weights for _ in range(int(weight * 100))]

    for _ in range(num_papers):
        search_query = random.choice(queries)
        search_results = scholarly.search_pubs(search_query)

        try:
            paper = next(search_results)
            bib = paper.get('bib', {})
            yield { 'title': bib.get('title', 'No title available'),
                'abstract': bib.get('abstract', 'No abstract available'),
                'year': bib.get('pub_year', 'No year available'),
                'authors': bib.get('author', 'No authors available')
                }
        except StopIteration:
            continue


if __name__ == "__main__":
    random_papers = google_get_papers(10)
    for i, paper in enumerate(random_papers):
        print(f"Paper {i+1}:")
        print(f"Title: {paper['title']}")
        print(f"Abstract: {paper['abstract']}")
        print(f"Year: {paper['year']}")
        print(f"Authors: {paper['authors']}\n")



# ========================== SEMANTIC SCHOLAR =========================== #



import requests
import random

def semantic(): # FIXME
    # Define the API endpoint URL
    url = 'https://api.semanticscholar.org/graph/v1/paper/search'
    
    # Define your API key
    api_key = 'your_api_key_here'
    
    # Define headers with API key
    headers = {'x-api-key': api_key}
    
    # Define query parameters for random papers
    query_params = {
        'query': 'random',  # Adjust this query as needed
        'limit': 10  # Number of papers to retrieve
    }
    
    # Send the API request
    response = requests.get(url, params=query_params)# , headers=headers)
    
    # Check response status
    if response.status_code == 200:
        response_data = response.json()
        for paper in response_data['data']:
            title = paper.get('title', 'N/A')
            abstract = paper.get('abstract', 'N/A')
            year = paper.get('year', 'N/A')
            primary_category = paper.get('fieldsOfStudy', ['N/A'])[0]
            print(f"Title: {title}\nAbstract: {abstract}\nYear: {year}\nPrimary Category: {primary_category}\n")
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")



















