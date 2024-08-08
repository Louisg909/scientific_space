from scholarly import scholarly
from scholarly import ProxyGenerator
import requests
from requests.exceptions import RequestException
import time

def scrape_author(author_name):
    print(f"DEBUG: Starting search for author: {author_name}")
    search_query = scholarly.search_author(author_name)
    author = None

    print("DEBUG: Iterating through search results...")
    try:
        for result in search_query:
            print(f"DEBUG: Found author: {result.get('name')}")
            if result.get('name').lower() == author_name.lower():
                print(f"DEBUG: Exact match found for author: {result.get('name')}")
                author = result
                break
    except RequestException as e:
        print(f"ERROR: An error occurred while searching for the author: {e}")
        return []

    if not author:
        print(f"No author found for name: {author_name}")
        return []

    print(f"DEBUG: Filling author details for {author_name}")
    try:
        author = scholarly.fill(author)
    except RequestException as e:
        print(f"ERROR: An error occurred while filling author details: {e}")
        return []

    papers = author.get('publications', [])
    
    result = []
    print(f"DEBUG: Found {len(papers)} publications for author {author_name}")
    for paper in papers:
        try:
            # Fill in the publication details to get the abstract
            paper = scholarly.fill(paper)
        except RequestException as e:
            print(f"ERROR: An error occurred while filling publication details: {e}")
            continue

        bib = paper.get('bib', {})
        title = bib.get('title', '')
        summary = bib.get('abstract', '')
        year = bib.get('pub_year', '')

        print(f'Title:\t{title}\nSummary:\t{summary}\nYear:\t{year}')
        
        if title and summary and year:
            result.append({
                'title': title,
                'summary': summary,
                'year': year
            })
    
    return result

    

if __name__ == "__main__":
    #author_name = input("Enter the author's name: ")
    #author_name = 'Albert Einstein'
    author_name = 'Jens Christian Claussen'
    print(f"DEBUG: Input author name: {author_name}")
    papers = scrape_author(author_name)
    for i, paper in enumerate(papers):
        print(f"Paper {i+1}:")
        print(f"Title: {paper['title']}")
        print(f"Summary: {paper['summary']}")
        print(f"Year: {paper['year']}\n")
