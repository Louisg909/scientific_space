import numpy as np



def calculate_weights(p, v):
    """
    Calculate the weights for each cited paper.
    p: numpy array, embedding vector of the paper
    v: list of numpy arrays, embedding vectors of the cited papers
    """
    weights = []
    for v_n in v:
        a = np.sum(v_n ** 2)
        b = -2 * np.sum(p * v_n)
        w_n = -b / (2 * a)
        weights.append(w_n)
    
    # Normalize weights
    weights = np.array(weights)
    normalized_weights = weights / np.sum(weights)
    return normalized_weights

def calculate_contribution(p, v, weights):
    """
    Calculate the contribution vector.
    p: numpy array, embedding vector of the paper
    v: list of numpy arrays, embedding vectors of the cited papers
    weights: numpy array, weights for each cited paper
    """
    weighted_sum = np.sum([w * v_n for w, v_n in zip(weights, v)], axis=0)
    c = p - weighted_sum
    return c

# Example usage
p = np.array([0.5, 0.2, 0.8])  # Example embedding vector of the paper
v = [np.array([0.1, 0.3, 0.4]), np.array([0.4, 0.1, 0.5])]  # Example embedding vectors of cited papers

weights = calculate_weights(p, v)
contribution = calculate_contribution(p, v, weights)

print("Weights:", weights)
print("Contribution vector:", contribution)
