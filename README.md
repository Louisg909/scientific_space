# The Scientific Genome
## Description
This code is written to accompany my masters project looking at the nature of the scientific landscape. I am doing this by embedding each paper into science space (using SciBERT transformer and embedding techniques), as well as genetic citation trees (where the embeddings are the genome). I then will use various tools to both validate my model as well attempting to gain insights into the intrinsic (non institutional or social) nature of scientific research.
## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Louisg909/scientific_space.git
    ```

2. Navigate into the project directory:
    ```bash
    cd scientific_space
    ```

3. (Optional) Create and activate a virtual environment:
    ```bash
    python -m venv venv
    ```

    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

5. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## Usage
Example usages to be put in here later when I have finished more of the code.
### Scraping papers
```bash
python scrape.py -a
```
(Add arguments for how many papers to scrape?)
Add more steps for usage.
