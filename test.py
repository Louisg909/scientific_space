
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

def assign_colors_and_labels(categories):
    # Define a list of colors for the five most common categories
    unique_colors = ["r", "g", "b", "c", "m"]
    other_color = "y"
    
    # Count the frequency of each category
    category_counts = Counter(categories)
    
    # Get the five most common categories
    most_common_categories = [category for category, count in category_counts.most_common(5)]
    
    # Create a mapping of these categories to their respective colors
    color_mapping = {category: unique_colors[i] for i, category in enumerate(most_common_categories)}
    
    # Assign the "other" color to all other categories
    colors = [color_mapping.get(category, other_color) for category in categories]
    
    # Create labels for the legend
    labels = {color: category for category, color in color_mapping.items()}
    labels[other_color] = "Other"
    
    return colors, labels

# Example usage
categories = ["cat1", "cat2", "cat1", "cat3", "cat2", "cat1", "cat4", "cat5", "cat6", "cat7", "cat2", "cat1"]
colors, labels = assign_colors_and_labels(categories)

# Example of how to use it in a scatter plot
x = np.random.rand(len(categories))
y = np.random.rand(len(categories))

plt.scatter(x, y, c=colors)

# Create the legend
handles = [plt.Line2D([0], [0], marker='o', color='w', label=label,
                      markerfacecolor=color, markersize=10) for color, label in labels.items()]
plt.legend(handles=handles, title="Categories")

plt.show()
