


def get_all(max_numb):
    for paper in get_jacs_papers(max_numb*1):
        yield paper



# ========== JOURNEY OF THE AMERICAN CHEMICAL SOCIETY (JACS) =========== #
# ================================= 4% ================================== #
# ======================= ERROR 403 - FORBIDDEN ======================== #


"""
#import requests
#from bs4 import BeautifulSoup
#import random
#import re
#import time
#
#BASE_URL = "https://pubs.acs.org"
#journal = "jacsat"
#
#def create_session():
#    session = requests.Session()
#    session.headers.update({
#        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
#    })
#    return session
#
#def get_largest_issue_id(session):
#    issues_url = f"{BASE_URL}/loi/{journal}"
#    print(f"Fetching issues list from URL: {issues_url}")
#    response = session.get(issues_url)
#    print(f"HTTP Status Code: {response.status_code}")
#    print(f"Response content length: {len(response.content)}")
#    
#    if response.status_code == 403:
#        print("Access forbidden. The server returned a 403 status code.")
#        return None
#
#    soup = BeautifulSoup(response.content, 'html.parser')
#    
#    issue_links_section = soup.find('div', class_='loi__issue')
#    if issue_links_section:
#        print("Found loi__issue div section.")
#    else:
#        print("Could not find loi__issue div section.")
#        return None
#
#    issue_links = issue_links_section.find_all('a', href=re.compile('/toc/jacsat/'))
#    print(f"Found {len(issue_links)} issue links.")
#    
#    issue_ids = [int(re.search(r'/toc/jacsat/(\d+)', link['href']).group(1)) for link in issue_links]
#    print(f"Issue IDs found: {issue_ids}")
#    
#    largest_id = max(issue_ids)
#    print(f"Largest issue ID found: {largest_id}")
#    return largest_id
#
#def get_random_issue_page(session, largest_id):
#    while True:
#        random_id = random.randint(1, largest_id)
#        random_issue_url = f"{BASE_URL}/toc/{journal}/{random_id}"
#        print(f"Trying to fetch issue page for random ID: {random_id} from URL: {random_issue_url}")
#        response = session.get(random_issue_url)
#        if response.status_code == 200:
#            print(f"Successfully fetched issue page for ID: {random_id}")
#            return response.content, random_id
#        time.sleep(random.uniform(1, 3))  # Adding delay to mimic human behavior
#
#def get_issue_list(html_content):
#    soup = BeautifulSoup(html_content, 'html.parser')
#    issue_div = soup.find('div', class_='issue-item')
#    if not issue_div:
#        print(f"No issue div found")
#        return None
#    
#    issue_list = issue_div.find_all('div', class_='issue-item')
#    if not issue_list:
#        print(f"No issues found in issue div")
#        return None
#    
#    print(f"Found {len(issue_list)} issues in the issue list")
#    return issue_list
#
#def get_random_paper_url(session, issue_list):
#    issue_url = BASE_URL + issue_list[random.randint(0, len(issue_list) - 1)].find('a')['href']
#    print(f"Trying to fetch issue page from URL: {issue_url}")
#    response = session.get(issue_url)
#    if response.status_code == 200:
#        print(f"Successfully fetched issue page from URL: {issue_url}")
#        return response.content, issue_url
#    else:
#        raise ValueError("Failed to fetch issue page.")
#
#def get_article_list(issue_html_content, issue_url):
#    print(f"Parsing article list from issue URL: {issue_url}")
#    soup = BeautifulSoup(issue_html_content, 'html.parser')
#    article_sections = soup.find_all('div', class_='issue-item_metadata')
#    if not article_sections:
#        print(f"Error: No articles found in the issue")
#        raise ValueError("No articles found in the issue")
#    
#    articles = []
#    for section in article_sections:
#        group_title_tag = section.find_previous('h2', class_='issue-heading')
#        if group_title_tag:
#            group_title = group_title_tag.text.strip()
#        else:
#            group_title = "Unknown"
#
#        article_link = section.find('a', class_='issue-item_title')['href']
#        articles.append((BASE_URL + article_link, group_title))
#    
#    print(f"Found {len(articles)} articles in the issue")
#    return articles
#
#def get_paper_details(html_content):
#    print(f"Parsing paper details...")
#    soup = BeautifulSoup(html_content, 'html.parser')
#    paper_details = {}
#
#    main_div = soup.find('div', class_='hlFld-Title')
#    if not main_div:
#        print(f"Error: No main content div found")
#        raise ValueError("No main content div found")
#
#    title_tag = main_div.find('h1', class_='article-header_title')
#    if not title_tag:
#        print(f"Error: No title found")
#        raise ValueError("No title found")
#    paper_details['title'] = title_tag.text.strip()
#
#    authors_tag = main_div.find('div', class_='loa-info')
#    if not authors_tag:
#        print(f"Error: No authors found")
#        raise ValueError("No authors found")
#    paper_details['authors'] = ", ".join(author.text.strip() for author in authors_tag.find_all('a'))
#
#    pub_info_tag = main_div.find('div', class_='epubdate')
#    if not pub_info_tag:
#        print(f"Error: No publication info found")
#        raise ValueError("No publication info found")
#    pub_info_text = pub_info_tag.text.strip()
#    year_match = re.search(r'\d{4}', pub_info_text)
#    paper_details['year'] = year_match.group(0) if year_match else "Unknown"
#
#    abstract_div = soup.find('div', class_='abstractSection')
#    if not abstract_div:
#        print(f"Error: No abstract found")
#        raise ValueError("No abstract found")
#    abstract_paragraph = abstract_div.find('p')
#    abstract_text = ' '.join(abstract_paragraph.stripped_strings)
#    abstract_text = re.sub(r'<span>[^<]*</span>', '{equation}', abstract_text)
#    paper_details['summary'] = abstract_text.strip()
#
#    print(f"Parsed paper details successfully")
#    return paper_details
#
#def get_jacs_papers(numb_papers):
#    session = create_session()
#    largest_id = get_largest_issue_id(session)
#    if largest_id is None:
#        print("Failed to find the largest issue ID.")
#        return
#    
#    articles_collected = 0
#    while articles_collected < numb_papers:
#        html_content, random_id = get_random_issue_page(session, largest_id)
#        issue_list = get_issue_list(html_content)
#
#        if issue_list:
#            issue_html_content, issue_url = get_random_paper_url(session, issue_list)
#            article_list = get_article_list(issue_html_content, issue_url)
#            
#            for article_url, group_title in article_list:
#                if articles_collected >= numb_papers:
#                    break
#                paper_html_content = session.get(article_url).content
#                paper_details = get_paper_details(paper_html_content)
#                paper_details['subtitle'] = group_title
#                paper_details['source'] = 'acs-jacs'
#                yield paper_details
#                articles_collected += 1
#
#if __name__ == "__main__":
#    numb_papers = 5
#
#    print("\nTesting get_largest_issue_id()")
#    session = create_session()
#    largest_id = get_largest_issue_id(session)
#    if largest_id is not None:
#        print(f"Largest ID: {largest_id}")
#
#    print("\nTesting get_random_issue_page()")
#    if largest_id is not None:
#        issue_page_content, random_id = get_random_issue_page(session, largest_id)
#        print(f"Random ID: {random_id}")
#        print(f"Content length: {len(issue_page_content)}")
#
#        print("\nTesting get_issue_list()")
#        issue_list = get_issue_list(issue_page_content)
#        if issue_list:
#            print(f"Found {len(issue_list)} issues")
#
#            print("\nTesting get_random_paper_url()")
#            if issue_list:
#                issue_html_content, issue_url = get_random_paper_url(session, issue_list)
#                print(f"Issue URL: {issue_url}")
#                print(f"Issue page content length: {len(issue_html_content)}")
#
#                print("\nTesting get_article_list()")
#                if issue_html_content:
#                    article_list = get_article_list(issue_html_content, issue_url)
#                    print(f"Found {len(article_list)} articles")
#
#                    print("\nTesting get_paper_details()")
#                    if article_list:
#                        article_url, group_title = article_list[0]
#                        print(f"Fetching article from URL: {article_url}")
#                        paper_html_content = session.get(article_url).content
#                        paper_details = get_paper_details(paper_html_content)
#                        paper_details['subtitle'] = group_title
#                        print(paper_details)
#
#    print("\nTesting get_jacs_papers()")
#    for paper in get_jacs_papers(numb_papers):
#        print(paper)
#
"""












