import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

import dimension_reduction as dr
import paper_manager as pm
from analysis import basic_temporal_analysis as an
from analysis import manipulation as mal

from scrapping import author_scrape




# ======================= AUTHOR WORK OVER TIME ======================== #

#bert = pm.SciBERT()
#
#author = 'Albert Einstein'
#
#years = []
#embeddings = []
#
#with pm.db() as db:
#    author_id = db.insert(table='authors', row={'name': author}, format='dict') # gets existing id if the author already exists.
#    for paper in author_scrape.scrape_author(author):
#        embedding = bert.embed(paper['title'] + ': ' + paper['summary'])
#        db.insert(table='author_papers', row={'author_id': author_id, 'title': paper['title'], 'summary': paper['summary'], 'year': paper['year'], 'embedding': pm.translate(embedding)}, format='dict')
#        years.append(paper['year'])
#        embeddings.append(embedding)
#
#
#
#dimensions = mal.split_embeddings(embeddings)
#
#corr, cov = an.covariance(years, dimensions, embeddings=False)
#
#high_corr_index = sorted(range(len(corr)), key=lambda i : dimensions[i], reverse=True)[:3]
#high_cov_index =  sorted(range(len(cov)), key=lambda i : dimensions[i], reverse=True)[:3]
#
#print(f'High Correlation:\t{high_corr_index}\nHigh Covarience:\t{high_cov_index}')
#
#an.plot_dimensions(years, dimensions, high_corr_index + high_cov_index, embeddings=False)










# ================================ OLD ================================= #


#def assign_colors_and_labels(categories):
#    # Define a list of colors for the five most common categories
#    unique_colors = ["r", "g", "b", "c", "m"]
#    other_color = "y"
#    
#    # Count the frequency of each category
#    category_counts = Counter(categories)
#    
#    # Get the five most common categories
#    most_common_categories = [category for category, count in category_counts.most_common(5)]
#    
#    # Create a mapping of these categories to their respective colors
#    color_mapping = {category: unique_colors[i] for i, category in enumerate(most_common_categories)}
#    
#    # Assign the "other" color to all other categories
#    colors = [color_mapping.get(category, other_color) for category in categories]
#    
#    # Create labels for the legend
#    labels = {color: category for category, color in color_mapping.items()}
#    labels[other_color] = "Other"
#    
#    return colors, labels
#
#
#def plot_3_projections(proj1, proj2, proj3, colours, names, subtitles, labels):
#    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
#
#    # Plot the first projection
#    axes[0].scatter(proj1[:, 0], proj1[:, 1], c=colours, cmap='viridis')
#    axes[0].set_title(names[0])
#    axes[0].set_xlabel('X-axis')
#    axes[0].set_ylabel('Y-axis')
#    axes[0].text(0.5, -0.1, subtitles[0], ha='center', va='center', transform=axes[0].transAxes)
#
#    # Plot the second projection
#    axes[1].scatter(proj2[:, 0], proj2[:, 1], c=colours, cmap='viridis')
#    axes[1].set_title(names[1])
#    axes[1].set_xlabel('X-axis')
#    axes[1].set_ylabel('Y-axis')
#    axes[1].text(0.5, -0.1, subtitles[1], ha='center', va='center', transform=axes[1].transAxes)
#
#    # Plot the third projection
#    axes[2].scatter(proj3[:, 0], proj3[:, 1], c=colours, cmap='viridis')
#    axes[2].set_title(names[2])
#    axes[2].set_xlabel('X-axis')
#    axes[2].set_ylabel('Y-axis')
#    axes[2].text(0.5, -0.1, subtitles[2], ha='center', va='center', transform=axes[2].transAxes)
#
#
#    handles = [plt.Line2D([0], [0], marker='o', color='w', label=label,
#                          markerfacecolor=color, markersize=10) for color, label in labels.items()]
#    plt.legend(handles=handles, title="Categories")
#    plt.tight_layout()
#    plt.show()
#
#def main():
#    #pm.update_scibert()
#    # print(sum(int((paper[6]!=b'') and isinstance(paper[6], bytes))for paper in pm.access(table='full_test')))
#
#    positions, cats = zip(*[[pm.translate(n[6]), n[5].split('.')[0]] for n in pm.access(table='full_test')])
#    positions = np.array(positions)
#
#    check_for_nan(positions)
#
#    if len(positions.shape) == 3:
#        # If the shape is (n_samples, 1, 768), reshape it to (n_samples, 768)
#        n_samples = positions.shape[0]
#        positions = positions.reshape(n_samples, -1)
#    elif len(positions.shape) == 2:
#        # If the shape is already (n_samples, 768), use it directly
#        positions = positions
#    else:
#        raise ValueError("Unexpected data shape: {}".format(positions.shape))
#    print(f"Original shape of positions: {positions.shape}")
#
#    # pm.param_search(test_func, cost_func, data, n_tests=10, initial_lr=0.01, tolerance=1e-6, precision=1e-4, max_iter=1000, **ranges) 
#
#    pca_data = dr.reductions.apply_pca(positions)
#
#    tsne_params, tsne_data = dr.param_search(dr.reductions.apply_tsne, dr.cost.tsne, positions, perplexity=(5,50))
#
#    iso_params, iso_data = dr.param_search(dr.reductions.apply_isomap, dr.cost.isomap, positions, n_neighbors=(2,30))
#
#    cols, labels = assign_colors_and_labels(cats)
#
#    plot_3_projections(pca_data, tsne_data, iso_data, cols, ['PCA', 't-SNE', 'Isomap'], [' ', tsne_params, iso_params], labels)
#
#def check_for_nan(data):
#    if np.isnan(data).any():
#        raise ValueError("Data contains NaN values. Please check the data source.")
#    else:
#        print("No NaN values found in the data.")
#
#def get_shape():
#    embedding = pm.translate([n for n in pm.access(table='full_test', limit=1)][0][6])
#    print(embedding.shape)
#
#if __name__ == '__main__':
#    #get_shape()
#    main()
