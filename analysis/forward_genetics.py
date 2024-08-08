import numpy as np
from scipy.stats import skew, kurtosis

class Node:
    def __init__(self, title, embedding, parents=None):
        self.title = title
        self.embedding = np.array(embedding, dtype=np.float64)
        self.parents = parents or []
        self.citation_weights, self.contribution = self.get_weights()
        self.cumulative_contribution = 1.0
        self.calculate_cumulative_contribution(self.cumulative_contribution)

    def set_contribution(self, contribution=1.0):
        self.cumulative_contribution = contribution
        if self.parents:
            for parent, weight in zip(self.parents, self.citation_weights):
                parent.set_contribution(contribution * weight)

    def get_weights(self):
        if not self.parents:
            return np.array([]), 1.0
        gene_pool = np.array([p.embedding for p in self.parents])
        return calculate_weights(self.embedding, gene_pool)

    def calculate_cumulative_contribution(self, parent_contribution=1.0):
        self.cumulative_contribution = parent_contribution
        if self.parents:
            for i, child in enumerate(self.parents):
                child_weight = self.citation_weights[i]
                child.calculate_cumulative_contribution(self.cumulative_contribution * child_weight)

    def get_position_data(self):
        node_data = [np.append(self.embedding, self.cumulative_contribution)]
        print(f"Node data (self): {node_data}")
        if not self.parents:
            return [node_data]
        parent_data = [parent.get_position_data() for parent in self.parents]
        
        print(f"Parent data before combining: {parent_data}")
        # Combine data from parents correctly
        combined_data = [[node_data]] + list(zip(*parent_data))
        
        # Flatten the lists in combined_data
        combined_data = [sum(depth_data, []) for depth_data in combined_data]
        
        print(f"Combined data: {combined_data}")
        return combined_data

    def get_distributions(self, general=False):
        """
        Finds the distributions per degree of subtree.
        
        Parameters:
        general (bool):
            - True: For understanding a larger population.
            - False: For understanding the specific tree data.
        
        Returns:
        tuple: Means, standard deviations, skewness, and kurtosis per depth.
        """
        data = self.get_position_data()
        print(f"Position data: {data}")
        
        means = [np.mean(n, axis=0) if len(n) > 0 else float('nan') for n in data]
        stand_dev = [np.std(n, axis=0, ddof=1 if general else 0) if len(n) > 0 else float('nan') for n in data]
        skews = [skew(n, axis=0) if len(n) > 0 else float('nan') for n in data]
        kurt_cobains = [kurtosis(n, axis=0) if len(n) > 0 else float('nan') for n in data]
        
        print(f"Means: {means}")
        print(f"Standard Deviations: {stand_dev}")
        print(f"Skewness: {skews}")
        print(f"Kurtosis: {kurt_cobains}")
        
        return means, stand_dev, skews, kurt_cobains

# Dummy calculate_weights function for illustration
def calculate_weights(embedding, gene_pool):
    # This is just a placeholder. Implement your own logic.
    weights = np.random.rand(len(gene_pool))
    weights /= weights.sum()
    return weights, weights.sum()

# Create the tree and run the analysis
tree = Node('', [1, 2], [
    Node('', [1.1, 2.3], [
        Node('', [2.0, 2.6], []),
        Node('', [1.0, 2.5], []),
        Node('', [1.3, 2.4], []),
        Node('', [0.7, 2.0], []),
        Node('', [1.5, 1.8], [])
        ]),
    Node('', [0.7, 2.1], [
        Node('', [0.4, 2.0], []),
        Node('', [0.2, 2.4], []),
        Node('', [0.8, 2.0], [])
        ]),
    Node('', [1.6, 2.0], [
        Node('', [1.9, 2.1], []),
        Node('', [1.7, 1.6], []),
        Node('', [1.5, 2.2], [])
        ]),
    Node('', [1.0, 1.6], [
        Node('', [1.1, 1.4], []),
        Node('', [0.8, 1.8], []),
        Node('', [0.6, 1.5], []),
        Node('', [1.2, 1.7], [])
        ])
    ])

mean, sd, skews, kurt = tree.get_distributions()
print(f'Means:\n{mean}\nStandard Deviations:\n{sd}\nSkewness:\n{skews}\nKurtosis:\n{kurt}')
