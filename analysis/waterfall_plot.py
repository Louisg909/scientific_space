import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import random

# Provided functions for calculating weights and contribution vectors
def calculate_inheritance_factor(source_embedding, citation_embedding):
    citation_embedding = citation_embedding.reshape(-1, 1)
    citation_contribution = np.dot(source_embedding.T, citation_embedding)
    citation_norm_squared = np.dot(citation_embedding.T, citation_embedding)
    inheritance_factor = citation_contribution / citation_norm_squared
    return inheritance_factor.item()

def calculate_citation_weights_and_contribution_vector(source_embedding, citation_embeddings):
    source_embedding = np.array(source_embedding, dtype=np.float64).reshape(-1, 1)
    if citation_embeddings is None or len(citation_embeddings) == 0:
        return None, source_embedding
    citation_embeddings = np.array(citation_embeddings, dtype=np.float64)

    inheritance_factors = [calculate_inheritance_factor(source_embedding, citation) 
                           for citation in citation_embeddings]
    total_inheritance = sum(inheritance_factors)
    weights = [factor / total_inheritance for factor in inheritance_factors]

    # Calculate the aggregated contribution vector
    aggregated_contribution = np.zeros_like(source_embedding, dtype=np.float64)
    for i in range(len(citation_embeddings)):
        aggregated_contribution += citation_embeddings[i].reshape(-1, 1) * weights[i]
    contribution_vector = source_embedding - aggregated_contribution

    return weights, contribution_vector

# Function to generate embeddings with weights and contribution vectors
def generate_citation_tree(base_embedding, num_citations=4):
    citation_embeddings = [np.random.rand(10) for _ in range(num_citations)]
    weights, contribution_vector = calculate_citation_weights_and_contribution_vector(base_embedding, citation_embeddings)
    citations = [base_embedding + contribution_vector.flatten()] + citation_embeddings
    return citations

# Generate source embedding
source_embedding = np.random.rand(10)

# Generate citation embeddings for the source embedding
first_level_citations = generate_citation_tree(source_embedding, num_citations=3)

# Generate second-level citations (citations of the first-level citations)
second_level_citations = []
second_level_sizes = []
for citation in first_level_citations[1:]:
    num_citations = random.randint(2, 3)
    second_level_sizes.append(num_citations)
    second_level_citations.append(generate_citation_tree(citation, num_citations=num_citations))

# Flatten the list of second-level citations
flat_second_level_citations = [item for sublist in second_level_citations for item in sublist]

# Combine all embeddings for PCA
all_embeddings = [source_embedding] + first_level_citations[1:] + flat_second_level_citations

# Perform PCA to reduce to 2D
pca = PCA(n_components=2)
pca_components = pca.fit_transform(all_embeddings)

# Influence calculation for both logarithmic and non-logarithmic scales
log_influence = np.flip(np.logspace(0, 1, len(pca_components)))
linear_influence = np.linspace(1, 10, len(pca_components))

# Function to plot the waterfall plot
def plot_waterfall(pca_components, influence, scale_type='logarithmic'):
    fig = plt.figure(figsize=(14, 6))
    
    # 3D Waterfall Plot
    ax = fig.add_subplot(121, projection='3d')
    ax.plot([pca_components[0, 0]], [pca_components[0, 1]], [influence[0]], 'ko')

    # Connect source to first-level citations
    start_idx = 1
    for i in range(len(first_level_citations) - 1):
        ax.plot([pca_components[0, 0], pca_components[start_idx + i, 0]],
                [pca_components[0, 1], pca_components[start_idx + i, 1]],
                [influence[0], influence[start_idx + i]], 'k-')
        ax.plot([pca_components[start_idx + i, 0]], [pca_components[start_idx + i, 1]], [influence[start_idx + i]], 'ko')

    # Connect each first-level citation to its own second-level citations
    current_idx = start_idx + len(first_level_citations) - 1
    for i in range(len(first_level_citations) - 1):
        for j in range(second_level_sizes[i]):
            ax.plot([pca_components[start_idx + i, 0], pca_components[current_idx, 0]],
                    [pca_components[start_idx + i, 1], pca_components[current_idx, 1]],
                    [influence[start_idx + i], influence[current_idx]], 'k-')
            ax.plot([pca_components[current_idx, 0]],
                    [pca_components[current_idx, 1]],
                    [influence[current_idx]], 'ko')
            current_idx += 1

    ax.set_xlabel('PCA Component 1')
    ax.set_ylabel('PCA Component 2')
    ax.set_zlabel('Product of Weights (Inverted, {} Scale)'.format(scale_type.capitalize()))

    # 2D Waterfall Plot
    ax2 = fig.add_subplot(122)
    ax2.plot([pca_components[0, 0]], [influence[0]], 'ko')

    # Connect source to first-level citations in 2D
    start_idx = 1
    for i in range(len(first_level_citations) - 1):
        ax2.plot([pca_components[0, 0], pca_components[start_idx + i, 0]],
                 [influence[0], influence[start_idx + i]], 'k-')
        ax2.plot([pca_components[start_idx + i, 0]], [influence[start_idx + i]], 'ko')

    # Connect each first-level citation to its own second-level citations in 2D
    current_idx = start_idx + len(first_level_citations) - 1
    for i in range(len(first_level_citations) - 1):
        for j in range(second_level_sizes[i]):
            ax2.plot([pca_components[start_idx + i, 0], pca_components[current_idx, 0]],
                     [influence[start_idx + i], influence[current_idx]], 'k-')
            ax2.plot([pca_components[current_idx, 0]],
                     [influence[current_idx]], 'ko')
            current_idx += 1

    ax2.set_xlabel('PCA Component 1')
    ax2.set_ylabel('Product of Weights (Inverted, {} Scale)'.format(scale_type.capitalize()))

    plt.show()

# Plot both logarithmic and linear waterfall plots
plot_waterfall(pca_components, log_influence, scale_type='logarithmic')
plot_waterfall(pca_components, linear_influence, scale_type='linear')
