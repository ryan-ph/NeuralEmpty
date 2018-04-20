import argparse
import re


from tqdm import tqdm
from simplify_graph import get_all_nodes_pattern, \
                           get_instance_node_pattern, \
                           expand, reverse


parser = argparse.ArgumentParser(
    description='Takes predicted file and converts it into a format that '
                'can be evaluated using SMATCH.'
)
parser.add_argument('input', type=str,
                    help='Input file.')
parser.add_argument('output', type=str,
                    help='Output file.')
args = parser.parse_args()

with open(args.input, 'r') as f:
    predictions = f.readlines()

# Reverse is true because model outputs simplified graphs
instance_nodes_pattern = get_instance_node_pattern(reverse=True)
all_nodes_pattern = get_all_nodes_pattern()

with open(args.output, 'w') as output:
    for i, pred in tqdm(enumerate(predictions)):

        # Adds node labels
        instance_nodes = [node[0] for node
                          in list(instance_nodes_pattern.findall(pred))]
        pred = reverse(pred, instance_nodes)

        # Expanding features
        pred = expand(pred)

        # Write reversed, unsquashed graph to file
        output.write(pred)
        if i < len(predictions) - 1:
            output.write('\n')
