import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from lifelines import CoxPHFitter
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Example genome vectors and decay rates
genome_vectors = np.array([
    [0.1, 0.2, 0.3],
    [0.3, 0.1, 0.2],
    [0.2, 0.3, 0.1],
    [0.1, 0.3, 0.2],
    [0.3, 0.2, 0.1],
    [0.2, 0.1, 0.3],
    [0.3, 0.2, 0.1]
])

decay_rates = np.array([0.2, 0.5, 0.3, 0.6, 0.8, 0.4, 0.7])
event = np.ones(len(decay_rates))  # All papers have an event

# Convert genome vectors to DataFrame
genome_df = pd.DataFrame(genome_vectors, columns=[f'Gene_{i+1}' for i in range(genome_vectors.shape[1])])

# Calculate correlation matrix
correlation_matrix = genome_df.corr()
print(correlation_matrix)

# Plot the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.show()

# Calculate VIF for each feature
vif_data = pd.DataFrame()
vif_data["feature"] = genome_df.columns
vif_data["VIF"] = [variance_inflation_factor(genome_df.values, i) for i in range(genome_df.shape[1])]
print(vif_data)

# Apply PCA if needed
n_components = 2  # Adjust based on the dataset's needs
pca = PCA(n_components=n_components)
genome_pca = pca.fit_transform(genome_vectors)

# Convert PCA components to DataFrame
pca_df = pd.DataFrame(genome_pca, columns=[f'PC{i+1}' for i in range(n_components)])
pca_df['Decay Rate'] = decay_rates
pca_df['Event'] = event

# Fit Cox Proportional-Hazards Model
cph = CoxPHFitter()

# Use PCA DataFrame for fitting
cph.fit(pca_df, duration_col='Decay Rate', event_col='Event')
cph.print_summary()

# Checking assumptions
cph.check_assumptions(pca_df)
