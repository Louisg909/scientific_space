import matplotlib.pyplot as plt
import logging
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set up a logger for this submodule
logger = logging.getLogger(__name__)

# Define marker styles for different categories
category_markers = {
    'Category 1': 'o',  # Circle
    'Category 2': 'x',  # Cross
    'Category 3': 's',  # Square
    'Category 4': 'D',  # Diamond
    'Category 5': '^',  # Triangle up
    'Other': '*',       # Star for other categories
}

category_colours = {
    'Category 1': 'b',  # Circle
    'Category 2': 'g',  # Cross
    'Category 3': 'r',  # Square
    'Category 4': 'm',  # Diamond
    'Category 5': 'c',  # Triangle up
    'Other': 'k',       # Star for other categories
}

# Maximum number of categories before grouping others into "Other"
max_categories = len(category_markers) - 1

def plot(data_dict, categories):
    logger.debug("Starting plot function.")
    
    # We know there will always be 8 plots arranged in a 2x4 grid
    fig, axes = plt.subplots(2, 4, figsize=(24, 12))
    logger.debug("Created fixed 2x4 subplots.")
    
    # Flatten the axes array for easy iteration
    axes = axes.flatten()
    
    # Custom ordering for the axes: alternate between rows
    custom_order = [0, 4, 1, 5,
                    2, 6, 3, 7]
    ordered_axes = [axes[i] for i in custom_order]
    
    logger.debug(f"Custom axes order: {ordered_axes}")

    # Gather all unique categories
    unique_categories = set(categories)
    logger.debug(f"Unique categories: {unique_categories}")
    
    # If the number of unique categories exceeds max_categories, group the rest into "Other"
    if len(unique_categories) > max_categories:
        categories_sorted = sorted(list(unique_categories), key= lambda x : categories.count(x) , reverse=True)
        primary_categories = set(categories_sorted[:max_categories])
        logger.debug(f"Primary categories: {primary_categories}")
    else:
        primary_categories = unique_categories
    
    category_to_marker = {category: marker for category, marker in zip(primary_categories, category_markers.values())}
    category_to_colour = {category: colour for category, colour in zip(primary_categories, category_colours.values())}
    category_to_marker["Other"] = category_markers["Other"]  # Use the marker for "Other"
    category_to_colour["Other"] = category_colours["Other"]  # Use the marker for "Other"
    
    logger.debug(f"Category to marker mapping: {category_to_marker}")

    # Loop through the dictionary and create each subplot
    for idx, (title, content) in enumerate(data_dict.items()):
        ax = ordered_axes[idx]
        logger.debug(f"Processing plot {title}")
        
        # Plot the data points
        for point_idx, point in enumerate(content['data']):
            category = categories[point_idx]
            position = point
            if category in primary_categories:
                marker = category_to_marker[category]
                colour = category_to_colour[category]
            else:
                marker = category_to_marker["Other"]
                colour = category_to_colour["Other"]
                category = "Other"
            logger.debug(f"Plotting point {position} with marker {marker} and colour {colour} for category {category}")
            ax.scatter(position[0], position[1], label=category, marker=marker, color=colour)
        
        # Set the title of the subplot
        ax.set_title(title)
        
        # Display the info below the subplot
        ax.text(0.5, -0.1, str(content['info']), transform=ax.transAxes, 
                ha='center', fontsize=10)
        
        # Add legend only to the top-right plot
        if idx == 4:  # The 4th plot in the custom order (index 3 in custom_order)
            handles, labels = ax.get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            ax.legend(by_label.values(), by_label.keys(), loc='upper right')
        else:
            ax.legend().set_visible(False)  # Ensure other legends are not visible

    # Turn off any unused axes
    for ax in axes[len(data_dict):]:
        logger.debug(f"Turning off unused axis: {ax}")
        ax.axis('off')
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    logger.debug("Layout adjusted, ready to show the plot.")
    
    plt.show()
    logger.debug("Plot shown successfully.")

# Define marker styles for different categories
int_category_markers = {
    'Category 1': 'circle',
    'Category 2': 'x',
    'Category 3': 'square',
    'Category 4': 'diamond',
    'Category 5': 'triangle-up',
    'Other': 'star',
}

int_category_colours = {
    'Category 1': 'blue',
    'Category 2': 'green',
    'Category 3': 'red',
    'Category 4': 'magenta',
    'Category 5': 'cyan',
    'Other': 'black',
}

max_categories = len(int_category_markers) - 1

