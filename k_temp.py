
import sqlite3
import struct
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

import paper_manager as pm

with pm.db() as db:
    embeddings = []
    titles = []
    for paper in  db.fetch(table_name = 'full_test',
                           output_format='dict'):
        embeddings.append(pm.translate(paper['embedding']))
        titles.append(paper['title'])
    embeddings = np.array(embeddings)
    titles = np.array(titles)

print('Fetched')


# Perform KMeans clustering
num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, random_state=0)
clusters = kmeans.fit_predict(embeddings)

# Print 15 titles from each cluster
for i in range(num_clusters):
    print(f'\nCluster {i} Titles:')
    cluster_titles = titles[clusters == i][:15]
    for title in cluster_titles:
        print(f'- {title}')

# Reduce dimensionality with PCA and plot clusters
pca = PCA(n_components=2)
reduced_embeddings = pca.fit_transform(embeddings)

plt.figure(figsize=(10, 8))
colors = ['red', 'blue', 'green', 'purple', 'orange']

labels = {
        0:"Mathematical Structures, " +
        "Inequalities, and Transformations",
        1:"Physical Phenomena, Quantum "+
        "Mechanics, and Theoretical Models",
        2:"Philosophical and Foundational "+
        "Questions in Science",
        3:"Computational Complexity, Communication, "+
        "and AI Interpretability",
        4:"Astrophysical Phenomena and High-Energy Physics"
        }


for i in range(num_clusters):
    cluster_points = reduced_embeddings[clusters == i]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1],
                c=colors[i], label=labels[i])

plt.title('Paper Clusters Based on Embeddings')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend()
plt.grid(True)
plt.show()
