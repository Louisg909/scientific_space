import numpy as np
from scipy.spatial import KDTree
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, Isomap
from sklearn.neighbors import NearestNeighbors
import itertools

if __name__ == '__main__':
    from parameter_finder import parameter_search
    import cost_functions as cost
else:
    from dimension_reduction.parameter_finder import parameter_search
    from dimension_reduction import cost_functions as cost


def plot_cumulative_variance(data):
    """Plots the cumulative variance explained by PCA components."""
    pca = PCA().fit(data)
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    
    plt.figure(figsize=(8, 5))
    plt.plot(cumulative_variance, marker='o', linestyle='--')
    plt.xlabel('Number of Principal Components')
    plt.ylabel('Cumulative Explained Variance')
    plt.title('Cumulative Variance Explained by PCA Components')
    plt.grid(True)
    plt.show()
    
def get_npca_model(data, variance_threshold=0.95):
    """Calculates the number of PCA components needed to retain the specified variance, before returning the model"""
    pca = PCA().fit(data)
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    n_components = np.argmax(cumulative_variance >= variance_threshold) + 1
    return PCA(n_components=n_components) # data is fitted by the return value.fit_transform(data)


def apply_dimensionality_reduction(raw_data, npca_data):
    """Applies the various dimensionality reduction techniques to the data."""
    def create_result_dict(result):
        return {'data': result[1], 'info': result[0]}

    tsne_raw = create_result_dict(parameter_search(apply_tsne, cost.tsne, raw_data, perplexity=(5, 50))) 
    tsne_npca = create_result_dict(parameter_search(apply_tsne, cost.tsne, npca_data, perplexity=(5, 50)))

    isomap_raw = create_result_dict(parameter_search(apply_isomap, cost.isomap, raw_data, n_neighbors=(2, 20)))
    isomap_npca = create_result_dict(parameter_search(apply_isomap, cost.isomap, npca_data, n_neighbors=(2, 20)))

    #hessian_raw = get_dict(parameter_search(apply_hessian, cost.hessian, raw, n_neighbors=(2,20)))
    #hessian_npca = get_dict(parameter_search(apply_hessian, cost.hessian, n_pca, n_neighbors=(2,20)))
    hessian_dummy = {'info' : 'Hessian doesn\'t work well with large datasets, using Isomap as placeholder', 'data': isomap_raw}

    return {
            'random_projection' : apply_random_projection(raw),
            'pca' : {'data': apply_pca(raw), 'info':''},
            'tsne_raw' : tsne_raw,
            'tsne_npca' : tsne_npca,
            'iso_raw' : isomap_raw,
            'iso_npca' : isomap_npca,
            'hessian_dummy' : hessian_dummy,
            'hessian_dummy' : hessian_dummy
        }


def apply_random_projection(data):
    """Applies a random projection to the data."""
    axes = np.random.choice(data.shape[1], size=2, replace=False)
    return {'data': data[:, axes], 'info': {'axes': axes}}

def apply_pca(data):
    """ Applies PCA on the data to reduce it to 2 dimensions."""
    return PCA(n_components=2).fit_transform(data)

def apply_tsne(data, perplexity=30.0):
    """ Applies t-SNE to reduce the data to 2 dimensions.  """
    return TSNE(n_components=2, perplexity=perplexity, learning_rate='auto', max_iter=1000).fit_transform(data)

def apply_isomap(data, n_neighbors=5):
    """ Applies Isomap to reduce the data to 2 dimensions.  """
    return Isomap(n_components=2, n_neighbors=int(n_neighbors)).fit_transform(data)

def apply_hessian(data, n_neighbors=10):
    """ Applies Hessian Locally Linear Embedding (LLE) to reduce the data to 2 dimensions."""
    n_neighbors = int(n_neighbors)

    tree = KDTree(data)
    _, indices = tree.query(data, k=n_neighbors + 1)  # +1 because the first neighbor is the point itself
    
    amples, _ = data.shape
    weight_matrix = lil_matrix((n_samples, n_samples))
    for i in range(n_samples):
        neighbors = indices[i][1:]  # skip the first neighbor (the point itself)
        Z = data[neighbors] - data[i]  # center the neighbors
        C = Z @ Z.T
        C = (C + C.T) / 2  # make sure C is symmetric
        w = np.linalg.solve(C + np.eye(n_neighbors) * 1e-3, np.ones(n_neighbors))  # solve Cw = 1
        w /= w.sum()  # normalize the weights
        weight_matrix[i, neighbors] = w
    
    hessian_matrx = lil_matrix((n_samples, n_samples))
    for i in range(n_samples):
        neighbors = indices[i][1:]
        for a, b in itertools.product(range(n_neighbors), repeat=2):
            hessian_matrix[i, neighbors[a]] += weight_matrix[i, neighbors[a]] * weight_matrix[i, neighbors[b]]
            hessian_matrix[i, neighbors[b]] += weight_matrix[i, neighbors[a]] * weight_matrix[i, neighbors[b]]

    hessain_matrix = (hessian_matrix + hessian_matrix.T) / 2
    
    eigenvalues, eigenvectors = eigsh(hessian_matrix, k=3, which='SM', maxiter=20000, tol=1e-4)
    
    # Return the two eigenvectors corresponding to the second and third smallest eigenvalues
    return eigenvectors[:, 1:3]

