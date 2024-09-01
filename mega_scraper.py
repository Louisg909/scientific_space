
import itertools
import time
from datetime import datetime, timedelta

# local imports
#from paper_manager import db, SciBERT, translate
import paper_manager as pm

# scrapers
#from .chemistry import get_chemical_science_papers as chemical_science
from scrapping.open_access import arxiv_papers, biorxiv_papers, chemrxiv_papers, pubmed_papers
from scrapping.physics import get_aps_papers as aps
from scrapping.crossref import retrieve_crossref_publications as crossref
from scrapping.databases import google_scholar_papers as google_scholar



"""
- Chemical Science
- crossref
- google scholar
- semantic scholar? (maybe)
- physical review journal (aps)
- ar$\chi$iv
- bioR$\chi$iv
- chemR$\chi$iv
- Pubmed
- ieee api -> limits not that great
"""


class Scraper:
    def __init__(self):
        self.SciBERT = pm.SciBERT()

        # scrapers list
        self.scrapers_seperate = [arxiv_papers(), biorxiv_papers(), chemrxiv_papers(), pubmed_papers(), aps(), crossref(), google_scholar()]
        self.scrapers = itertools.cycle(scraper.__iter__() for scraper in self.scrapers_seperate)
        #self.source_weights = [     chemical_science(), 
        #        0.10, # Chemical Science
        #        0.2,  # arXiv
        #        0.05, # bioRxiv
        #        0.05, # chemRxiv
        #        0.15, # PubMed
        #        0.15, # APS
        #        0.05, # Crossref
        #        0.25, # google scholar
        #        ]

        

    def combined(self):
        while True:
            try:
                yield next(next(self.scrapers))
            except StopIteration:
                self.scrapers = itertools.cycle(scraper for scraper in self.scrapers if scraper)
                if not self.scrapers:
                    break
            except Exception as e:
                print(f"Error encountered: {e}")

    def run(self):
        # ieee = IEEEScraper() - just run this seperatly every day lol - it takes literally 20 seconds to do 200 calls at 10 calls per second lol
        # for paper in ieee(max_iterations = 200):
        #     # add paper to database
        #     paper
        # del ieee # rip ieee :(

        # main scraping
        
        with pm.db() as db:
            while True:
                start_time = datetime.now()
                end_time = start_time + timedelta(hours=1)
                while datetime.now() < end_time: # hour on
                    for paper in self.combined():
                        # get embedding
                        paper['embedding'] = pm.translate(self.SciBERT.embed(f'{paper.get("title","")}: \n{paper.get("summary","")}'))
                        db.insert(paper, input_format='dict')
                        time.sleep(300)
                    self.scrapers = itertools.cycle(scraper.__iter__() for scraper in self.scrapers_seperate)
                time.sleep(3600) # hour off

def run_mega():
    scrape = Scraper()
    scrape.run()

def test_each_generator():
    for p in arxiv_papers():
        print(f'Arxiv:\t{p}')
        break
    for p in biorxiv_papers():
        print(f'Biorxiv:\t{p}')
        break
    for p in chemrxiv_papers():
        print(f'Chemrxiv:\t{p}')
        break
    for p in pubmed_papers():
        print(f'Pubmed:\t{p}')
        break
    for p in aps():
        print(f'APS:\t{p}')
        break
    for p in crossref():
        print(f'Crossref:\t{p}')
        break
    for p in google_scholar():
        print(f'Google:\t{p}')
        break

if __name__ == '__main__':
    test_each_generator()




"""
Basically want it to scrape efficiently with all the scrapers together, each weighted, each yielding dictionaries ready to be placed into the database. Check each of the scrapers before running.

Want to eliminate dead space - which is why I have only put sleeping before the request call, with the time depending on how much time was since last call to that. I will need to work out how to run multiple generators along side eachother...


Run IEEE first as only 200 calls per day, and can do 20 per second so only like 10 seconds worth of calls. Probably over croyde will just do that once to avoid any errors?

"""

