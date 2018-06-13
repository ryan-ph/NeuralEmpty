import argparse
import re


from tqdm import tqdm
from simplify_graph import get_all_nodes_pattern, \
                           get_instance_node_pattern, \
                           squash, simplify, find_features


parser = argparse.ArgumentParser(
    description='Takes the parsed input and outputs the data in squashed '
                'format in train, dev, and test datasets.'
)
parser.add_argument('input', type=str,
                    help='Input file.')
parser.add_argument('output', type=str,
                    help='Output path.')
args = parser.parse_args()


instance_nodes_pattern = get_instance_node_pattern()
all_nodes_pattern = get_all_nodes_pattern()


with open(args.input, 'r') as f:
    lines = list(f.readlines())

    # Input should be in the format:
    # <original graph> \t <translation graph> \n
    for j, graphs in enumerate(tqdm(lines)):
        graphs = graphs.split('\t')

        for i in range(len(graphs)):
            graph = graphs[i]

            # Grabs all instance nodes
            instance_nodes = list(instance_nodes_pattern.findall(graph))

            # Removes or adds node labels depending on flags
            graph = simplify(graph, instance_nodes)

            all_nodes = list(all_nodes_pattern.finditer(graph))
            features = find_features(graph, all_nodes)
            graph = squash(graph, features)

            graphs[i] = graph

        lines[j] = '\t'.join(graphs)

train_size = int(len(lines) * .8)
dev_size = int(len(lines) * .1)

train = lines[:train_size]
dev = lines[train_size:train_size + dev_size]
test = lines[train_size + dev_size:]

for dataset, path in zip([train, dev, test], ['train.txt', 'dev.txt', 'test.txt']):
    with open(args.output + path, 'w') as output:
        for line in dataset:
            output.write(line)
