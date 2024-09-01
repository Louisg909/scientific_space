import numpy as np

def calculate_inheritance_factor(source_embedding, citation_embedding):
    # Reshape citation_embedding to be a column vector
    citation_embedding = citation_embedding.reshape(-1, 1)

    citation_contribution = np.dot(source_embedding.T, citation_embedding)
    citation_norm_squared = np.dot(citation_embedding.T, citation_embedding)
    inheritance_factor = citation_contribution / citation_norm_squared
    return inheritance_factor.item()  # Convert to scalar


def calculate_citation_weights_and_contribution_vector(source_embedding,
                                                       citation_embeddings):
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
    
    return weights, contribution_vector


if __name__ == '__main__':
    v1 = [0,1,2,3]
    v2 = [2,6,4,5]
    v3 = [20,42,64,1]
    p = [1,40,20,12]
    v = [v1, v2, v3]

    l_weights, _ = calculate_citation_weights_and_contribution_vector(p, v)
    print(l_weights)





