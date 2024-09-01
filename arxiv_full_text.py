
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
