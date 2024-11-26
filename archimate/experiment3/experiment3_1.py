import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

ground_truth = ['cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_1', 'cluster_1', 'cluster_1',  'cluster_2', 'cluster_2', 'cluster_2', 'cluster_2', 'cluster_2', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_4', 'cluster_5',]

output = ['cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_1', 'cluster_2', 'cluster_2', 'cluster_2', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_4', 'cluster_4', 'cluster_4', 'cluster_5', 'cluster_6', 'cluster_7']

true_labels = np.array(ground_truth)
predicted_labels = np.array(output)
labels = np.unique(np.concatenate((true_labels, predicted_labels)))
cm = confusion_matrix(true_labels, predicted_labels, labels=labels)
accuracy = np.sum(np.diag(cm)) / np.sum(cm)

correct_mask = np.eye(len(labels), dtype=bool)
incorrect_mask = ~correct_mask

# Plot Confusion Matrix
plt.figure(figsize=(9, 6))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    mask=incorrect_mask,  # Masking incorrect predictions
    xticklabels=labels,
    yticklabels=labels,
    cbar_kws={'format': ''}, 
    cbar=True,
    vmin=0,  # Set the minimum value of the color scale
    vmax=5,
)
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Reds",  # Color for correct predictions
    mask=correct_mask,  # Masking correct predictions
    xticklabels=labels,
    yticklabels=labels,
    cbar=False,
    vmin=0,  # Set the minimum value of the color scale
    vmax=5,
)
plt.xlabel('Predicted Clusters')
plt.ylabel('True Clusters')
plt.title(f'Confusion Matrix for the Best Threshold (0.65 - 0.7)\nAccuracy : 0.96')
plt.savefig('confusion_matrix.png', dpi=300)
plt.show()
