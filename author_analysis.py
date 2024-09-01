
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.stats import pearsonr

# Assuming scrape_author, SciBERT, calculate_citation_weights_and_contribution_vector are imported
from paper_manager import SciBERT
from scrapping import scrape_author
from analysis import calculate_citation_weights_and_contribution_vector

def main():
    authors = ['Albert Einstein', 'Marie Curie', 'Niels Bohr', 'Werner Heisenberg', 'Enrico Fermi']
    all_publications = {}

    # Scrape data for each author
    for author in authors:
        print(f"Scraping data for {author}...")
        papers = scrape_author(author)
        all_publications[author] = papers

    # Initialize SciBERT model
    scibert = SciBERT()

    # Generate embeddings for each publication
    author_embeddings = {}
    for author, publications in all_publications.items():
        embeddings = []
        for paper in publications:
            text = f"{paper['title']}: {paper['summary']}"
            embedding = scibert.embed(text)
            embeddings.append((paper['year'], embedding))
        author_embeddings[author] = embeddings

    # Analyze contribution vectors over time
    for author, embeddings in author_embeddings.items():
        embeddings.sort(key=lambda x: x[0])  # Sort by year
        years = [year for year, _ in embeddings]
        contribution_vectors = []

        for i, (_, source_embedding) in enumerate(embeddings):
            citation_embeddings = [embedding for _, embedding in embeddings[:i]]
            _, contribution_vector = calculate_citation_weights_and_contribution_vector(source_embedding, citation_embeddings)
            contribution_vectors.append(contribution_vector.flatten())

        # Apply PCA to reduce dimensions for visualization
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(contribution_vectors)

        plt.plot(years, pca_result[:, 0], label=f"{author} (PCA1)")
        plt.plot(years, pca_result[:, 1], label=f"{author} (PCA2)")

    plt.xlabel('Year')
    plt.ylabel('PCA Components')
    plt.title('Contribution Vectors Over Time')
    plt.legend()
    plt.show()

    # Correlation analysis between authors
    for i in range(len(authors)):
        for j in range(i + 1, len(authors)):
            author_1 = authors[i]
            author_2 = authors[j]
            embeddings_1 = np.array([vector for _, vector in author_embeddings[author_1]])
            embeddings_2 = np.array([vector for _, vector in author_embeddings[author_2]])

            min_len = min(len(embeddings_1), len(embeddings_2))
            embeddings_1 = embeddings_1[:min_len]
            embeddings_2 = embeddings_2[:min_len]

            correlations = [pearsonr(embeddings_1[i], embeddings_2[i])[0] for i in range(min_len)]
            avg_correlation = np.mean(correlations)

            print(f"Correlation between {author_1} and {author_2}: {avg_correlation}")

if __name__ == "__main__":
    main()
