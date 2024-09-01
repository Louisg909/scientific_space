import numpy as np
from scipy.stats import skew, kurtosis
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as ticker

from citation_weights import get_weights_contribution

class Node:
    def __init__(self, title, embedding, parents=None):
        self.title = title
        self.embedding = np.array(embedding, dtype=np.float64)
        self.parents = parents or []
        self.citation_weights, self.contribution = self.get_weights()
        self.product_of_weights = 1.0
        self.calculate_product_of_weights(self.product_of_weights)

    def set_contribution(self, contribution=1.0):
        self.product_of_weights = contribution
        if self.parents:
            for parent, weight in zip(self.parents, self.citation_weights):
                parent.set_contribution(contribution * weight)

    def get_weights(self):
        if not self.parents:
            return np.array([]), 1.0
        gene_pool = np.array([p.embedding for p in self.parents])
        return get_weights_contribution(self.embedding, gene_pool)

    def calculate_product_of_weights(self, parent_product=1.0):
        self.product_of_weights = parent_product
        print(f"Node: {self.title}, Product of Weights: {self.product_of_weights}")
        if self.parents:
            for i, child in enumerate(self.parents):
                child_weight = self.citation_weights[i]
                child.calculate_product_of_weights(self.product_of_weights * child_weight)

    def get_position_data(self):
        node_data = [np.append(self.embedding, self.product_of_weights)]
        if not self.parents:
            return [node_data]
        parent_data = [parent.get_position_data() for parent in self.parents]
        
        # Combine data from parents correctly
        combined_data = [[node_data]] + list(zip(*parent_data))
        
        # Flatten the lists in combined_data
        combined_data = [sum(depth_data, []) for depth_data in combined_data]
        
        return combined_data

def reduce_data_with_pca(data, n_components=2):
    # Assuming data is a list of arrays where the last element is the product of weights
    embeddings = np.array([d[:-1] for d in data])
    contributions = np.array([d[-1] for d in data])

    # Apply PCA to reduce the dimensionality
    pca = PCA(n_components=n_components)
    reduced_embeddings = pca.fit_transform(embeddings)

    # Combine the reduced embeddings with the product of weights
    if n_components == 1:
        reduced_data = np.hstack([reduced_embeddings, contributions.reshape(-1, 1)])
    else:
        reduced_data = np.hstack([reduced_embeddings, contributions.reshape(-1, 1)])

    return reduced_data

def plot_3d_network(nodes, reduced_data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extract the x, y, z coordinates from reduced_data
    x_coords = reduced_data[:, 0]
    y_coords = reduced_data[:, 1]
    z_coords = reduced_data[:, 2]

    # Plot all the points (nodes)
    ax.scatter(x_coords, y_coords, z_coords, c='b', marker='o')

    # Draw lines between parents and children
    for i, node in enumerate(nodes):
        for parent in node.parents:
            parent_index = nodes.index(parent)
            ax.plot(
                [x_coords[i], x_coords[parent_index]],
                [y_coords[i], y_coords[parent_index]],
                [z_coords[i], z_coords[parent_index]],
                'k-'
            )

    ax.set_xlabel('PCA Component 1')
    ax.set_ylabel('PCA Component 2')
    
    # Use a more extreme log scale for the Z-axis with base 2
    ax.set_zscale('log', base=4)

    # Invert the Z-axis so smaller values are at the top
    ax.invert_zaxis()

    # Set custom Z-axis ticks and labels to cover a wider range
    z_ticks = np.array([1/2**i for i in range(0, int(np.log2(max(z_coords))) + 5)])  # Increased the range by +5
    ax.set_zticks(z_ticks)
    ax.get_zaxis().set_major_formatter(ticker.FuncFormatter(lambda val, _: f'{val:.4f}'))

    ax.set_zlabel('Product of Weights (Inverted, Log Scale)')

    plt.show()

def plot_2d_network(nodes, reduced_data):
    fig, ax = plt.subplots()

    # Extract the x and y coordinates from reduced_data
    x_coords = reduced_data[:, 0]
    y_coords = reduced_data[:, 1]

    # Create a dictionary to map nodes to their coordinates
    node_coords = {node: (x, y) for node, (x, y) in zip(nodes, zip(x_coords, y_coords))}

    # Sort nodes based on their original Z (product of weights) before inversion
    sorted_nodes = sorted(nodes, key=lambda n: n.product_of_weights, reverse=True)

    # Plot all the points (nodes)
    for node in sorted_nodes:
        x, y = node_coords[node]
        ax.scatter(x, y, c='b', marker='o')

    # Draw lines between parents and children based on the node_coords mapping
    for node in sorted_nodes:
        for parent in node.parents:
            parent_coord = node_coords[parent]
            node_coord = node_coords[node]
            ax.plot(
                [node_coord[0], parent_coord[0]],
                [node_coord[1], parent_coord[1]],
                'k-'
            )

    ax.set_xlabel('PCA Component 1')

    # Use a more extreme log scale for the Y-axis with base 2
    ax.set_yscale('log', base=4)

    # Invert the Y-axis so smaller values are at the top
    ax.invert_yaxis()

    # Set custom Y-axis ticks and labels to cover a wider range
    y_ticks = np.array([1/2**i for i in range(0, int(np.log2(max(y_coords))) + 5)])
    ax.set_yticks(y_ticks)
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda val, _: f'{val:.4f}'))

    ax.set_ylabel('Product of Weights (Inverted, Log Scale)')

    plt.show()

def collect_nodes(node):
    nodes = [node]
    for parent in node.parents:
        nodes.extend(collect_nodes(parent))
    return nodes

if __name__ == '__main__':
    # Create the tree with 10-dimensional embeddings
    tree = Node('', np.random.rand(10), [
        Node('', np.random.rand(10), [
            Node('', np.random.rand(10), []),
            Node('', np.random.rand(10), []),
            Node('', np.random.rand(10), []),
            Node('', np.random.rand(10), []),
            Node('', np.random.rand(10), [])
            ]),
        Node('', np.random.rand(10), [
            Node('', np.random.rand(10), []),
            Node('', np.random.rand(10), []),
            Node('', np.random.rand(10), [])
            ]),
        Node('', np.random.rand(10), [
            Node('', np.random.rand(10), []),
            Node('', np.random.rand(10), []),
            Node('', np.random.rand(10), [])
            ]),
        Node('', np.random.rand(10), [
            Node('', np.random.rand(10), []),
            Node('', np.random.rand(10), []),
            Node('', np.random.rand(10), []),
            Node('', np.random.rand(10), [])
            ])
        ])

    # Get position data
    data = tree.get_position_data()

    # Flatten the list of lists into a single list of vectors
    flat_data = [item for sublist in data for item in sublist]

    # Apply PCA reduction for 3D plot (2 components + product of weights)
    reduced_data_3d = reduce_data_with_pca(flat_data, n_components=2)

    # Apply PCA reduction for 2D plot (1 component + product of weights)
    reduced_data_2d = reduce_data_with_pca(flat_data, n_components=1)

    # Collect all nodes
    all_nodes = collect_nodes(tree)

    # Plot the 3D network
    plot_3d_network(all_nodes, reduced_data_3d)

    # Plot the 2D network
    plot_2d_network(all_nodes, reduced_data_2d)
