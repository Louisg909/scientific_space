import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, adjusted_rand_score, pairwise_distances
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
from scipy.spatial import procrustes
from scipy.spatial.distance import pdist, squareform
from scipy.sparse.csgraph import shortest_path
from scipy.stats import entropy
from scipy.special import softmax

# TODO
"""
- Fill in empty functions
- Make some functions more universal
    - Stuff like finding number of clusters in data original and reduced, comparing these, and use this number as comparison?
"""


# =========================== COST FUNCTIONS ============================ #



def hessian(original_data, reduced_data):
    original_distances = pairwise_distances(original_data)
    reconstructed_distances = pairwise_distances(reduced_data)
    
    mse =np.mean(np.square(original_distances - reconstructed_distances))
    
    return  1 / (1 + mse) # normalised

def isomap(original_data, reduced_data):
    geodesic_distances = shortest_path(pairwise_distances(original_data), method='auto', directed=False)
    euclidean_distances = pairwise_distances(reduced_data)

    residual_variance = 1 - np.sum(np.square(geodesic_distances - euclidean_distances)) / np.sum(np.squar(geodesic_distances))

    return residual_variance


def tsne(original_data, reduced_data):
    def kl_divergence(P, Q):
        Q = np.clip(Q, 1e-12, None) # Q has to be positive
        return np.sum(P * np.log(P / Q))

    def compute_joint_probabilities(distances, eps=1e-12):
        probabilities = np.exp(-distances ** 2)
        probabilities /= np.maximum(np.sum(probabilities, axis=1, keepdims=True), eps)

        return np.clip(probabilities, eps, 1 - eps)


    P = compute_joint_probabilities(pairwise_distances(original_distances))
    Q = compute_joint_probabilities(pairwise_distances(reduced_distances))
    
    # Symmetrize the probability matrices
    P = (P + P.T) / (2 * P.shape[0])
    Q = (Q + Q.T) / (2 * Q.shape[0])
    
    kl_div = kl_divergence(P, Q)
    
    normalized_kl_div = 1 / (1 + kl_div)
    
    return normalized_kl_div



# ============================ OTHER TESTS ============================= #


def trustworthiness_continuity(original_data, reduced_data, n_neighbors=5):
    def calculate_trustworthiness(original_data, reduced_data, n_neighbors):
        n_samples = original_data.shape[0]
        
        # Nearest neighbors in original space
        knn_orig = NearestNeighbors(n_neighbors=n_neighbors).fit(original_data)
        knn_orig_distances, knn_orig_indices = knn_orig.kneighbors(original_data)
        
        # Nearest neighbors in reduced space
        knn_red = NearestNeighbors(n_neighbors=n_neighbors).fit(reduced_data)
        knn_red_distances, knn_red_indices = knn_red.kneighbors(reduced_data)
        
        # Calculate ranks in original space
        ranks_orig = np.argsort(knn_orig_distances, axis=1)
        
        # Trustworthiness
        trust_sum = 0.0
        for i in range(n_samples):
            for j in range(1, n_neighbors):
                if knn_red_indices[i, j] not in knn_orig_indices[i]:
                    rank_indices = np.where(knn_orig_indices[i] == knn_red_indices[i, j])[0]
                    if rank_indices.size > 0:
                        rank = rank_indices[0]
                        trust_sum += rank - n_neighbors
        
        trustworthiness = 1 - (2.0 / (n_samples * n_neighbors * (2 * n_samples - 3 * n_neighbors - 1))) * trust_sum
        return trustworthiness

    def calculate_continuity(original_data, reduced_data, n_neighbors):
        n_samples = original_data.shape[0]
        
        # Nearest neighbors in original space
        knn_orig = NearestNeighbors(n_neighbors=n_neighbors).fit(original_data)
        knn_orig_distances, knn_orig_indices = knn_orig.kneighbors(original_data)
        
        # Nearest neighbors in reduced space
        knn_red = NearestNeighbors(n_neighbors=n_neighbors).fit(reduced_data)
        knn_red_distances, knn_red_indices = knn_red.kneighbors(reduced_data)
        
        # Calculate ranks in reduced space
        ranks_red = np.argsort(knn_red_distances, axis=1)
        
        # Continuity
        cont_sum = 0.0
        for i in range(n_samples):
            for j in range(1, n_neighbors):
                if knn_orig_indices[i, j] not in knn_red_indices[i]:
                    rank_indices = np.where(knn_red_indices[i] == knn_orig_indices[i, j])[0]
                    if rank_indices.size > 0:
                        rank = rank_indices[0]
                        cont_sum += rank - n_neighbors
        
        continuity = 1 - (2.0 / (n_samples * n_neighbors * (2 * n_samples - 3 * n_neighbors - 1))) * cont_sum
        return continuity

    # Calculate Trustworthiness and Continuity
    trustworthiness = calculate_trustworthiness(original_data, reduced_data, n_neighbors)
    continuity = calculate_continuity(original_data, reduced_data, n_neighbors)

    # Combined cost metric
    cost_metric = 1 - (trustworthiness + continuity) / 2
    return cost_metric


