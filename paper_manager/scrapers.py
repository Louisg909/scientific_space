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

