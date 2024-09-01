
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA


# Scrape and embed citation tree


# Get citation tree


# get contribution vectors and citation weights
def get_contributions(tree):
    # hmm idk

    contribution_pos = embeddings + contributions

    pca = PCA(n_components=2)
    reduced_embeddings = pca.fit_transform(embeddings)
    return embeddings, contributino_pos


# reduce all embeddings via pca (and maybe tsne?)




# plot vector diagram

def plot_vectors(vectors):
    """
    Plots a list of vectors in 2D space.

    Parameters:
    vectors (list of tuples): Each tuple contains two numpy arrays. 
                              The first array is the start of the vector,
                              and the second array is the end of the vector.
    """
    # Initialize a plot
    plt.figure()
    ax = plt.gca()

    # Lists to hold all x and y values for setting axis limits
    all_x = []
    all_y = []

    # Loop through each vector and plot it
    for start, end in vectors:
        # Calculate the vector components
        vector = end - start
        ax.quiver(start[0], start[1], vector[0], vector[1], angles='xy', scale_units='xy', scale=1)
        
        # Collect x and y values
        all_x.extend([start[0], end[0]])
        all_y.extend([start[1], end[1]])

    # Set the aspect of the plot to be equal
    ax.set_aspect('equal')

    # Determine the limits of the plot
    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(all_y), max(all_y)

    # Set the limits of the plot with a small margin
    plt.xlim(x_min - 1, x_max + 1)
    plt.ylim(y_min - 1, y_max + 1)

    # Set grid, labels, and title
    plt.grid(True)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('2D Vector Plot')

    # Show the plot
    plt.show()


# ============================== TESTING =============================== #
def test_plot():
    # Example usage
    vectors = [
        (np.array([0, 0]), np.array([1, 1])),
        (np.array([1, 1]), np.array([2, 0])),
        (np.array([2, 0]), np.array([3, 3])),
        (np.array([-1, -2]), np.array([1, 2])),
        (np.array([0, -1]), np.array([2, 1]))
    ]
    
    plot_vectors(vectors)


if __name__ == '__main__':
    test_plot()