def plot_interactive(data_dict, categories, point_titles):
    # We know there will always be 8 plots arranged in a 2x4 grid
    fig = make_subplots(rows=2, cols=4, subplot_titles=list(data_dict.keys()), start_cell="top-left")

    # Custom ordering for the axes: top-left, bottom-left, top-second-left, bottom-second-left, etc.
    custom_order = [(1, 1), (2, 1), (1, 2), (2, 2),
                    (1, 3), (2, 3), (1, 4), (2, 4)]

    # Gather all unique categories
    unique_categories = set(categories)
    
    # If the number of unique categories exceeds max_categories, group the rest into "Other"
    if len(unique_categories) > max_categories:
        categories_sorted = sorted(list(unique_categories), key=lambda x: categories.count(x), reverse=True)
        primary_categories = set(categories_sorted[:max_categories])
    else:
        primary_categories = unique_categories

    category_to_marker = {category: marker for category, marker in zip(primary_categories, int_category_markers.values())}
    category_to_colour = {category: colour for category, colour in zip(primary_categories, int_category_colours.values())}
    category_to_marker["Other"] = int_category_markers["Other"]
    category_to_colour["Other"] = int_category_colours["Other"]

    # Loop through the dictionary and create each subplot
    for idx, (title, content) in enumerate(data_dict.items()):
        row, col = custom_order[idx]
        
        # Prepare data for the plot
        x_values = [point[0] for point in content['data']]
        y_values = [point[1] for point in content['data']]
        marker_symbols = []
        marker_colours = []
        hover_texts = []
        trace_names = []

        for point_idx, point in enumerate(content['data']):
            category = categories[point_idx]
            if category in primary_categories:
                marker = category_to_marker[category]
                colour = category_to_colour[category]
            else:
                marker = category_to_marker["Other"]
                colour = category_to_colour["Other"]
                category = "Other"

            marker_symbols.append(marker)
            marker_colours.append(colour)
            hover_texts.append(point_titles[point_idx])
            trace_names.append(category)

        # Add the scatter plot to the figure
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode='markers',
            marker=dict(symbol=marker_symbols, color=marker_colours),
            text=hover_texts,
            hoverinfo='text',
            showlegend=(idx == 0),  # Show legend only for the first plot
            legendgroup=category,   # Group traces by category for toggling
            name=category           # Use actual category names in the legend
        ), row=row, col=col)

        # Set the x-axis title
        fig.update_xaxes(title_text=str(content['info']), row=row, col=col)

    # Update layout for better spacing and title
    fig.update_layout(height=600, width=1200, title_text="Interactive Projections", clickmode='event+select')
    fig.show()

# Example usage:
if __name__ == '__main__':
    example_data = {
        "rand": {
            "info": "[301 762]",
            "data": [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
        },
        "pca": {
            "info": "{'perplexity': 27.5}",
            "data": [[2, 1], [4, 3], [6, 5], [8, 7], [10, 9]]
        },
        "tsne": {
            "info": "{'n_neighbors': 10.9999}",
            "data": [[2, 2], [4, 4], [6, 6], [8, 8], [10, 10]]
        },
        "pca_tsne": {
            "info": "Fillers because hessian doesn't like to work on big datasets.",
            "data": [[1, 1], [3, 3], [5, 5], [7, 7], [9, 9]]
        },
        "iso": {
            "info": "{'n_neighbors': 10.9999}",
            "data": [[1, 3], [3, 5], [5, 7], [7, 9], [9, 11]]
        },
        "pca_iso": {
            "info": "{'perplexity': 27.5}",
            "data": [[2, 3], [4, 5], [6, 7], [8, 9], [10, 11]]
        },
        "hes": {
            "info": "{'n_neighbors': 10.9999}",
            "data": [[3, 4], [5, 6], [7, 8], [9, 10], [11, 12]]
        },
        "hes again lol": {
            "info": "Fillers because hessian doesn't like to work on big datasets.",
            "data": [[4, 5], [6, 7], [8, 9], [10, 11], [12, 13]]
        }
    }
    
    example_categories = ["Category 1", "Category 2", "Category 3", "Category 4", "Category 5"]
    example_point_titles = ["Point A", "Point B", "Point C", "Point D", "Point E"]

    plot_interactive(example_data, example_categories, example_point_titles)

if __name__ == '__main__':
    # Example usage:
    example_data = {
        "Projection 1": {
            "info": "This is projection 1",
            "data": [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
        },
        "Projection 2": {
            "info": "This is projection 2",
            "data": [[2, 1], [4, 3], [6, 5], [8, 7], [10, 9]]
        },
        "Projection 3": {
            "info": "This is projection 3",
            "data": [[2, 2], [4, 4], [6, 6], [8, 8], [10, 10]]
        },
        "Projection 4": {
            "info": "This is projection 4",
            "data": [[1, 1], [3, 3], [5, 5], [7, 7], [9, 9]]
        },
        "Projection 5": {
            "info": "This is projection 5",
            "data": [[1, 3], [3, 5], [5, 7], [7, 9], [9, 11]]
        },
        "Projection 6": {
            "info": "This is projection 6",
            "data": [[2, 3], [4, 5], [6, 7], [8, 9], [10, 11]]
        },
        "Projection 7": {
            "info": "This is projection 7",
            "data": [[3, 4], [5, 6], [7, 8], [9, 10], [11, 12]]
        },
        "Projection 8": {
            "info": "This is projection 8",
            "data": [[4, 5], [6, 7], [8, 9], [10, 11], [12, 13]]
        }
    }
    
    example_categories = ["rand", "pca", "tsne", "pca_tsne", "iso", ""]
    example_point_titles = ["Point A", "Point B", "Point C", "Point D", "Point E"]

    plot_interactive(example_data, example_categories, example_point_titles)

