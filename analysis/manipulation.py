
def split_embeddings(embeddings):
    # Find the number of dimensions
    dimensions = len(embeddings[0])
    
    # Initialize a list to hold the result for each dimension
    dimension_vals = [[] for _ in range(dimensions)]
    
    # Iterate through each embedding and its corresponding year
    for embedding in embeddings:
        for i, value in enumerate(embedding):
            dimension_vals[i].append(value)

    return dimension_vals