def find_cluster_number(original, reduced):
    # find in original
    n_original = 2
    # find in reduced
    n_reduced = 2
    return 1 - ((n_reduced-n_original)^2 / n_original^2), n_original # scale where 0 is that it doesn't have the same, 1 means it does have the same

# Clustering Quality
def calculate_clustering_quality(original_data, reduced_data, aprox_n_clusters=3):
    kmeans_original = KMeans(n_clusters=aprox_n_clusters).fit(original_data)
    kmeans_reduced = KMeans(n_clusters=aprox_n_clusters).fit(reduced_data)
    return adjusted_rand_score(kmeans_original.labels_, kmeans_reduced.labels_)

def calculate_reconstruction_error(original_data, reduced_data):
    pca = PCA(n_components=reduced_data.shape[1])
    reduced_data_approx = pca.inverse_transform(reduced_data)
    return np.mean(np.square(original_data - reduced_data_approx))

def calculate_explained_variance(original_data, reduced_data):
    pca = PCA(n_components=reduced_data.shape[1])
    pca.fit(original_data)
    return np.sum(pca.explained_variance_ratio_)

# Cluster Separation
def calculate_cluster_separation(original_data, reduced_data):
    # This is a placeholder and would need a specific cluster separation metric implementation
    distance_matrix = pairwise_distances(reduced_data)
    separation = np.sum(np.min(distance_matrix, axis=1))
    return separation

# Mean Relative Rank Error (MRRE)
def calculate_mrre(original_data, reduced_data):
    # Placeholder for MRRE calculation
    # Implement MRRE metric
    return 0

def calculate_procrustes(original_data, reduced_data):
    _, _, disparity = procrustes(original_data, reduced_data)
    return disparity

def calculate_metrics(original_data, reduced_data):
    silhouette = silhouette_score(original_data, reduced_data)
    db_index = davies_bouldin_score(original_data, reduced_data)
    reconstruction_error = calculate_reconstruction_error(original_data, reduced_data)
    explained_variance = calculate_explained_variance(original_data, reduced_data)
    clustering_quality = calculate_clustering_quality(original_data, reduced_data)
    cluster_separation = calculate_cluster_separation(original_data, reduced_data)
    continuity = calculate_continuity(original_data, reduced_data)
    trustworthiness = calculate_trustworthiness(original_data, reduced_data)
    mrre = calculate_mrre(original_data, reduced_data)
    procrustes_score = calculate_procrustes(original_data, reduced_data)
    
    return {
        'silhouette': silhouette,
        'db_index': db_index,
        'reconstruction_error': reconstruction_error,
        'explained_variance': explained_variance,
        'clustering_quality': clustering_quality,
        'cluster_separation': cluster_separation,
        'trust_continuity': trustworthiness_continuity,
        'mrre': mrre,
        'procrustes_score': procrustes_score
    }


