import requests
from bs4 import BeautifulSoup
import random
import re
import time

BASE_URL = "https://pubs.rsc.org"
journal = "sc"

def create_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    })
    return session

def get_largest_issue_id(session):
    issues_url = f"{BASE_URL}/en/journals/journalissues/{journal}"
    response = session.get(issues_url)
    
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    issue_links_section = soup.find('div', class_='cards-list')

    if not issue_links_section:
        return None

    issue_links = issue_links_section.find_all('a', href=re.compile(f'/en/journals/issue/\\d+'))
    if not issue_links:
        return None

    issue_ids = [int(re.search(r'/issue/(\d+)', link['href']).group(1)) for link in issue_links]
    return max(issue_ids)

def get_random_issue_page(session, largest_id):
    while True:
        random_id = random.randint(1, largest_id)
        random_issue_url = f"{BASE_URL}/en/journals/{journal}/issue/{random_id}"
        response = session.get(random_issue_url)
        if response.status_code == 200:
            return response.content, random_id
        time.sleep(random.uniform(1, 3))  # Adding delay to mimic human behavior

def get_issue_list(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.find_all('div', class_='issue-item')

def get_random_paper_url(session, issue_list):
    issue_url = BASE_URL + issue_list[random.randint(0, len(issue_list) - 1)].find('a')['href']
    response = session.get(issue_url)
    if response.status_code == 200:
        return response.content, issue_url
    raise ValueError("Failed to fetch issue page.")

def get_article_list(issue_html_content, issue_url):
    soup = BeautifulSoup(issue_html_content, 'html.parser')
    article_sections = soup.find_all('div', class_='issue-item')
    if not article_sections:
        raise ValueError("No articles found in the issue")
    
    articles = []
    for section in article_sections:
        group_title_tag = section.find_previous('h2', class_='issue-heading')
        group_title = group_title_tag.text.strip() if group_title_tag else "Unknown"
        article_link = section.find('a', class_='issue-item_title')['href']
        articles.append((BASE_URL + article_link, group_title))
    
    return articles

def get_paper_details(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    paper_details = {}

    main_div = soup.find('div', class_='article-header')
    if not main_div:
        raise ValueError("No main content div found")

    title_tag = main_div.find('h1', class_='title')
    if not title_tag:
        raise ValueError("No title found")
    paper_details['title'] = title_tag.text.strip()

    authors_tag = main_div.find('ul', class_='authors')
    if not authors_tag:
        raise ValueError("No authors found")
    paper_details['authors'] = ", ".join(author.text.strip() for author in authors_tag.find_all('a'))

    pub_info_tag = main_div.find('span', class_='pub-date')
    year_match = re.search(r'\d{4}', pub_info_tag.text.strip() if pub_info_tag else '')
    paper_details['year'] = year_match.group(0) if year_match else "Unknown"

    abstract_div = soup.find('div', class_='abstract')
    if not abstract_div:
        raise ValueError("No abstract found")
    abstract_paragraph = abstract_div.find('p')
    abstract_text = ' '.join(abstract_paragraph.stripped_strings)
    abstract_text = re.sub(r'<span>[^<]*</span>', '{equation}', abstract_text)
    paper_details['summary'] = abstract_text.strip()

    return paper_details

def get_chemical_science_papers(numb_papers):
    session = create_session()
    largest_id = get_largest_issue_id(session)
    if largest_id is None:
        return
    
    articles_collected = 0
    while articles_collected < numb_papers:
        html_content, random_id = get_random_issue_page(session, largest_id)
        issue_list = get_issue_list(html_content)

        if issue_list:
            issue_html_content, issue_url = get_random_paper_url(session, issue_list)
            article_list = get_article_list(issue_html_content, issue_url)
            
            for article_url, group_title in article_list:
                if articles_collected >= numb_papers:
                    break
                paper_html_content = session.get(article_url).content
                paper_details = get_paper_details(paper_html_content)
                paper_details['subtitle'] = group_title
                paper_details['source'] = 'chem'
                yield paper_details
                articles_collected += 1

if __name__ == "__main__":
    numb_papers = 5

    for paper in get_chemical_science_papers(numb_papers):
        print(paper)
