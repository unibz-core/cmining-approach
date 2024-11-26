import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import test_patterns
import test_graphClustering1

# Mining output containing the selected patterns (extracted from experiment 1 neutral trial)
PATTERNS_PATH = "outputpatterns.txt"

# Helper functions
def extract_cluster(list_of_lists):
    indexes = [item[1] for item in list_of_lists]
    return indexes

def extract_clusters(input_list):
    # Extract the second element from each sublist
    clusters = [item[1] for item in input_list]
    return clusters

def order_sublists_by_index(input_list):
    ordered_list = sorted(input_list, key=lambda x: x[0])
    return ordered_list

def add_indices_to_list(input_list):
    result_list = []
    for index, item in enumerate(input_list):
        result_list.append([index, item])
    return result_list

def extract_indexes(list_of_lists):
    indexes = [item[0] for item in list_of_lists]
    return indexes


ground_truth = ['cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_1', 'cluster_1', 'cluster_1',  'cluster_2', 'cluster_2', 'cluster_2', 'cluster_2', 'cluster_2', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_4', 'cluster_5',]

pattern_graphs = test_patterns.convertPatterns(PATTERNS_PATH)
list_of_vectors = test_graphClustering1.graphs2dataframes2vectors(pattern_graphs)
single_dataframe = test_graphClustering1.transform2singledataframe(list_of_vectors)
patterns_similarity_matrix = test_graphClustering1.calculate_similarity(single_dataframe)
grouped_items = test_graphClustering1.group_similar_items(patterns_similarity_matrix, 0.65)
output_ = extract_clusters(grouped_items)
print(output_)

ordered_grouped_items = order_sublists_by_index(grouped_items)
result = add_indices_to_list(ground_truth)
indexes = extract_indexes(result)

trend = [
            [0.1,0.22], [0.15,0.22], [0.2,0.22],[0.25,0.22], [0.3,0.22], [0.35,0.56], [0.4,0.61], 
            [0.45,0.68], [0.5,0.76], [0.6,0.9], [0.64,0.915], [0.65,0.96], [0.66,0.96], [0.67,0.96],
            [0.68,0.96], [0.69,0.96], [0.7,0.96], [0.71,0.94], [0.72,0.94], [0.73,0.93], [0.74,0.93], 
            [0.75,0.93], [0.8,0.88], [0.85,0.875], [0.9,0.85], [0.95,0.835], [0.99,0.83]
        ]

# Replace with clustering output of output_ (line 42)
output = ['cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_1', 'cluster_2', 'cluster_2', 'cluster_2', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_4', 'cluster_4', 'cluster_4', 'cluster_5', 'cluster_6', 'cluster_7']

first_numbers = [item[0] for item in trend]
second_numbers = [item[1] for item in trend]

# PLOT
colormap = plt.cm.Blues
plt.figure(figsize=(8, 7))
ax = sns.barplot(x=first_numbers,y=second_numbers, hue=first_numbers, palette=colormap(second_numbers), legend=False, alpha=1)
plt.xticks(rotation=90,color='#565656')
plt.xticks(fontsize=12)
ax.set_ylim(0, 1.05)
ax.set_yticklabels([])
for i, v in enumerate(second_numbers):
    ax.text(i, v + 0.01, str(v), ha='center', va='bottom', rotation=90, fontsize=12, color='#565656')
plt.xlabel('Clustering Threshold', fontsize=15)
plt.ylabel('Accuracy', fontsize=15)
plt.savefig('chart.png', dpi=300)

def calculate_accuracy(A, B, P):
    accuracy = 0
    numPairs = 0
    for i in P:
        for j in P:
            #Check if the 'cluster' values are equal for A and B
            checkPredicted = A[i][1] == A[j][1]
            checkReal = B[i][1] == B[j][1]
            
            if checkPredicted == checkReal:
                accuracy += 1
            numPairs += 1
    if numPairs == 0:
        return 0.0
    else:
        accuracy = accuracy / numPairs
        return accuracy

final_result = calculate_accuracy(ordered_grouped_items, result, indexes)
print("Accuracy:", final_result)