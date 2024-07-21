import numpy as np
from scipy.spatial.distance import pdist, squareform
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor, _DistanceMatrix
from Bio import Phylo
import networkx as nx

# Define the tree as a dictionary
tree = {
    'node1': {'parents': [], 'children': ['node2', 'node3'], 'vector': [0.1, 0.2, 0.3]},
    'node2': {'parents': ['node1'], 'children': ['node4'], 'vector': [0.4, 0.5, 0.6]},
    'node3': {'parents': ['node1'], 'children': [], 'vector': [0.7, 0.8, 0.9]},
    'node4': {'parents': ['node2'], 'children': [], 'vector': [1.0, 1.1, 1.2]},
}

# Create a directed graph and add nodes and edges
G = nx.DiGraph()
G.add_node('node1', vector=[0.1, 0.2, 0.3])
G.add_node('node2', vector=[0.4, 0.5, 0.6])
G.add_node('node3', vector=[0.7, 0.8, 0.9])
G.add_node('node4', vector=[1.0, 1.1, 1.2])
G.add_edges_from([('node1', 'node2'), ('node1', 'node3'), ('node2', 'node4')])

# Create the vector array and compute the distance matrix
vector_array = [[1, 3, 4, 6, 3, 5, 3], [2, 4, 5, 6, 7, 7, 3], [3, 5, 8, 8, 6, 3, 6], 
                [2, 4, 6, 6, 7, 4, 2], [3, 5, 7, 7, 4, 3, 1], [2, 4, 6, 6, 8, 5, 2], 
                [5, 2, 3, 7, 1, 3, 1]]
dist_matrix = pdist(vector_array, metric='euclidean')
dist_matrix_square = squareform(dist_matrix)

# Check the size of the distance matrix
num_elements = dist_matrix_square.shape[0]

# Ensure that the number of nodes matches the size of the distance matrix
if num_elements != len(G.nodes):
    print(f"Number of elements in distance matrix: {num_elements}")
    print(f"Number of nodes in graph: {len(G.nodes)}")
    raise ValueError("The number of nodes and the size of the distance matrix do not match.")

# Convert the squareform distance matrix to a list of lists
dist_matrix_square_list = dist_matrix_square.tolist()

# Create the _DistanceMatrix object
distance_matrix = _DistanceMatrix(names=list(G.nodes), matrix=dist_matrix_square_list)

# Construct the tree using the Neighbor-Joining algorithm
constructor = DistanceTreeConstructor()
tree = constructor.nj(distance_matrix)

# Draw the tree
Phylo.draw(tree)




#
#import matplotlib.pyplot as plt
#nx.draw(G, with_labels=True, node_size=700, node_color='lightblue')
#plt.show()
#
#
#
#vectors = [G.nodes[node]['vector'] for node in G.nodes]
#vector_array = np.array(vectors)
#mean_vector = np.mean(vector_array, axis=0)
#var_vector = np.var(vector_array, axis=0)
#correlation_matrix = np.corrcoef(vector_array.T)
#
#
#betweenness_centrality = nx.betweenness_centrality(G)
#closeness_centrality = nx.closeness_centrality(G)
#
#
#from networkx.algorithms.community import greedy_modularity_communities
#
#communities = list(greedy_modularity_communities(G))
#
#import pandas as pd
#import seaborn as sns
#
## Example: Plotting centrality measures
#centrality_df = pd.DataFrame({
#    'Node': list(betweenness_centrality.keys()),
#    'Betweenness': list(betweenness_centrality.values()),
#    'Closeness': list(closeness_centrality.values())
#})
#sns.barplot(data=centrality_df, x='Node', y='Betweenness')
#plt.show()



