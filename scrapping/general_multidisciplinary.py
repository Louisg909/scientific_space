

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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

def aaas_get_random_article_urls(count=10):
    """
    Function to get random article URLs from the Science | AAAS website using Selenium.
    """
    url = "https://www.science.org/journals"
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-blink-features=AutomationControlled')  # New option
    driver_path = './chromedriver.exe' 
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)
    
    # Adding delay to account for Cloudflare challenge
    time.sleep(10)  # Increased sleep time to allow Cloudflare challenge to resolve
    
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/doi/") and contains(@href, "science")]'))
    )
    
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
    if (count > len(article_links)):
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
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver_path = './chromedriver.exe' 
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)
    time.sleep(5) 
    
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
        print(f'Paper: {paper}')

"""

The error you are seeing (`selenium.common.exceptions.TimeoutException`) is occurring because Selenium is unable to find the specified element on the page within the allotted time. This is likely due to the ongoing issue with the Cloudflare challenge, which is preventing the page from fully loading or behaving as expected.

### Possible Solutions

1. **Increase the Timeout Further**: You can try increasing the timeout even more to give the page more time to bypass the Cloudflare challenge. However, this might not solve the issue if the challenge remains unresolved.

   ```python
   WebDriverWait(driver, 30).until(
       EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/doi/") and contains(@href, "science")]'))
   )
   ```

2. **Use a Different WebDriver**: Consider using a different WebDriver like `undetected-chromedriver`, which is specifically designed to avoid detection by anti-bot services like Cloudflare.

   First, you would need to install it:

   ```bash
   pip install undetected-chromedriver
   ```

   Then, update your code to use it:

   ```python
   import undetected_chromedriver as uc

   def aaas_get_random_article_urls(count=10):
       """
       Function to get random article URLs from the Science | AAAS website using Selenium.
       """
       url = "https://www.science.org/journals"
       
       options = uc.ChromeOptions()
       options.add_argument('--headless')  
       options.add_argument('--disable-gpu')
       driver = uc.Chrome(options=options)
       
       driver.get(url)
       
       # Adding delay to account for Cloudflare challenge
       time.sleep(10)
       
       WebDriverWait(driver, 20).until(
           EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/doi/") and contains(@href, "science")]'))
       )
       
       # Print the page source for debugging
       print(driver.page_source)
       
       # Find all article links
       article_links = driver.find_elements(By.XPATH, '//a[contains(@href, "/doi/") and contains(@href, "science")]')
       print(f"Found {len(article_links)} article links")
       
       if not article_links:
           print("No article links found.")
           driver.quit()
           return []
       
       if len(article_links) < count:
           count = len(article_links)
       
       random_links = random.sample(article_links, count)
       article_urls = ["https://www.science.org" + link.get_attribute('href') for link in random_links]
       
       driver.quit()
       return article_urls
   ```

3. **Use a Proxy**: Using a proxy server might help you bypass Cloudflare's checks if they are based on IP address.

4. **Manually Bypass Cloudflare**: You could manually access the site once in a regular browser and solve the Cloudflare challenge, then export the cookies and use them in your Selenium session to bypass the challenge.

5. **Consider an Alternative Approach**: Instead of using Selenium, you could try using a library like `requests-html` that can render JavaScript. This might bypass the Cloudflare challenge in some cases.

### Example with `requests-html`:

```python
from requests_html import HTMLSession

def aaas_get_random_article_urls(count=10):
    session = HTMLSession()
    url = "https://www.science.org/journals"
    
    r = session.get(url)
    r.html.render(sleep=3)  # Wait for JavaScript to load
    
    article_links = r.html.xpath('//a[contains(@href, "/doi/") and contains(@href, "science")]', first=False)
    
    if len(article_links) < count:
        count = len(article_links)
    
    random_links = random.sample(article_links, count)
    article_urls = ["https://www.science.org" + link.attrs['href'] for link in random_links]
    
    return article_urls
```

This approach can sometimes bypass Cloudflare because it renders the JavaScript like a regular browser, but it is less likely to trigger anti-bot mechanisms.

If none of these methods work, you might need to explore other options for scraping or obtaining the data, such as using an API if available or manually collecting the necessary information.
"""

# ================================ PNAS ================================= #
# =============================== 17.5% ================================ #



# ================== PUBLIC LIBRARY OF SCIENCE (PLOS) =================== #
# ================================ 20% ================================= #

















