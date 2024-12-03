import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from scipy.optimize import linear_sum_assignment

ground_truth = ['cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_1', 'cluster_1', 'cluster_1',  'cluster_2', 'cluster_2', 'cluster_2', 'cluster_2', 'cluster_2', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_4', 'cluster_5',]

output = ['cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_1', 'cluster_2', 'cluster_2', 'cluster_2', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_4', 'cluster_4', 'cluster_4', 'cluster_5', 'cluster_6', 'cluster_7']

true_labels = np.array(ground_truth)
predicted_labels = np.array(output)
labels = np.unique(np.concatenate((true_labels, predicted_labels)))
cm = confusion_matrix(true_labels, predicted_labels, labels=labels)

# Use Hungarian algorithm to reassign clusters
row_ind, col_ind = linear_sum_assignment(-cm)  # Negate to maximize match
reordered_cm = cm[:, col_ind] 

# Recalculate accuracy with reordered labels
accuracy = np.sum(np.diag(reordered_cm)) / np.sum(reordered_cm)

# Adjust label order for plotting
reordered_labels = labels[col_ind]

correct_mask = np.eye(len(labels), dtype=bool)
incorrect_mask = ~correct_mask

plt.figure(figsize=(9, 6))
sns.heatmap(
    reordered_cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    mask=incorrect_mask,
    xticklabels=reordered_labels,
    yticklabels=labels,
    cbar=True,
    cbar_kws={'format': ''}, 
    vmin=0,
    vmax=5
)
sns.heatmap(
    reordered_cm,
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
plt.title(f'Confusion Matrix (reordered) for the best threshold (0.65-0.7)\nAccuracy: {accuracy:.2f}')
plt.savefig('reordered_confusion_matrix.png', dpi=300)
# plt.show()