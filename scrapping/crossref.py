from crossref_commons.iteration import iterate_publications_as_json
import random
import time

def extract_metadata(data):
    title = data.get('title', [''])[0]
    abstract = data.get('abstract', '')
    publication_year = data.get('published-print', {}).get('date-parts', [[None]])[0][0]
    source = data.get('container-title', [''])[0]
    authors = [f"{author.get('given', '')} {author.get('family', '')}" for author in data.get('author', [])]
    return {
        'doi': data.get('DOI', ''),
        'title': title,
        'summary': abstract,
        'year': publication_year,
        'source': source,
        'authors': ', '.join(authors)
    }

def retrieve_publications_with_metadata(max_results_per_query=1000, total_iterations=5):
    max_results_per_query = min(1000, max_results_per_query)

    request_buffer = 1  # Minimum number of seconds between each request
    timer = 0
    filter = {
        'type': 'journal-article',  # Focus on journal articles
        'has-abstract': 'true',     # Ensure we get publications with abstracts
    }

    queries_list = [
        # General Science Fields
        'science OR technology OR biology OR physics OR chemistry OR engineering OR geology OR environmental OR mathematics OR neuroscience OR astronomy OR computer science',
        # High-Impact Journals
        'Nature', 'Science', 'PNAS', 'PLOS', 'Physical Review', 'Journal of Applied Physics', 'Journal of High Energy Physics', 'Journal of the American Chemical Society', 'Angewandte Chemie', 'Chemical Science', 'Journal of Biological Chemistry', 'Cell', 'Journal of Experimental Biology', 'Geophysical Research Letters', 'Journal of Geophysical Research', 'Environmental Science & Technology', 'Nature Communications', 'Science Advances', 'Journal of Interdisciplinary Science Topics',
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
    total_retrieved = 0

    total_papers = int(max_results_per_query / max(query_weights))

    for iteration in range(total_iterations):
        print(f"Starting iteration {iteration + 1}/{total_iterations}")
        for query, weight in zip(queries_list, query_weights):
            print(f"Making a request with query: {query}")

            # Request with buffering to be polite (but also take advantage of any time spent doing other things)
            delta_time = request_buffer - (time.time() - timer)
            if delta_time > 0:
                time.sleep(delta_time)
            new_publications = list(iterate_publications_as_json(max_results=int(total_papers * weight), filter=filter, queries={'query': query}))
            timer = time.time()

            for publication in new_publications:
                doi = publication['DOI']
                if doi not in processed_dois:  # Skip already processed DOIs
                    extracted_data = extract_metadata(publication)
                    processed_dois.add(doi)
                    yield extracted_data

            total_retrieved += len(new_publications)
            print(f"Retrieved {total_retrieved} publications so far...")

def main():
    max_results_per_query = 1000  # Number of results per query iteration - max is 1000 for the free API.
    total_iterations = 5  # Number of times to repeat queries for diversity

    for pub in retrieve_publications_with_metadata(max_results_per_query=max_results_per_query, total_iterations=total_iterations):
        print(f"DOI: {pub['doi']}")
        print(f"Title: {pub['title']}")
        print(f"Summary: {pub['summary']}")
        print(f"Year: {pub['year']}")
        print(f"Source: {pub['source']}")
        print(f"Authors: {pub['authors']}")
        print('-' * 80)

if __name__ == "__main__":
    main()