# ========================= ANGEWANDTE CHEMIE ========================== #
# ================================= 3% ================================== #
# ======================= ERROR 403 - FORBIDDEN ======================== #
#
#"""
#import requests
#from bs4 import BeautifulSoup
#import random
#import re
#import time
#
#BASE_URL = "https://onlinelibrary.wiley.com"
#journal = "an"
#
#def create_session():
#    session = requests.Session()
#    session.headers.update({
#        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
#    })
#    return session
#
#def get_largest_issue_id(session):
#    issues_url = f"{BASE_URL}/loi/{journal}"
#    print(f"Fetching issues list from URL: {issues_url}")
#    response = session.get(issues_url)
#    print(f"HTTP Status Code: {response.status_code}")
#    print(f"Response content length: {len(response.content)}")
#    
#    if response.status_code != 200:
#        print("Failed to access the issues list page.")
#        return None
#
#    soup = BeautifulSoup(response.content, 'html.parser')
#    
#    issue_links_section = soup.find_all('a', href=re.compile(f'/toc/{journal}/'))
#    if issue_links_section:
#        print("Found issue links section.")
#    else:
#        print("Could not find issue links section.")
#        return None
#
#    issue_ids = [int(re.search(r'/toc/an/(\d+)', link['href']).group(1)) for link in issue_links_section]
#    print(f"Issue IDs found: {issue_ids}")
#    
#    largest_id = max(issue_ids)
#    print(f"Largest issue ID found: {largest_id}")
#    return largest_id
#
#def get_random_issue_page(session, largest_id):
#    while True:
#        random_id = random.randint(1, largest_id)
#        random_issue_url = f"{BASE_URL}/toc/{journal}/{random_id}"
#        print(f"Trying to fetch issue page for random ID: {random_id} from URL: {random_issue_url}")
#        response = session.get(random_issue_url)
#        if response.status_code == 200:
#            print(f"Successfully fetched issue page for ID: {random_id}")
#            return response.content, random_id
#        time.sleep(random.uniform(1, 3))  # Adding delay to mimic human behavior
#
#def get_issue_list(html_content):
#    soup = BeautifulSoup(html_content, 'html.parser')
#    issue_div = soup.find_all('div', class_='issue-item')
#    if not issue_div:
#        print(f"No issue div found")
#        return None
#    
#    print(f"Found {len(issue_div)} issues in the issue list")
#    return issue_div
#
#def get_random_paper_url(session, issue_list):
#    issue_url = BASE_URL + issue_list[random.randint(0, len(issue_list) - 1)].find('a')['href']
#    print(f"Trying to fetch issue page from URL: {issue_url}")
#    response = session.get(issue_url)
#    if response.status_code == 200:
#        print(f"Successfully fetched issue page from URL: {issue_url}")
#        return response.content, issue_url
#    else:
#        raise ValueError("Failed to fetch issue page.")
#
#def get_article_list(issue_html_content, issue_url):
#    print(f"Parsing article list from issue URL: {issue_url}")
#    soup = BeautifulSoup(issue_html_content, 'html.parser')
#    article_sections = soup.find_all('div', class_='issue-item_metadata')
#    if not article_sections:
#        print(f"Error: No articles found in the issue")
#        raise ValueError("No articles found in the issue")
#    
#    articles = []
#    for section in article_sections:
#        group_title_tag = section.find_previous('h2', class_='issue-heading')
#        if group_title_tag:
#            group_title = group_title_tag.text.strip()
#        else:
#            group_title = "Unknown"
#
#        article_link = section.find('a', class_='issue-item_title')['href']
#        articles.append((BASE_URL + article_link, group_title))
#    
#    print(f"Found {len(articles)} articles in the issue")
#    return articles
#
#def get_paper_details(html_content):
#    print(f"Parsing paper details...")
#    soup = BeautifulSoup(html_content, 'html.parser')
#    paper_details = {}
#
#    main_div = soup.find('div', class_='hlFld-Title')
#    if not main_div:
#        print(f"Error: No main content div found")
#        raise ValueError("No main content div found")
#
#    title_tag = main_div.find('h1', class_='article-header_title')
#    if not title_tag:
#        print(f"Error: No title found")
#        raise ValueError("No title found")
#    paper_details['title'] = title_tag.text.strip()
#
#    authors_tag = main_div.find('div', class_='loa-info')
#    if not authors_tag:
#        print(f"Error: No authors found")
#        raise ValueError("No authors found")
#    paper_details['authors'] = ", ".join(author.text.strip() for author in authors_tag.find_all('a'))
#
#    pub_info_tag = main_div.find('div', class_='epubdate')
#    if not pub_info_tag:
#        print(f"Error: No publication info found")
#        raise ValueError("No publication info found")
#    pub_info_text = pub_info_tag.text.strip()
#    year_match = re.search(r'\d{4}', pub_info_text)
#    paper_details['year'] = year_match.group(0) if year_match else "Unknown"
#
#    abstract_div = soup.find('div', class_='abstractSection')
#    if not abstract_div:
#        print(f"Error: No abstract found")
#        raise ValueError("No abstract found")
#    abstract_paragraph = abstract_div.find('p')
#    abstract_text = ' '.join(abstract_paragraph.stripped_strings)
#    abstract_text = re.sub(r'<span>[^<]*</span>', '{equation}', abstract_text)
#    paper_details['summary'] = abstract_text.strip()
#
#    print(f"Parsed paper details successfully")
#    return paper_details
#
#def get_jacs_papers(numb_papers):
#    session = create_session()
#    largest_id = get_largest_issue_id(session)
#    if largest_id is None:
#        print("Failed to find the largest issue ID.")
#        return
#    
#    articles_collected = 0
#    while articles_collected < numb_papers:
#        html_content, random_id = get_random_issue_page(session, largest_id)
#        issue_list = get_issue_list(html_content)
#
#        if issue_list:
#            issue_html_content, issue_url = get_random_paper_url(session, issue_list)
#            article_list = get_article_list(issue_html_content, issue_url)
#            
#            for article_url, group_title in article_list:
#                if articles_collected >= numb_papers:
#                    break
#                paper_html_content = session.get(article_url).content
#                paper_details = get_paper_details(paper_html_content)
#                paper_details['subtitle'] = group_title
#                paper_details['source'] = 'ange-chem'
#                yield paper_details
#                articles_collected += 1
#
#if __name__ == "__main__":
#    numb_papers = 5
#
#    print("\nTesting get_largest_issue_id()")
#    session = create_session()
#    largest_id = get_largest_issue_id(session)
#    if largest_id is not None:
#        print(f"Largest ID: {largest_id}")
#
#    print("\nTesting get_random_issue_page()")
#    if largest_id is not None:
#        issue_page_content, random_id = get_random_issue_page(session, largest_id)
#        print(f"Random ID: {random_id}")
#        print(f"Content length: {len(issue_page_content)}")
#
#        print("\nTesting get_issue_list()")
#        issue_list = get_issue_list(issue_page_content)
#        if issue_list:
#            print(f"Found {len(issue_list)} issues")
#
#            print("\nTesting get_random_paper_url()")
#            if issue_list:
#                issue_html_content, issue_url = get_random_paper_url(session, issue_list)
#                print(f"Issue URL: {issue_url}")
#                print(f"Issue page content length: {len(issue_html_content)}")
#
#                print("\nTesting get_article_list()")
#                if issue_html_content:
#                    article_list = get_article_list(issue_html_content, issue_url)
#                    print(f"Found {len(article_list)} articles")
#
#                    print("\nTesting get_paper_details()")
#                    if article_list:
#                        article_url, group_title = article_list[0]
#                        print(f"Fetching article from URL: {article_url}")
#                        paper_html_content = session.get(article_url).content
#                        paper_details = get_paper_details(paper_html_content)
#                        paper_details['subtitle'] = group_title
#                        print(paper_details)
#
#    print("\nTesting get_jacs_papers()")
#    for paper in get_jacs_papers(numb_papers):
#        print(paper)
#"""

