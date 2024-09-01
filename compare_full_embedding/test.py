import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, Isomap

import numpy as np
title_embeddings = np.random.rand(100, 300)  # 100 samples, 300 features
content_embeddings = np.random.rand(100, 300)



# pca
title_reduced_pca = PCA(n_components=2).fit_transform(title_embeddings)
title_reduced_tsne = TSNE(n_components=2, perplexity=10, learning_rate='auto', max_iter=1000).fit_transform(title_embeddings)

# embed title and latex

# pca
content_reduced_pca = PCA(n_components=2).fit_transform(content_embeddings)
content_reduced_tsne = TSNE(n_components=2, perplexity=10, learning_rate='auto', max_iter=1000).fit_transform(content_embeddings)

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Create a 2x2 subplot grid
fig, axs = plt.subplots(2, 2, figsize=(15, 12))

# Plot PCA for Title Embeddings
axs[0, 0].scatter(title_reduced_pca[:, 0], title_reduced_pca[:, 1], c='blue', alpha=0.6)
axs[0, 0].set_title('PCA of the embeddings of title and summary')
axs[0, 0].set_xlabel('Principal Component 1')
axs[0, 0].set_ylabel('Principal Component 2')

# Plot t-SNE for Title Embeddings
axs[0, 1].scatter(title_reduced_tsne[:, 0], title_reduced_tsne[:, 1], c='green', alpha=0.6)
axs[0, 1].set_title('t-SNE of the embeddings of title and summary')
axs[0, 1].set_xlabel('t-SNE Dimension 1')
axs[0, 1].set_ylabel('t-SNE Dimension 2')

# Plot PCA for Content Embeddings
axs[1, 0].scatter(content_reduced_pca[:, 0], content_reduced_pca[:, 1], c='red', alpha=0.6)
axs[1, 0].set_title('PCA of the embeddings of the paper contents')
axs[1, 0].set_xlabel('Principal Component 1')
axs[1, 0].set_ylabel('Principal Component 2')

# Plot t-SNE for Content Embeddings
axs[1, 1].scatter(content_reduced_tsne[:, 0], content_reduced_tsne[:, 1], c='purple', alpha=0.6)
axs[1, 1].set_title('t-SNE of the embeddings of the paper contents')
axs[1, 1].set_xlabel('t-SNE Dimension 1')
axs[1, 1].set_ylabel('t-SNE Dimension 2')

# Adjust layout for better spacing
plt.tight_layout()

# Display the plots
plt.show()
