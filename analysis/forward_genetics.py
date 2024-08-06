# main.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import skew, kurtosis
from citation_weights import calculate_weights


class Node:
    def __init__(self, title, embedding, parents: list = None):
        self.title = title
        self.embedding = np.array(embedding, dtype=np.float64)
        self.parents = parents
        self.citation_weights, self.contribution = self.get_weights()
        print(self.contribution)
        self.cumulative_contribution = 1.0

        self.calculate_cumulative_contribution(self.cumulative_contribution)

    def set_contribution(self, contribution = 1.0):
        self.cumulative_contribution = contribution
        if self.parents:
            for parent, weight in zip(self.parents, self.citation_weights):
                parent.set_contribution(contribution * weight)

    def get_weights(self):
        gene_pool = np.array([p.embedding for p in self.parents])
        return calculate_weights(self.embedding, gene_pool)

    def calculate_cumulative_contribution(self, parent_contribution=1.0):
        self.cumulative_contribution = parent_contribution
        if self.parents:
            for i, child in enumerate(self.parents):
                child_weight = self.citation_weights[i]
                child.calculate_cumulative_contribution(self.cumulative_contribution * child_weight)

    def get_position_data(self):
        # Form:   [This, [parent1, parent2, parent3, parent4], [grandparent1, grandparent2, grandparent3]]
        node_data = np.append(self.embedding, [self.cumulative_contribution])
        if not self.parents or self.parents == []:
            return [node_data]
        parent_data = [parent.get_position_data() for parent in self.parents]

        print(parent_data)
        print(zip(*parent_data))
        print(data for data in zip(*parent_data))
        data = [sum((vals for vals in data), []) for data in zip(*parent_data)]

        return [[node_data]] + data

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
        
        means = [np.mean(n) if len(n) > 0 else float('nan') for n in data]
        stand_dev = [np.std(n, ddof=1 if general else 0) if len(n) > 0 else float('nan') for n in data]
        skews = [skew(n) if len(n) > 0 else float('nan') for n in data]
        kurt_cobains = [kurtosis(n) if len(n) > 0 else float('nan') for n in data]
        
        return means, stand_dev, skews, kurt_cobains

def plot_tree(root):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    def plot_node(node, parent_coords=None):
        x, y = node.contribution[:2].flatten()  # Ensure these are scalars
        z = np.log2(node.cumulative_contribution)  # Use cumulative product for z-axis with log transform

        if parent_coords:
            px, py, pz = parent_coords
            ax.plot([px, x], [py, y], [pz, z], 'r-o')

        if node.parents:
            for i, child in enumerate(node.parents):
                plot_node(child, (x, y, z))

    # Gather all cumulative contributions to determine range for ticks
    cumulative_contributions = []

    def gather_contributions(node):
        cumulative_contributions.append(node.cumulative_contribution)
        if node.parents:
            for child in node.parents:
                gather_contributions(child)

    gather_contributions(root)
    
    min_contribution = min(cumulative_contributions)
    max_contribution = max(cumulative_contributions)

    min_exponent = int(np.floor(np.log2(min_contribution)))
    max_exponent = int(np.ceil(np.log2(max_contribution)))

    plot_node(root)
    ax.set_xlabel('Contribution X')
    ax.set_ylabel('Contribution Y')
    ax.set_zlabel('Cumulative Contribution')

    # Set custom ticks and labels for the z-axis
    z_ticks = np.arange(min_exponent, max_exponent + 1)
    z_tick_labels = [f'$2^{{{exp}}}$' for exp in z_ticks]

    ax.set_zticks(z_ticks)
    ax.set_zticklabels(z_tick_labels)

    plt.show()





if __name__ == '__main__':
    tree = Node('', [1,2], [
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

    mean, sd, skew, kurt = tree.get_distributions()
    print(f'Mean:\t{mean}\nSD:\t{sd}\nSkew:\t{skew}\nKurtosis:\t{kurt}', flush=True)

#    tree = Node('Root', [1.5, 0], [
#        Node('Parent', [1.2, 0], [
#            Node('Grandparent', [1, 0], [])]),
#        Node('Unrelated', [0,1], [])])
    #tree = Node('Paper 1', [1, 2], [
    #    Node('Paper 2', [0.5, 1], [
    #        Node('Paper 3', [1, 1], [
    #            Node('Paper 9', [0.8, 0.7], []),
    #            Node('Paper 10', [0.5, 0.4], []),
    #        ]),
    #        Node('Paper 4', [1, 0.8], [
    #            Node('Paper 11', [0.9, 0.8], []),
    #            Node('Paper 12', [0.7, 0.5], []),
    #        ])
    #    ]),
    #    Node('Paper 5', [1, 2.5], [
    #        Node('Paper 6', [1, 0], [
    #            Node('Paper 13', [0.6, 0.3], []),
    #            Node('Paper 14', [0.8, 0.4], []),
    #        ]),
    #        Node('Paper 15', [0.9, 2.2], [
    #            Node('Paper 16', [0.7, 0.6], []),
    #            Node('Paper 17', [0.8, 0.7], []),
    #        ])
    #    ]),
    #    Node('Paper 7', [1.5, 2], [
    #        Node('Paper 8', [2, 0], [
    #            Node('Paper 18', [1.2, 1.1], []),
    #            Node('Paper 19', [1.3, 1.2], []),
    #        ]),
    #        Node('Paper 20', [1.6, 2.1], [
    #            Node('Paper 21', [1.4, 1.5], []),
    #            Node('Paper 22', [1.7, 1.9], []),
    #        ])
    #    ]),
    #    Node('Paper 23', [1.2, 2.4], [
    #        Node('Paper 24', [0.7, 0.9], [
    #            Node('Paper 25', [0.4, 0.6], []),
    #            Node('Paper 26', [0.5, 0.7], []),
    #        ]),
    #        Node('Paper 27', [1.1, 1.2], [
    #            Node('Paper 28', [0.8, 0.9], []),
    #            Node('Paper 29', [0.9, 1.0], []),
    #        ])
    #    ])
    #])

    # Plot the tree
    plot_tree(tree)