# ========================== CHEMICAL SCIENCE =========================== #
# ================================= 2% ================================== #


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
    print(f"Fetching issues list from URL: {issues_url}")
    response = session.get(issues_url)
    print(f"HTTP Status Code: {response.status_code}")
    print(f"Response content length: {len(response.content)}")
    
    if response.status_code != 200:
        print("Failed to access the issues list page.")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    
    issue_links_section = soup.find('div', class_='cards-list')
    if issue_links_section:
        print("Found issue links section.")
    else:
        print("Could not find issue links section.")
        return None

    issue_links = issue_links_section.find_all('a', href=re.compile(f'/en/journals/issue/\d+'))
    if not issue_links:
        print("Could not find any issue links.")
        return None

    issue_ids = [int(re.search(r'/issue/(\d+)', link['href']).group(1)) for link in issue_links]
    print(f"Issue IDs found: {issue_ids}")
    
    largest_id = max(issue_ids)
    print(f"Largest issue ID found: {largest_id}")
    return largest_id

def get_random_issue_page(session, largest_id):
    while True:
        random_id = random.randint(1, largest_id)
        random_issue_url = f"{BASE_URL}/en/journals/{journal}/issue/{random_id}"
        print(f"Trying to fetch issue page for random ID: {random_id} from URL: {random_issue_url}")
        response = session.get(random_issue_url)
        if response.status_code == 200:
            print(f"Successfully fetched issue page for ID: {random_id}")
            return response.content, random_id
        time.sleep(random.uniform(1, 3))  # Adding delay to mimic human behavior

