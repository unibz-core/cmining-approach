# Mining Frequent Structures in Conceptual Models

This `README` provides instructions for conducting experiments and demonstrations using the CM-Mining application. Please refer to the paper *"Mining Frequent Structures in Conceptual Models"* (under review) for additional details, specifically sections 6 and 7.

## Installation

1. Visit [CM-Mining GitHub Repository](https://github.com/unibz-core/CM-Mining).
2. Follow the installation instructions provided in the repository to install the application.

## Experiment Instructions (OntoUML)

The OntoUML experiments can be found in the `ontouml` directory.

### Experiment 1

1. Copy the `models` directory into the application root directory.
2. Run each of the 6 trials discussed in the paper by applying the parameters specified in the `parameters.txt` file.

### Experiment 2

1. Copy the `models` directory into the application root directory.
2. Run the two trials (first with 47 models, second with 94) by executing the `test.py` file.
   - Use the nodes and frequency parameters described in the corresponding experiment section (refer to Table 5).
   - Generate a performance report using: `python3 -m cProfile test.py > test.txt`.

### Experiment 3

The `outputpatterns.txt` file represents the list of patterns to be clustered.

1. Run `test_confusionmatrix.py` to generate the data discussed in the corresponding section.

## Experiment Instructions (ArchiMate)

The ArchiMate experiments can be found in the `archimate` directory.

### Experiment 1

1. Copy the `models` directory into the application root directory.
2. Run each of the 6 trials discussed in the paper by applying the parameters specified in the `parameters.txt` file.

The output of the trials can be found in the `output` directory.

### Experiment 2

1. Copy the two dataset directories (`50-models` and `100-models`) into the application root directory.
2. Run the two trials (first with 50 models, second with 100) by executing the `experiment2.py` file.
   - Use the nodes and frequency parameters described in the corresponding experiment section (refer to Table 6).
   - The execution time of each module can be seen in the program's output.

### Experiment 3

The `outputpatterns.txt` file represents the list of patterns to be clustered.

1. Run `experiment3.py` to generate the data discussed in the corresponding section.
2. Run `experiment3_1.py` to generate the confusion matrix.


## Demonstration (OntoUML)

This section provides a complete set of models and 5 trials used to generate the list of patterns.

- Each trial folder contains:
  - Parameters used
  - Generated graphs
  - Generated patterns

Feel free to explore these folders to understand the experiments conducted and the outcomes achieved.

For any further details or inquiries, refer to the paper's Sections 6 and 7 or consult the repository's documentation.

## Note

Ensure the application is set up correctly and all dependencies are installed before executing the experiments or demonstrations.

