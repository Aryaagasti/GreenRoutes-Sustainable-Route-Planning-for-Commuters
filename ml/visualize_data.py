import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load dataset
data = pd.read_csv('backend/data.csv')

# Create visualizations
plt.figure(figsize=(10, 6))
sns.lineplot(data=data, x='date', y='carbon_emission')
plt.title('Carbon Emission Over Time')
plt.xlabel('Date')
plt.ylabel('Carbon Emission')

# Save the plot as a static PNG file
plt.savefig('backend/visualizations/plots/carbon_emission_over_time.png')

# Show the plot
plt.show()
