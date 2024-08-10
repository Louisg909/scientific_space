
import numpy as np
from scipy.spatial import KDTree
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, Isomap
import itertools
from sklearn.neighbors import NearestNeighbors

if __name__ == '__main__':
    from parameter_finder import param_search
    import cost_functions as cost
else:
    from .parameter_finder import param_search
    from . import cost_functions as cost


def find_npca(data):
    """
    Plots the cumulative variance and allows the user to input the desired variance threshold.
    
    Parameters:
    data : ndarray
        The input data to perform PCA on.
    
    Returns:
    float
        The variance threshold specified by the user.
    """
    # Perform PCA to calculate the explained variance
    pca = PCA().fit(data)
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    
    # Plot the cumulative variance
    plt.figure(figsize=(8, 5))
    plt.plot(cumulative_variance, marker='o', linestyle='--')
    plt.xlabel('Number of Principal Components')
    plt.ylabel('Cumulative Explained Variance')
    plt.title('Cumulative Variance Explained by PCA Components')
    plt.grid(True)
    plt.show()
    
    # Ask the user for their desired variance threshold
    variance_threshold = float(input('Please enter the desired variance threshold (e.g., 0.95 for 95%):\t'))
    return variance_threshold

def get_npca(data, variance_threshold=0.95):
    """
    Applies PCA on the data to retain a specified amount of variance.
    
    Parameters:
    data : ndarray
        Takes the data as an input.
    variance_threshold : float, optional, default=0.95
        The amount of original variance to retain in the reduction.
    """
    pca = PCA().fit(data)
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    n_components = np.argmax(cumulative_variance >= variance_threshold) + 1
    return PCA(n_components=n_components) # data is fitted by the return value.fit_transform(data)


def apply_reductions(raw, n_pca):
    """
    Applies multiple dimensionality reduction techniques on the data.
    data : ndarray
        Takes the data as an input.
    """
    def get_dict(result):
        return {'data': result[1], 'info': result[0]}

    # parameters
    tsne_raw = get_dict(param_search(apply_tsne, cost.tsne, raw, perplexity=(5,50))) 
    tsne_npca = get_dict(param_search(apply_tsne, cost.tsne, n_pca, perplexity=(5,50)))
    print(tsne_npca)

    isomap_raw = get_dict(param_search(apply_isomap, cost.isomap, raw, n_neighbors=(2,20)))
    isomap_npca = get_dict(param_search(apply_isomap, cost.isomap, n_pca, n_neighbors=(2,20)))

    # hessian_raw = get_dict(param_search(apply_hessian, cost.hessian, raw, n_neighbors=(2,20)))
    #hessian_npca = get_dict(param_search(apply_hessian, cost.hessian, n_pca, n_neighbors=(2,20)))
    hessian_raw = {'info' : 'Fillers because hessian doesn\'t like to work on big datasets.', 'data': isomap_raw}


    return {'rand' : apply_random(raw), 'pca' : {'data': apply_pca(raw), 'info':''}, 'tsne' : tsne_raw, 'pca_tsne' : tsne_npca,
            'iso' : isomap_raw, 'pca_iso' : isomap_npca, 'hes' : hessian_raw, 'hes again lol' : hessian_raw}



def apply_random(data):
    """
    Applies a random projection of the data.
    
    Parameters:
    data : ndarray
        Takes the data as an input.
    """
    axes = np.random.choice(data.shape[1], size=2, replace=False)
    return {'data': data[:, axes], 'info': axes}

def apply_pca(data):
    """
    Applies PCA on the data to reduce it to 2 dimensions.

    Parameters:
    data : ndarray
        Takes the data as an input.
    """
    pca = PCA(n_components=2).fit_transform(data)
    return pca

def apply_tsne(data, perplexity=30.0):
    max_iter=1000
    """
    Applies t-SNE on both the data and npca to reduce them to 2 dimensions.
    
    Parameters:
    data : ndarray
        Takes the data as an input.
    perplexity : float, optional, default=30.0
        The perplexity is related to the number of nearest neighbors that is used in other manifold learning algorithms.
    """
    return TSNE(n_components=2, perplexity=perplexity, learning_rate='auto', max_iter=max_iter).fit_transform(data)

def apply_isomap(data, n_neighbors=5):
    """
    Applies Isomap on both the data and npca to reduce them to 2 dimensions.
    
    Parameters:
    data : ndarray
        Takes the data as an input.
    n_neighbors : int, optional, default=5
        Number of neighbors to consider for each point.
    """
    return Isomap(n_components=2, n_neighbors=int(n_neighbors)).fit_transform(data)

def apply_hessian(data, n_neighbors=10):
    """
    Applies Isomap on both the data and npca to reduce them to 2 dimensions.
    
    Parameters:
    data : ndarray
        Takes the data as an input.
    n_neighbors : int, optional, default=10
        Number of neighbors to consider for each point.
    """
    n_neighbors=int(n_neighbors)
    # Step 1: Compute the k-nearest neighbors
    tree = KDTree(data)
    distances, indices = tree.query(data, k=n_neighbors + 1)  # +1 because the first neighbor is the point itself
    
    # Step 2: Compute the weight matrix
    N, D = data.shape
    W = lil_matrix((N, N))
    for i in range(N):
        neighbors = indices[i][1:]  # skip the first neighbor (the point itself)
        Z = data[neighbors] - data[i]  # center the neighbors
        C = Z @ Z.T
        C = (C + C.T) / 2  # make sure C is symmetric
        w = np.linalg.solve(C + np.eye(n_neighbors) * 1e-3, np.ones(n_neighbors))  # solve Cw = 1
        w /= w.sum()  # normalize the weights
        W[i, neighbors] = w
    
    # Step 3: Compute the Hessian matrix
    H = lil_matrix((N, N))
    for i in range(N):
        neighbors = indices[i][1:]
        for a in range(n_neighbors):
            for b in range(n_neighbors):
                H[i, neighbors[a]] += W[i, neighbors[a]] * W[i, neighbors[b]]
                H[i, neighbors[b]] += W[i, neighbors[a]] * W[i, neighbors[b]]
    
    # Make H symmetric
    H = (H + H.T) / 2
    
    # Step 4: Compute the eigenvalues and eigenvectors
    print('\n\nFinding eigs', flush=True)
    print(f'H:\n{H}', flush=True)
    eigenvalues, eigenvectors = eigsh(H, k=3, which='SM', maxiter=20000, tol=1e-4)  # smallest magnitude
    
    # Return the two eigenvectors corresponding to the second and third smallest eigenvalues
    return eigenvectors[:, 1:3]


if __name__ == '__main__':
    np.random.seed(42)
    
    # Generate high-dimensional data (e.g., 1000 samples, 100 features)
    n_samples = 1000
    n_features = 100

    # Create random high-dimensional data
    high_dim_data = np.random.rand(n_samples, n_features)

    def get_dict(result):
        return {'data': result[1], 'info': result[0]}

    a, b = param_search(apply_tsne, cost.tsne, high_dim_data, initial_lr=10, **{'perplexity':(5,20)})
    print(a)
    print(b)
    tsne_raw = get_dict((a, b))

    print(tsne_raw)

