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
