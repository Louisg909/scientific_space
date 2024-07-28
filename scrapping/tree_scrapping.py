import time
import requests
import sqlite3

import commands as pm

#TODO - add scraper that takes depth and number of starting papers - randomly scrapes for those starting papers and then does the depth scrape for each of those papers.

sleep_timer = 0.5 # 1 second

def get_paper_details(paper_id):
    url = f'https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=title,abstract,references'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve paper {paper_id}")
        return None

def paper_in_db(paper_details) -> bool:
    title = paper_details.get('title', 'No title available')
    abstract = paper_details.get('abstract', 'No abstract available')
    authors = [author.get('name') for author in paper_details.get('authors', [])]
    year = paper_details.get('year', 'No year available')
    categories = paper_details.get('fieldsOfStudy', [None])[0]

    result = pm.grab('papers', select='*', where=(['title', 'summary', 'year'], [title, abstract, year]))
    if result:
        return result[0]
    return False

def add_paper_db(paper_details) -> int:
    title = paper_details.get('title', 'No title available')
    abstract = paper_details.get('abstract', 'No abstract available')
    authors = ", ".join([author.get('name') for author in paper_details.get('authors', [])])
    year = paper_details.get('year', 'No year available')
    categories = paper_details.get('fieldsOfStudy', [None])[0]
    embedding = None  # Assuming embedding is not provided in paper_details

    pm.insert('papers', (title, abstract, authors, year, categories, embedding))

    return paper_in_db(paper_details)

def add_reference_db(parent_id: int, child_id: int) -> None:
    if child_id is None:
        return  # Skip if child_id is None
    conn = sqlite3.connect('science_papers.db')
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO [references] (parent_id, child_id)
            VALUES (?, ?)
        ''', (parent_id, child_id))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(e)
    finally:
        conn.close()

def build_citation_tree(paper_id, depth=2) -> int:  # returns paper's id so can be added to child-parent database
    print(paper_id)
    global sleep_timer
    time.sleep(sleep_timer)

    if depth == 0:
        return None
    
    paper_details = get_paper_details(paper_id)

    if not paper_details:
        return None

    cheese = paper_in_db(paper_details)
    if cheese:
        return cheese

    db_paper_id = add_paper_db(paper_details)

    references_scraped = paper_details.get('references', [])
    if len(references_scraped) < 10:
        references_scraped[:10]
    print(references_scraped)

    for ref in references_scraped:
        ref_id = ref.get('paperId')
        if ref_id:
            ref_db_id = build_citation_tree(ref_id, depth = depth-1)
            if ref_db_id:  # Ensure ref_db_id is valid
                add_reference_db(db_paper_id, ref_db_id)

    return db_paper_id

if __name__ == '__main__':
    # Example usage
    source_paper_id = 'arXiv:2203.08567'  # Replace with your source paper ID
    citation_tree = build_citation_tree(source_paper_id, depth=3)
