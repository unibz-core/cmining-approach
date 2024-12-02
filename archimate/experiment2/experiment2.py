from pathlib import Path
import subprocess
import os, time
import warnings
import timeout_decorator
import archimate.pipeline
import archimate.transform
import archimate.types
import utils.generateinput
import utils.graphClustering1
import utils.gspanMiner

DATASET_DIR = './archimate/50-models/'
INPUT_DIR = './input/'
PATTERNS_DIR = './patterns/'
PATTERNS_FILE = INPUT_DIR + 'outputpatterns.txt'
PLANTUML_JAR_PATH = "./utils/plantumlGenerator.jar"

GS_NODES = 3
GS_FREQ = 10
GSPAN_TIMEOUT = 600 # 10 minutes

def count_elements(models: list[dict]):
    total_elements = 0
    total_relationships = 0
    for model in models:
        elements = model.get('elements', [])
        total_elements += len(elements)
        relationships = model.get('relationships', [])
        total_relationships += len(relationships)
    print(f"Elements: {total_elements}, Relationships: {total_relationships}")

def run_test():
    start_time = time.perf_counter()
    ############# STEP 1 #############
    # IMPORT
    models = archimate.pipeline.import_models(DATASET_DIR)
    graphs = archimate.transform.create_graphs(models, INPUT_DIR)
    # FILTER
    new_graphs = utils.generateinput.process_graphs([], [], graphs)
    new_graphs_with_names = utils.generateinput.process_graphs_with_names([], [], graphs)
    # SAVE
    utils.generateinput.save_graphs_to_pickle(new_graphs, './input/graphs.pickle')
    utils.generateinput.graphs_to_data_file(new_graphs_with_names, 'graphs')
    ####################################
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print("------------------------------------------------------------------------")
    print(f"Total Models: {len(models)}, Dataset: {DATASET_DIR}")
    count_elements(models)
    print(f"Support: {GS_FREQ}, Nodes: {GS_NODES}")
    print("------------------------------------------------------------------------")
    print(f"[IMPORT] Execution time: {execution_time} seconds")
    


    start_time = time.perf_counter()
    ############# STEP 2 #############
    # setup gspan miner
    gsParameters = [GS_FREQ, GS_NODES]
    inputs = utils.gspanMiner.gsparameters(gsParameters)
    warnings.simplefilter(action='ignore', category=FutureWarning)
    @timeout_decorator.timeout(600)
    def run_gspan_with_timeout(inputs):
        return utils.gspanMiner.run_gspan(inputs)
    
    # MINING
    try:
        run_gspan_with_timeout(inputs)
    except timeout_decorator.timeout_decorator.TimeoutError:
        print("gSpan Miner execution timed out.")
    except Exception as e:
        print(f"Error: {e}")
    ####################################
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"[MINING] Execution time: {execution_time} seconds")


    start_time = time.perf_counter()
    ############# STEP 3 #############
    # load and process pattern graphs
    uploadgraphs = utils.patterns.load_graphs_from_pickle('./input/graphs.pickle')
    pattern_graphs = utils.patterns.convertPatterns(PATTERNS_FILE)

    # CLUSTERING
    patterns_features = utils.graphClustering1.graphs2dataframes2vectors(pattern_graphs)
    patterns_dataframe = utils.graphClustering1.transform2singledataframe(patterns_features)
    patterns_similarity_matrix = utils.graphClustering1.calculate_similarity(patterns_dataframe)
    similarity_threshold = float(0.9)
    patterns_cluster_labels = utils.graphClustering1.group_similar_items(patterns_similarity_matrix, similarity_threshold)
    pattern_graphs_clustered = utils.graphClustering1.merge_lists(patterns_cluster_labels, pattern_graphs)
    ####################################
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"[CLUSTERING] Execution time: {execution_time} seconds")


    start_time = time.perf_counter()
    ############# STEP 4 #############
    # VISUALIZATION
    cleaned_pattern_graphs = []
    # create plantUML diagram text file for each pattern
    for pattern in pattern_graphs_clustered:
        # file path: ./patterns/<cluster>/<pattern_support>_<pattern_index>.txt
        p_cluster_dir = os.path.join(PATTERNS_DIR, pattern[0]['pattern_cluster'])
        if not os.path.exists(p_cluster_dir):
            os.mkdir(p_cluster_dir)
        pattern_file = os.path.join(p_cluster_dir, f"{pattern[0]['pattern_support']}_{pattern[0]['pattern_index']}.txt")
        
        # bring pattern graph into standard graph structure 
        cleaned_pattern_graph = archimate.transform.clean_graph(pattern[1])
        cleaned_pattern_graphs.append(cleaned_pattern_graph)
        archimate.visualization.generate_diagram(cleaned_pattern_graph[0], cleaned_pattern_graph[1], pattern_file)
    
    # plantUML txt -> png left out
    '''
    generated_files = Path(PATTERNS_DIR).glob('**/*.txt')
    for idx, txt_file in enumerate(generated_files, start=0):
        cmd = f"java -jar {PLANTUML_JAR_PATH} {txt_file}"
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(f"Generated diagram for: {txt_file}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Could not generate diagram for {txt_file.name}: {e}")
    '''
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"[VISUALIZATION] Execution time: {execution_time} seconds")
    print("------------------------------------------------------------------------")
    print(f"Patterns found: {len(pattern_graphs)}")
    print("------------------------------------------------------------------------")