def get_issue_list(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    issue_div = soup.find_all('div', class_='issue-item')
    if not issue_div:
        print(f"No issue div found")
        return None
    
    print(f"Found {len(issue_div)} issues in the issue list")
    return issue_div

def get_random_paper_url(session, issue_list):
    issue_url = BASE_URL + issue_list[random.randint(0, len(issue_list) - 1)].find('a')['href']
    print(f"Trying to fetch issue page from URL: {issue_url}")
    response = session.get(issue_url)
    if response.status_code == 200:
        print(f"Successfully fetched issue page from URL: {issue_url}")
        return response.content, issue_url
    else:
        raise ValueError("Failed to fetch issue page.")

def get_article_list(issue_html_content, issue_url):
    print(f"Parsing article list from issue URL: {issue_url}")
    soup = BeautifulSoup(issue_html_content, 'html.parser')
    article_sections = soup.find_all('div', class_='issue-item')
    if not article_sections:
        print(f"Error: No articles found in the issue")
        raise ValueError("No articles found in the issue")
    
    articles = []
    for section in article_sections:
        group_title_tag = section.find_previous('h2', class_='issue-heading')
        if group_title_tag:
            group_title = group_title_tag.text.strip()
        else:
            group_title = "Unknown"

        article_link = section.find('a', class_='issue-item_title')['href']
        articles.append((BASE_URL + article_link, group_title))
    
    print(f"Found {len(articles)} articles in the issue")
    return articles

def get_paper_details(html_content):
    print(f"Parsing paper details...")
    soup = BeautifulSoup(html_content, 'html.parser')
    paper_details = {}

    main_div = soup.find('div', class_='article-header')
    if not main_div:
        print(f"Error: No main content div found")
        raise ValueError("No main content div found")

    title_tag = main_div.find('h1', class_='title')
    if not title_tag:
        print(f"Error: No title found")
        raise ValueError("No title found")
    paper_details['title'] = title_tag.text.strip()

    authors_tag = main_div.find('ul', class_='authors')
    if not authors_tag:
        print(f"Error: No authors found")
        raise ValueError("No authors found")
    paper_details['authors'] = ", ".join(author.text.strip() for author in authors_tag.find_all('a'))

    pub_info_tag = main_div.find('span', class_='pub-date')
    if not pub_info_tag:
        print(f"Error: No publication info found")
        raise ValueError("No publication info found")
    pub_info_text = pub_info_tag.text.strip()
    year_match = re.search(r'\d{4}', pub_info_text)
    paper_details['year'] = year_match.group(0) if year_match else "Unknown"

    abstract_div = soup.find('div', class_='abstract')
    if not abstract_div:
        print(f"Error: No abstract found")
        raise ValueError("No abstract found")
    abstract_paragraph = abstract_div.find('p')
    abstract_text = ' '.join(abstract_paragraph.stripped_strings)
    abstract_text = re.sub(r'<span>[^<]*</span>', '{equation}', abstract_text)
    paper_details['summary'] = abstract_text.strip()

    print(f"Parsed paper details successfully")
    return paper_details

def get_chemical_science_papers(numb_papers):
    session = create_session()
    largest_id = get_largest_issue_id(session)
    if largest_id is None:
        print("Failed to find the largest issue ID.")
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
                paper_details['source'] = 'chem-sci'
                yield paper_details
                articles_collected += 1

if __name__ == "__main__":
    numb_papers = 5

    print("\nTesting get_largest_issue_id()")
    session = create_session()
    largest_id = get_largest_issue_id(session)
    if largest_id is not None:
        print(f"Largest ID: {largest_id}")

    print("\nTesting get_random_issue_page()")
    if largest_id is not None:
        issue_page_content, random_id = get_random_issue_page(session, largest_id)
        print(f"Random ID: {random_id}")
        print(f"Content length: {len(issue_page_content)}")

        print("\nTesting get_issue_list()")
        issue_list = get_issue_list(issue_page_content)
        if issue_list:
            print(f"Found {len(issue_list)} issues")

            print("\nTesting get_random_paper_url()")
            if issue_list:
                issue_html_content, issue_url = get_random_paper_url(session, issue_list)
                print(f"Issue URL: {issue_url}")
                print(f"Issue page content length: {len(issue_html_content)}")

                print("\nTesting get_article_list()")
                if issue_html_content:
                    article_list = get_article_list(issue_html_content, issue_url)
                    print(f"Found {len(article_list)} articles")

                    print("\nTesting get_paper_details()")
                    if article_list:
                        article_url, group_title = article_list[0]
                        print(f"Fetching article from URL: {article_url}")
                        paper_html_content = session.get(article_url).content
                        paper_details = get_paper_details(paper_html_content)
                        paper_details['subtitle'] = group_title
                        print(paper_details)

    print("\nTesting get_chemical_science_papers()")
    for paper in get_chemical_science_papers(numb_papers):
        print(paper)






# ================== ROYAL SOCIETY OF CHEMISTRY (RSC) =================== #
#import sys
#import os
#
## Add the submodule path to sys.path
#submodule_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../paper_scraper/paperscraper/'))
#if submodule_path not in sys.path:
#    sys.path.insert(0, submodule_path)
#
#from paper_scraper.paperscraper import PaperScraper






























