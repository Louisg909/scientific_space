
import plotly.express as px
import pandas as pd


# TODO
"""
- Check visualisation
"""

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
