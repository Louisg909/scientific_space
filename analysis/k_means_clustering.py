import sqlite3
import struct
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

import paper_manager as pm

with pm.db() as db:
    data = db.fetch(table_name = 'full_test', select='title, embedding')

embeddings = np.array([pm.translate(embedding) for _, embedding in sample_data])
titles = [title for title, _ in sample_data]

# Perform KMeans clustering
num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, random_state=0)
clusters = kmeans.fit_predict(embeddings)

# Reduce dimensionality with PCA and plot clusters
pca = PCA(n_components=2)
reduced_embeddings = pca.fit_transform(embeddings)

plt.figure(figsize=(10, 8))
colors = ['red', 'blue', 'green', 'purple', 'orange']

for i in range(num_clusters):
    cluster_points = reduced_embeddings[clusters == i]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], c=colors[i], label=f'Cluster {i}')

plt.title('Paper Clusters Based on Embeddings')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend()
plt.grid(True)
plt.show()
