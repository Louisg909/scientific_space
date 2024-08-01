

# ========================== CATEGORY == 35% =========================== #

def get_all():
    yield



# =============================== NATURE ================================ #
# =============================== 37.5% ================================ #
# ================================ API ================================= #



# ============================ SCIENCE AAAS ============================= #
# ================================ 25% ================================= #
# ============================ WEB SCRAPING ============================= #
# XXX XXX FIXME FIXME XXX XXX FIXME FIXME FIXME XXX XXX FIXME FIXME XXX XXX


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import random
import time

def aaas_get_random_article_urls(count=10):
    """
    Function to get random article URLs from the Science | AAAS website using Selenium.
    """
    url = "https://www.science.org/journals"
    
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    driver_path = './chromedriver.exe'  # Path to your chromedriver.exe
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    # Access the page
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    
    # Print the page source for debugging
    print(driver.page_source)
    
    # Find all article links
    article_links = driver.find_elements(By.XPATH, '//a[contains(@href, "/doi/") and contains(@href, "science")]')
    print(f"Found {len(article_links)} article links")
    
    if not article_links:
        print("No article links found.")
        driver.quit()
        return []
    
    # Check if there are enough links to sample
    if len(article_links) < count:
        count = len(article_links)
    
    random_links = random.sample(article_links, count)
    article_urls = ["https://www.science.org" + link.get_attribute('href') for link in random_links]
    
    driver.quit()
    return article_urls

def aaas_get_article_details(url):
    """
    Function to scrape details from an article page using Selenium.
    """
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    driver_path = './chromedriver.exe'  # Path to your chromedriver.exe
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    # Access the page
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    
    title = driver.find_element(By.CLASS_NAME, 'article__headline').text.strip() if driver.find_elements(By.CLASS_NAME, 'article__headline') else 'N/A'
    summary = driver.find_element(By.CLASS_NAME, 'article__body').text.strip() if driver.find_elements(By.CLASS_NAME, 'article__body') else 'N/A'
    year = driver.find_element(By.CLASS_NAME, 'pub-date').get_attribute('datetime')[:4] if driver.find_elements(By.CLASS_NAME, 'pub-date') else 'N/A'
    category = driver.find_element(By.CLASS_NAME, 'article__category').text.strip() if driver.find_elements(By.CLASS_NAME, 'article__category') else 'N/A'
    
    driver.quit()
    
    return {
        'title': title,
        'summary': summary,
        'year': year,
        'category': category
    }

def aaas_random_papers_generator(count=10):
    """
    Generator function to yield random papers with details.
    """
    article_urls = aaas_get_random_article_urls(count)
    
    if not article_urls:
        print("No article URLs to process.")
        return
    
    for url in article_urls:
        article_details = aaas_get_article_details(url)
        if article_details:
            yield article_details

# Example usage
if __name__ == "__main__":
    for paper in aaas_random_papers_generator(5):
        print(paper)


# ================================ PNAS ================================= #
# =============================== 17.5% ================================ #



# ================== PUBLIC LIBRARY OF SCIENCE (PLOS) =================== #
# ================================ 20% ================================= #

















