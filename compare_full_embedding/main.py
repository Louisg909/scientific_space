import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from collections import Counter

from scraper import arxiv_papers
from embed_data import SciBERT

def apply_pca(data):
    """Applies PCA on the data to reduce it to 2 dimensions."""
    return PCA(n_components=2).fit_transform(data)

def filter_top_categories(papers, top_n=6):
    """Filters the papers to only include those from the top N categories."""
    category_counts = Counter([paper['primary_category'] for paper in papers])
    top_categories = set([cat for cat, _ in category_counts.most_common(top_n)])
    return [paper for paper in papers if paper['primary_category'] in top_categories]

print('Loading scibert...')
bert = SciBERT()
print('Loaded scibert.')

print('Loading papers...')
papers = list(arxiv_papers(max_results=1000))  # Convert generator to a list
print(papers)
print('Filtering papers...')
filtered_papers = filter_top_categories(papers, top_n=6)
print(f'Filtered from {len(papers)} to {len(filtered_papers)}.')

title_embeddings = []
content_embeddings = []
categories = []

print('Getting and embedding papers')
count = 1
for paper in filtered_papers:
    print(f'Processing paper number {count}')

    # Check if content is None
    if paper["content"] is None:
        print(f'Warning: Paper {paper["id"]} titled "{paper["title"]}" has no content. Skipping embedding for content.')
        count += 1
        continue

    try:
        # Embedding title and summary
        title_embedding = bert.embed(f'{paper["title"]}: {paper["summary"]}', length=30)
        title_embeddings.append(title_embedding)
        
        # Embedding full content
        content_embedding = bert.embed(f'{paper["title"]}: {paper["content"]}', length=1024)
        content_embeddings.append(content_embedding)
        
        categories.append(paper['primary_category'])

    except Exception as e:
        print(f'Error: An error occurred while embedding paper {paper["id"]} titled "{paper["title"]}". Error: {e}')
        continue
    print(f'Paper {count} embedded.')

    count += 1

print('Papers embedded')

title_embeddings = np.array(title_embeddings)
content_embeddings = np.array(content_embeddings)

# PCA and t-SNE
title_reduced_pca = apply_pca(title_embeddings)
title_reduced_tsne = TSNE(n_components=2, perplexity=10, learning_rate='auto', max_iter=1000).fit_transform(title_embeddings)

content_reduced_pca = apply_pca(content_embeddings)
content_reduced_tsne = TSNE(n_components=2, perplexity=10, learning_rate='auto', max_iter=1000).fit_transform(content_embeddings)

# Plot by category
fig, axs = plt.subplots(2, 2, figsize=(15, 12))

# Get a list of unique categories
unique_categories = list(set(categories))
category_colors = plt.cm.get_cmap('tab10', len(unique_categories))

# Plot PCA for Title Embeddings by Category
for i, category in enumerate(unique_categories):
    indices = [j for j, x in enumerate(categories) if x == category]
    axs[0, 0].scatter(title_reduced_pca[indices, 0], title_reduced_pca[indices, 1], 
                      c=category_colors(i), label=category, alpha=0.6)
axs[0, 0].set_title('PCA of the embeddings of title and summary by category')
axs[0, 0].set_xlabel('Principal Component 1')
axs[0, 0].set_ylabel('Principal Component 2')
axs[0, 0].legend()

# Plot t-SNE for Title Embeddings by Category
for i, category in enumerate(unique_categories):
    indices = [j for j, x in enumerate(categories) if x == category]
    axs[0, 1].scatter(title_reduced_tsne[indices, 0], title_reduced_tsne[indices, 1], 
                      c=category_colors(i), label=category, alpha=0.6)
axs[0, 1].set_title('t-SNE of the embeddings of title and summary by category')
axs[0, 1].set_xlabel('t-SNE Dimension 1')
axs[0, 1].set_ylabel('t-SNE Dimension 2')
axs[0, 1].legend()

# Plot PCA for Content Embeddings by Category
for i, category in enumerate(unique_categories):
    indices = [j for j, x in enumerate(categories) if x == category]
    axs[1, 0].scatter(content_reduced_pca[indices, 0], content_reduced_pca[indices, 1], 
                      c=category_colors(i), label=category, alpha=0.6)
axs[1, 0].set_title('PCA of the embeddings of the paper contents by category')
axs[1, 0].set_xlabel('Principal Component 1')
axs[1, 0].set_ylabel('Principal Component 2')
axs[1, 0].legend()

# Plot t-SNE for Content Embeddings by Category
for i, category in enumerate(unique_categories):
    indices = [j for j, x in enumerate(categories) if x == category]
    axs[1, 1].scatter(content_reduced_tsne[indices, 0], content_reduced_tsne[indices, 1], 
                      c=category_colors(i), label=category, alpha=0.6)
axs[1, 1].set_title('t-SNE of the embeddings of the paper contents by category')
axs[1, 1].set_xlabel('t-SNE Dimension 1')
axs[1, 1].set_ylabel('t-SNE Dimension 2')
axs[1, 1].legend()

plt.tight_layout()
plt.show()

# KMeans clustering
num_clusters = 6
kmeans = KMeans(n_clusters=num_clusters, random_state=0)
title_clusters = kmeans.fit_predict(title_embeddings)
content_clusters = kmeans.fit_predict(content_embeddings)

# Plot by KMeans clusters
fig, axs = plt.subplots(2, 2, figsize=(15, 12))

cluster_colors = plt.cm.get_cmap('tab10', num_clusters)

# Plot PCA for Title Embeddings by Cluster
axs[0, 0].scatter(title_reduced_pca[:, 0], title_reduced_pca[:, 1], 
                  c=cluster_colors(title_clusters), alpha=0.6)
axs[0, 0].set_title('PCA of the embeddings of title and summary by KMeans cluster')
axs[0, 0].set_xlabel('Principal Component 1')
axs[0, 0].set_ylabel('Principal Component 2')

# Plot t-SNE for Title Embeddings by Cluster
axs[0, 1].scatter(title_reduced_tsne[:, 0], title_reduced_tsne[:, 1], 
                  c=cluster_colors(title_clusters), alpha=0.6)
axs[0, 1].set_title('t-SNE of the embeddings of title and summary by KMeans cluster')
axs[0, 1].set_xlabel('t-SNE Dimension 1')
axs[0, 1].set_ylabel('t-SNE Dimension 2')

# Plot PCA for Content Embeddings by Cluster
axs[1, 0].scatter(content_reduced_pca[:, 0], content_reduced_pca[:, 1], 
                  c=cluster_colors(content_clusters), alpha=0.6)
axs[1, 0].set_title('PCA of the embeddings of the paper contents by KMeans cluster')
axs[1, 0].set_xlabel('Principal Component 1')
axs[1, 0].set_ylabel('Principal Component 2')

# Plot t-SNE for Content Embeddings by Cluster
axs[1, 1].scatter(content_reduced_tsne[:, 0], content_reduced_tsne[:, 1], 
                  c=cluster_colors(content_clusters), alpha=0.6)
axs[1, 1].set_title('t-SNE of the embeddings of the paper contents by KMeans cluster')
axs[1, 1].set_xlabel('t-SNE Dimension 1')
axs[1, 1].set_ylabel('t-SNE Dimension 2')

plt.tight_layout()
plt.show()
