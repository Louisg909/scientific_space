import requests
from bs4 import BeautifulSoup
import random
import re


def get_all(max_numb):
    for paper in get_aps_papers(max_numb*1):
        yield paper


# =================== physical review journal (aps) ==================== #
# ================================= 5% ================================== #

"""
Notes

Note - may have some bias of old research.... try to counter-act this somehow.

- Go to journal page issues at https://journals.aps.org/prlissues
- Gett largest h4 id -->    <h4 id="v133">
- Find random number from 1 to largest id (inclusvie)
- https://journals.aps.org/prl/issues/{random_a}#v{random_a}
- Find div that includes the id on the website --> <div class="volume-issue-list"> <h4 id="v{id_number}"> ... </h4> <ul> <li> (list of issues to pick from)
- Pick one of those issues and go to the page href (relative)
- pick a random html button (takes me to a paper - think about whether to just use papers or use everything?
- Get title, abstract, authors, year of publication. etc  - LATEX NEEDS FORMATTINGGGGGG :((((""" # TODO find way to get latex from their funny code
"""
In class="medium-9 columns", <h3> is the title, <h5 class="authors"> is authors, <h5 class ="pub-info"> is information including the year of publication (last 4 non-whitespace chars).
In <div class=content">, the abstract is under <p> - includes <span> elements for latex that should just be replaced with "{equation}".

"""

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

def get_aps_papers(numb_papers):
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
            
            for article_url, group_title in article_list:
                if articles_collected >= numb_papers:
                    break
                paper_html_content = requests.get(article_url).content
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










# ===================== JOURNAL OF APPLIED PHYSICS ====================== #
# ================================= 2% ================================== #




# =============== JOURNAL OF HIGH ENERGY PHYSICS (JHEP) ================ #
# ================================= 2% ================================== #























