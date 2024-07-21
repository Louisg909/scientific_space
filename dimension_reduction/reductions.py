
import numpy as np
from scipy.spatial import KDTree
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh

import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, Isomap
import itertools
from sklearn.neighbors import NearestNeighbors


def apply_npca(dt, variance_threshold=0.95):
    """
    Applies PCA on the data to retain a specified amount of variance.
    
    Parameters:
    dt : object
        Takes the simulation state as an input.
    variance_threshold : float, optional, default=0.95
        The amount of original variance to retain in the reduction.
    """
    pca = PCA().fit(dt.data)
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    n_components = np.argmax(cumulative_variance >= variance_threshold) + 1
    dt.n_pca = PCA(n_components=n_components).fit_transform(dt.data)


def find_params(dt):
    apply_npca(dt)

    fbp = find_best_parameters

    params = {}
    reduced = {}

    params['tsne'], reduced['tsne'] = fbp(apply_tsne, cf.trustworthiness_continuity, dt.data, n_tests=20, initial_lr=0.01, tolerance=1e-6, precision=1e-4, max_iter=1000, perplexity=(5,50))
    params['pca tsne'], reduced['pca tsne'] = fbp(apply_tsne, cf.trustworthiness_continuity, dt.n_pca, n_tests=20, initial_lr=0.01, tolerance=1e-6, precision=1e-4, max_iter=1000, perplexity=(5,50))

def apply_reductions(dt):
    """
    Applies multiple dimensionality reduction techniques on the data.
    dt : takes the simulation state as an input
    """
    apply_npca(dt)

    dt.reduced['rand'] = apply_random(dt.data)
    dt.reduced['pca'] = apply_pca(dt.n_pca)
    dt.reduced['tsne'] = apply_tsne(dt.data)
    dt.reduced['pca tsne'] = apply_tsne(dt.n_pca)
    dt.reduced['iso'] = apply_isomap(dt.data)
    dt.reduced['pca iso'] = apply_isomap(dt.n_pca)
    dt.reduced['hes'] = apply_hessian(dt.data)
    dt.reduced['pca hes'] = apply_hessian(dt.n_pca)


def apply_random(data):
    """
    Applies a random projection of the data.
    
    Parameters:
    dt : object
        Takes the simulation state as an input.
    """
    axes = np.random.choice(data.shape[1], size=2, replace=False)
    return data[:, axes]

def apply_pca(data):
    """
    Applies PCA on the data to reduce it to 2 dimensions.
    
    Parameters:
    t : object
        Takes the simulation state as an input.
    """
    pca = PCA(n_components=2).fit_transform(data)
    return pca

def apply_tsne(data, perplexity=30.0):
    learning_rate='auto'
    n_iter=1000
    """
    Applies t-SNE on both the data and npca to reduce them to 2 dimensions.
    
    Parameters:
    dt : object
        Takes the simulation state as an input.
    n_components : int, optional, default=2
        Dimension of the embedded space.
    perplexity : float, optional, default=30.0
        The perplexity is related to the number of nearest neighbors that is used in other manifold learning algorithms.
    learning_rate : float or 'auto', optional, default='auto'
        The learning rate for t-SNE.
    n_iter : int, optional, default=1000
        Maximum number of iterations for the optimization.
    """
    return TSNE(n_components=2, perplexity=perplexity, learning_rate=learning_rate, n_iter=n_iter).fit_transform(data)

def apply_isomap(data, n_neighbors=5):
    """
    Applies Isomap on both the data and npca to reduce them to 2 dimensions.
    
    Parameters:
    dt : object
        Takes the simulation state as an input.
    n_components : int, optional, default=2
        Number of coordinates for the manifold.
    n_neighbors : int, optional, default=5
        Number of neighbors to consider for each point.
    """
    return Isomap(n_components=2, n_neighbors=int(n_neighbors)).fit_transform(data)

def apply_hessian(data, n_neighbors=10):
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
