
import plotly.express as px
import pandas as pd

import plotly.graph_objects as go


# TODO
"""
- Check visualisation
"""

def plot(titles, x_vals, y_vals, categories):
    # Assign a unique color to each category
    category_list = list(set(categories))  # Create a list of unique categories
    colors = {category: f'hsl({i * (360 / len(category_list))}, 70%, 50%)' for i, category in enumerate(category_list)}

    # Create the scatter plot with color coding
    fig = go.Figure()
    for category in category_list:
        # Filter data points for each category
        idx = [i for i, cat in enumerate(categories) if cat == category]
        fig.add_trace(go.Scatter(
            x=[x_vals[i] for i in idx],
            y=[y_vals[i] for i in idx],
            mode='markers',
            marker=dict(size=10, color=colors[category]),
            text=[titles[i] for i in idx],
            name=category,  # Use category name for the legend
            hoverinfo='text'
        ))

    # Add titles and labels
    fig.update_layout(
        title='Interactive Scatter Plot of Articles',
        xaxis_title='X Coordinate',
        yaxis_title='Y Coordinate',
        legend_title="Category"
    )
    
    # Display the plot
    fig.show()



def visualize(dt):
    plot_data(dt.reduced_data['rand'], dt.categories, dt.titles, "Random Visualization")
    plot_data(dt.reduced_data['PCA'], dt.categories, dt.titles, "PCA Visualization")
    plot_data(dt.reduced_data['tsne'], dt.categories, dt.titles, "t-SNE Visualization")
    plot_data(dt.reduced_data['pca tsne'], dt.categories, dt.titles, "t-SNE on PCA Visualization")
    plot_data(dt.reduced_data['iso']isomap_data, dt.categories, dt.titles, "Isomap Visualization")
    plot_data(dt.reduced_data['pca iso'], dt.categories, dt.titles, "Isomap on PCA Visualization")
    plot_data(dt.reduced_data['hes'], dt.categories, dt.titles, "Hessian Eigenmap Visualization")
    plot_data(dt.reduced_data['pca hes'], dt.categories, dt.titles, "Hessian Eigenmap on PCA Visualization")

def plot_data(data, labels, titles, title):
    df = pd.DataFrame(data, columns=['x', 'y'])
    df['category'] = labels
    df['title'] = titles
    fig = px.scatter(df, x='x', y='y', color='category', hover_data=['title'], title=title)
    fig.show()
