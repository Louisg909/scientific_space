
from collections import defaultdict
from itertools import zip_longest
import numpy as np
import matplotlib.pyplot as plt
from .manipulation import split_embeddings

# ========================== LINEAR ANALYSIS =========================== #

# For things like an author's contribution vectors, and embeddings of works in a dicipline over time.

def plot(years, vectors, embeddings=True):
    max_plots = 6 

    if embeddings:
        # Transform embeddings
        dimension_vals = split_embeddings(vectors)
    else:
        dimension_vals = vectors

    # Create a list of unique years and calculate averages
    unique_years = sorted(list(set(years)))
    averages = {year: [0] * len(dimension_vals) for year in unique_years}
    counts = {year: 0 for year in unique_years}

    for i, year in enumerate(years):
        for j in range(len(dimension_vals)):
            averages[year][j] += dimension_vals[j][i]
        counts[year] += 1

    for year in unique_years:
        averages[year] = [val / counts[year] for val in averages[year]]

    # Determine the number of dimensions to plot per subplot
    num_dimensions = len(dimension_vals)
    dimensions_per_plot = max(1, num_dimensions // max_plots + (num_dimensions % max_plots > 0))

    fig, axes = plt.subplots(3, 2, figsize=(14, 18), sharex=True)
    axes = axes.flatten()

    # Plot each group of dimensions
    for plot_index in range(max_plots):
        start_dim = plot_index * dimensions_per_plot
        end_dim = min((plot_index + 1) * dimensions_per_plot, num_dimensions)
        
        if start_dim >= end_dim:
            break
        
        ax = axes[plot_index]
        
        for i in range(start_dim, end_dim):
            dim_values = dimension_vals[i]
            # Scatter plot for individual points
            ax.scatter(years, dim_values, label=f'Dimension {i+1} Data Points')
            
            # Line plot for average values without markers
            avg_values = [averages[year][i] for year in unique_years]
            ax.plot(unique_years, avg_values, linestyle='-', label=f'Dimension {i+1} Average')
        
        ax.set_title(f'Dimensions {start_dim+1} to {end_dim} Over Years')
        ax.set_xlabel('Year')
        ax.set_ylabel('Value')
        ax.legend()
        ax.grid(True)

    plt.tight_layout()
    plt.show()

def plot_dimensions(years, vectors, dimensions_to_plot, embeddings=True):
    max_plots = 6
    dimensions_to_plot = dimensions_to_plot[:max_plots]  # Ensure no more than 6 dimensions

    if embeddings:
        # Transform embeddings
        dimension_vals = split_embeddings(vectors)
    else:
        dimension_vals = vectors

    # Create a list of unique years and calculate averages
    unique_years = sorted(list(set(years)))
    averages = {year: [0] * len(dimension_vals) for year in unique_years}
    counts = {year: 0 for year in unique_years}

    for i, year in enumerate(years):
        for j in range(len(dimension_vals)):
            averages[year][j] += dimension_vals[j][i]
        counts[year] += 1

    for year in unique_years:
        averages[year] = [val / counts[year] for val in averages[year]]

    fig, axes = plt.subplots(len(dimensions_to_plot), 1, figsize=(14, 18), sharex=True)

    if len(dimensions_to_plot) == 1:
        axes = [axes]  # Ensure axes is always a list for consistency

    # Plot each specified dimension
    for plot_index, dim in enumerate(dimensions_to_plot):
        ax = axes[plot_index]
        
        dim_values = dimension_vals[dim - 1]
        # Scatter plot for individual points
        ax.scatter(years, dim_values, label=f'Dimension {dim} Data Points')
        
        # Line plot for average values without markers
        avg_values = [averages[year][dim - 1] for year in unique_years]
        ax.plot(unique_years, avg_values, linestyle='-', label=f'Dimension {dim} Average')
        
        ax.set_title(f'Dimension {dim} Over Years')
        ax.set_ylabel('Value')
        ax.legend()
        ax.grid(True)

    # Set x-label for the bottom axis only
    axes[-1].set_xlabel('Year')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # Example usage
    years = [2000, 2001, 2002, 2003, 2000, 2001, 2002, 2003, 2000, 2001, 2002, 2003, 2000, 2001, 2002, 2003]
    embeddings = [
        [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7, 2.9, 3.1],
        [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2],
        [0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7, 2.9, 3.1, 3.3],
        [0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4],
        [0.15, 0.35, 0.55, 0.75, 0.95, 1.15, 1.35, 1.55, 1.75, 1.95, 2.15, 2.35, 2.55, 2.75, 2.95, 3.15],
        [0.25, 0.45, 0.65, 0.85, 1.05, 1.25, 1.45, 1.65, 1.85, 2.05, 2.25, 2.45, 2.65, 2.85, 3.05, 3.25],
        [0.35, 0.55, 0.75, 0.95, 1.15, 1.35, 1.55, 1.75, 1.95, 2.15, 2.35, 2.55, 2.75, 2.95, 3.15, 3.35],
        [0.45, 0.65, 0.85, 1.05, 1.25, 1.45, 1.65, 1.85, 2.05, 2.25, 2.45, 2.65, 2.85, 3.05, 3.25, 3.45],
        [0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7, 2.9, 3.1, 3.3, 3.5],
        [0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6],
        [0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7, 2.9, 3.1, 3.3, 3.5, 3.7],
        [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8],
        [0.85, 1.05, 1.25, 1.45, 1.65, 1.85, 2.05, 2.25, 2.45, 2.65, 2.85, 3.05, 3.25, 3.45, 3.65, 3.85],
        [0.95, 1.15, 1.35, 1.55, 1.75, 1.95, 2.15, 2.35, 2.55, 2.75, 2.95, 3.15, 3.35, 3.55, 3.75, 3.95],
        [1.05, 1.25, 1.45, 1.65, 1.85, 2.05, 2.25, 2.45, 2.65, 2.85, 3.05, 3.25, 3.45, 3.65, 3.85, 4.05],
        [1.15, 1.35, 1.55, 1.75, 1.95, 2.15, 2.35, 2.55, 2.75, 2.95, 3.15, 3.35, 3.55, 3.75, 3.95, 4.15]
    ]
    
    plot(years, embeddings)




def covariance(years, vectors, embeddings=True):
    if embeddings:
        dimension_vals = split_embeddings(vectors)
    else:
        dimension_vals = vectors

    correlation = []
    covariance = []
    
    for vals in dimension_vals:
        covariance.append(np.cov(vals, years)[0, 1])
        correlation.append(np.corrcoef(vals, years)[0, 1])

    return correlation, covariance




if __name__ == '1__main__':
    # Example usage
    years = [2022, 2001, 1952, 1995, 1988, 2005, 2010, 2015, 2000, 1990]
    embeddings = [
        [1, -3, 3],
        [2, 0, 4],
        [5, 2, 7],
        [3, 2, 5],
        [2, -2, 4],
        [5, 1, 7],
        [7, 12, 9],
        [8, 5, 10],
        [4, 1, 6],
        [2, 8, 4]
    ]
    
    cor, cov = covariance(years, embeddings)
    
    print(cov)
    print(cor)

    plot(years, embeddings)













