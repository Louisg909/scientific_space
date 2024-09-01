import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE





def calculate_inheritance_factor(source_embedding, citation_embedding):
    # Reshape citation_embedding to be a column vector
    citation_embedding = citation_embedding.reshape(-1, 1)

    citation_contribution = np.dot(source_embedding.T, citation_embedding)
    citation_norm_squared = np.dot(citation_embedding.T, citation_embedding)
    inheritance_factor = citation_contribution / citation_norm_squared
    return inheritance_factor.item()  # Convert to scalar


def calculate_citation_weights_and_contribution_vector(source_embedding, citation_embeddings):
    source_embedding = np.array(source_embedding, dtype=np.float64).reshape(-1, 1)
    if citation_embeddings is None or len(citation_embeddings) == 0:
        return None, source_embedding
    citation_embeddings = np.array(citation_embeddings, dtype=np.float64)

    inheritance_factors = [calculate_inheritance_factor(source_embedding, citation) for citation in citation_embeddings]
    total_inheritance = sum(inheritance_factors)
    weights = [factor / total_inheritance for factor in inheritance_factors]

    # Calculate the aggregated contribution vector
    aggregated_contribution = np.zeros_like(source_embedding, dtype=np.float64)
    for i in range(len(citation_embeddings)):
        aggregated_contribution += citation_embeddings[i]reshape(-1, 1) * weights[i]
    contribution_vector = source_embedding - aggregated_contribution

    return weights, contribution_vector








def calculate_inheritance_factor(source_embedding, citation_embedding):
    # Reshape citation_embedding to be a column vector
    citation_embedding = citation_embedding.reshape(-1, 1)

    citation_contribution = np.dot(source_embedding.T, citation_embedding)
    citation_norm_squared = np.dot(citation_embedding.T, citation_embedding)
    inheritance_factor = citation_contribution / citation_norm_squared
    return inheritance_factor.item()  # Convert to scalar


def calculate_citation_weights_and_contribution_vector(source_embedding, citation_embeddings):
    source_embedding = np.array(source_embedding, 
                                dtype=np.float64).reshape(-1, 1)
    if citation_embeddings is None or len(citation_embeddings) == 0:
        return None, source_embedding
    citation_embeddings = np.array(citation_embeddings, dtype=np.float64)

    inheritance_factors = [
            calculate_inheritance_factor(source_embedding, citation) 
            for citation in citation_embeddings]
    total_inheritance = sum(inheritance_factors)
    weights = [factor / total_inheritance for factor in inheritance_factors]

    # Calculate the aggregated contribution vector
    aggregated_contribution = np.zeros_like(source_embedding, dtype=np.float64)
    for i in range(len(citation_embeddings)):
        aggregated_contribution += citation_embeddings[i]reshape(-1, 
                                                                  1) * weights[i]
    contribution_vector = source_embedding - aggregated_contribution
    


def plot_embeddings_and_contributions(embeddings, contributions):
    result = contribution_with_reductions(embeddings, contributions)
    plot_vectors(result)

def contribution_with_reductions(embeddings, contributions, tsne_perplexity=30, tsne_n_iter=1000):
    # Combine embeddings and contributions
    total = np.vstack((embeddings, contributions))

    # Apply PCA to reduce dimensionality to 2 components
    pca = PCA(n_components=2)
    reduced_total_pca = pca.fit_transform(total)

    # Apply t-SNE to reduce dimensionality to 2 components
    tsne = TSNE(n_components=2, perplexity=tsne_perplexity, n_iter=tsne_n_iter, random_state=42)
    reduced_total_tsne = tsne.fit_transform(total)

    # Split the reduced_total arrays back into embeddings and contributions
    n_samples = embeddings.shape[0]
    
    reduced_embeddings_pca = reduced_total_pca[:n_samples]
    reduced_cont_pos_pca = reduced_total_pca[n_samples:]
    
    reduced_embeddings_tsne = reduced_total_tsne[:n_samples]
    reduced_cont_pos_tsne = reduced_total_tsne[n_samples:]

    # Prepare vectors
    vectors_pca = prepare_vectors(reduced_embeddings_pca, reduced_cont_pos_pca)
    vectors_tsne = prepare_vectors(reduced_embeddings_tsne, reduced_cont_pos_tsne)

    # Return a dictionary with the results
    return {"pca": vectors_pca, "tsne": vectors_tsne}

def prepare_vectors(start, end):
    """
    Prepares a list of tuples where each tuple contains a start vector and an end vector.

    Parameters:
    start (numpy.ndarray): A 2D numpy array where each row is a 2D start vector.
    end (numpy.ndarray): A 2D numpy array where each row is a 2D end vector.

    Returns:
    list: A list of tuples, where each tuple is (start_i, end_i).
    """
    if start.shape != end.shape:
        raise ValueError("The start and end arrays must have the same shape.")
    
    # Create a list of tuples where each tuple is (start[i], end[i])
    vectors = [(start[i], end[i]) for i in range(start.shape[0])]
    
    return vectors

def plot_vectors(vector_reductions):
    vectors_pca = vector_reductions['pca']
    vectors_tsne = vector_reductions['tsne']

    # Initialize a plot with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Lists to hold all x and y values for setting axis limits
    all_x_pca, all_y_pca = [], []
    all_x_tsne, all_y_tsne = [], []

    # Plot PCA vectors
    for start, end in vectors_pca:
        vector = end - start
        ax1.quiver(start[0], start[1], vector[0], vector[1], angles='xy', scale_units='xy', scale=1)
        all_x_pca.extend([start[0], end[0]])
        all_y_pca.extend([start[1], end[1]])

    ax1.set_aspect('equal')
    x_min_pca, x_max_pca = min(all_x_pca), max(all_x_pca)
    y_min_pca, y_max_pca = min(all_y_pca), max(all_y_pca)
    ax1.set_xlim(x_min_pca - 1, x_max_pca + 1)
    ax1.set_ylim(y_min_pca - 1, y_max_pca + 1)
    ax1.grid(True)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_title('PCA Contribution Vectors')

    # Plot TSNE vectors
    for start, end in vectors_tsne:
        vector = end - start
        ax2.quiver(start[0], start[1], vector[0], vector[1], angles='xy', scale_units='xy', scale=1)
        all_x_tsne.extend([start[0], end[0]])
        all_y_tsne.extend([start[1], end[1]])

    ax2.set_aspect('equal')
    x_min_tsne, x_max_tsne = min(all_x_tsne), max(all_x_tsne)
    y_min_tsne, y_max_tsne = min(all_y_tsne), max(all_y_tsne)
    ax2.set_xlim(x_min_tsne - 1, x_max_tsne + 1)
    ax2.set_ylim(y_min_tsne - 1, y_max_tsne + 1)
    ax2.grid(True)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('TSNE Contribution Vectors')

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.show()

