import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data = pd.read_csv('backend/data.csv')

# Preprocess data
X = data[['traffic', 'public_transport', 'carbon_emission', 'weather']]
X = pd.get_dummies(X, columns=['weather'], drop_first=True)

# Apply KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)
data['cluster'] = clusters

# Save clustered data
data.to_csv('backend/clustered_data.csv', index=False)

# Visualization
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='traffic', y='carbon_emission', hue='cluster', palette='viridis')
plt.title('Clustering of Routes Based on Traffic and Carbon Emission')
plt.xlabel('Traffic')
plt.ylabel('Carbon Emission')
plt.savefig('backend/visualizations/plots/clustering_routes.png')
plt.show()
