import plotly.graph_objects as go


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



#class Article:
#    def __init__(self, title, x, y):
#        self.title = title
#        self.x = x
#        self.y = y
#
## Sample data
#articles = [
#    Article("Article 1", 1, 2),
#    Article("Article 2", 3, 4),
#    Article("Article 3", 5, 1),
#    Article("Article 4", 7, 6),
#    Article("Article 5", 4, 5)
#]
#
## Extracting data into lists for plotting
#titles = [article.title for article in articles]
#x_values = [article.x for article in articles]
#y_values = [article.y for article in articles]
#
#plot(titles, x_values, y_values)



