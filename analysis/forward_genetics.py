# main.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from citation_weights import calculate_weights

class Node:
    def __init__(self, title, embedding, citations: list, depth=0):
        self.title = title
        self.embedding = np.array(embedding, dtype=np.float64)
        self.citations = citations
        self.citation_weights, self.contribution = self.get_weights()
        self.depth = depth
        self.cumulative_contribution = 1.0

    def get_weights(self):
        if self.citations:
            gene_pool = np.array([p.embedding for p in self.citations])
            return calculate_weights(self.embedding, gene_pool)
        else:
            return np.array([]), np.zeros_like(self.embedding)

    def calculate_cumulative_contribution(self, parent_contribution=1.0):
        self.cumulative_contribution = parent_contribution
        if self.citations:
            for i, child in enumerate(self.citations):
                child_weight = self.citation_weights[i]
                child.calculate_cumulative_contribution(self.cumulative_contribution * child_weight)

def plot_tree(root):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    def plot_node(node, parent_coords=None):
        x, y = node.contribution[:2].flatten()  # Ensure these are scalars
        z = node.cumulative_contribution  # Use cumulative product for z-axis

        if parent_coords:
            px, py, pz = parent_coords
            ax.plot([px, x], [py, y], [pz, z], 'r-o')

        if node.citations:
            for i, child in enumerate(node.citations):
                plot_node(child, (x, y, z))

    plot_node(root)
    ax.set_xlabel('Contribution X')
    ax.set_ylabel('Contribution Y')
    ax.set_zlabel('Cumulative Contribution')
    plt.show()

if __name__ == '__main__':
#    tree = Node('Root', [1.5, 0], [
#        Node('Parent', [1.2, 0], [
#            Node('Grandparent', [1, 0], [])]),
#        Node('Unrelated', [0,1], [])])
    tree = Node('Paper 1', [1, 2], [
        Node('Paper 2', [0.5, 1], [
            Node('Paper 3', [1, 1], [
                Node('Paper 9', [0.8, 0.7], []),
                Node('Paper 10', [0.5, 0.4], []),
            ]),
            Node('Paper 4', [1, 0.8], [
                Node('Paper 11', [0.9, 0.8], []),
                Node('Paper 12', [0.7, 0.5], []),
            ])
        ]),
        Node('Paper 5', [1, 2.5], [
            Node('Paper 6', [1, 0], [
                Node('Paper 13', [0.6, 0.3], []),
                Node('Paper 14', [0.8, 0.4], []),
            ]),
            Node('Paper 15', [0.9, 2.2], [
                Node('Paper 16', [0.7, 0.6], []),
                Node('Paper 17', [0.8, 0.7], []),
            ])
        ]),
        Node('Paper 7', [1.5, 2], [
            Node('Paper 8', [2, 0], [
                Node('Paper 18', [1.2, 1.1], []),
                Node('Paper 19', [1.3, 1.2], []),
            ]),
            Node('Paper 20', [1.6, 2.1], [
                Node('Paper 21', [1.4, 1.5], []),
                Node('Paper 22', [1.7, 1.9], []),
            ])
        ]),
        Node('Paper 23', [1.2, 2.4], [
            Node('Paper 24', [0.7, 0.9], [
                Node('Paper 25', [0.4, 0.6], []),
                Node('Paper 26', [0.5, 0.7], []),
            ]),
            Node('Paper 27', [1.1, 1.2], [
                Node('Paper 28', [0.8, 0.9], []),
                Node('Paper 29', [0.9, 1.0], []),
            ])
        ])
    ])

    # Calculate cumulative contributions starting from the root
    tree.calculate_cumulative_contribution()

    # Plot the tree
    plot_tree(tree)
