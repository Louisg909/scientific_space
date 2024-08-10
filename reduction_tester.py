import logging
import numpy as np
import os

import paper_manager as pm
from dimension_reduction import reductions
from plotting import plot_interactive




# Set up logging configuration to overwrite the log file each time the code is run
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,  # Adjust as needed
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{log_dir}/application.log", mode='w'),  # 'w' mode overwrites the log file each time
        logging.StreamHandler()  # Optional: logs to console
    ]
)

logger = logging.getLogger(__name__)

logging.getLogger('PIL').setLevel(logging.WARNING)
logging.getLogger('numpy').setLevel(logging.WARNING)
logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)
logging.getLogger('matplotlib.pyplot').setLevel(logging.WARNING)

table = 'full_test'  # change to correct table when ready



#logger.info('Embedding files in database')
#def main():
#    bert = pm.SciBERT()
#    with pm.db() as db:
#        db.edit('full_test', bert.add_embedding)
#logger.info('FInished embedding files in database')

def get_data():
    logger.info(f"Fetching data for papers from table {table}.")
    with pm.db() as db:
        data = {p['id'] : {'title': p['title'], 'summary': p['summary'], 'embedding': pm.translate(p['embedding']), 'category': p['category'].split('.')[0]} for p in db.access(table=table, format='dict')}
    logger.debug(f"Fetched data: {{key: value for (key, value), _ in zip(data.items(), range(4))}}...")  # Log only a sample to avoid large output
    return data

def main():
    logger.info("Starting main processing.")
    
    papers = get_data()
    
    data = np.array([paper['embedding'] for paper in papers.values()])
    print(data.shape)
    ids = list(papers.keys())
    categories = [paper['category'] for paper in papers.values()]
    titles = [paper['title'] for paper in papers.values()]

    logger.info(f"Data shape after embedding: {data.shape}")
    
    variance_threshold = reductions.find_npca(data)
    logger.info(f"Calculated variance threshold for nPCA: {variance_threshold}")
    
    npca = reductions.get_npca(data, variance_threshold=variance_threshold)
    npca_data = npca.fit_transform(data)
    logger.info(f"nPCA data shape: {npca_data.shape}")
    
    reduction_types = reductions.apply_reductions(data, npca_data)
    logger.info("Applied dimensionality reductions.")

    plot_interactive(reduction_types, categories, titles)
    logger.info("Plotted reduction results.")
    logger.info("Processing complete.")

if __name__ == '__main__':
    main()
