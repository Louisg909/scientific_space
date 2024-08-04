




import numpy as np

def calculate_weights(p, v=None):
    """
    Calculate the weights, normalized weights, and contribution vector for a given vector p and a set of parent vectors v.

    Parameters:
    p (np.ndarray): Target vector.
    v (np.ndarray): 2D array where each row is a parent vector.

    Returns:
    w (np.ndarray): Raw weights.
    w_hat (np.ndarray): Normalized weights.
    c (np.ndarray): Contribution vector.
    """
    if v is None:
        return None, p

    # Convert p and v to float64 for precision and to avoid casting issues
    p = np.array(p, dtype=np.float64).reshape(-1, 1)
    v = np.array(v, dtype=np.float64)
    
    # Number of parent vectors
    n = v.shape[0]
    
    # Calculate raw weights
    w = np.zeros(n, dtype=np.float64)
    for i in range(n):
        numerator = np.sum(p * v[i].reshape(-1, 1))
        denominator = np.sum(v[i] ** 2)
        w[i] = numerator / denominator
    
    # Normalize weights
    w_sum = np.sum(w)
    w_hat = w / w_sum
    
    # Calculate the contribution vector
    contribution_sum = np.zeros_like(p, dtype=np.float64)
    for i in range(n):
        contribution_sum += v[i].reshape(-1, 1) * w_hat[i]
    
    # Contribution vector
    c = p - contribution_sum
    
    return w_hat, c

if __name__ == '__main__':
    # Example usage:
    p = [1, 2, 3]
    v = [
#        [0.5, 1, 1.5],
#        [1, 2, 2.5],
#        [1.5, 2, 2]
    ]
    
    w_hat, c = calculate_weights(p, v)
    print("Normalized weights:", w_hat)
    print("Contribution vector:", c)
    

