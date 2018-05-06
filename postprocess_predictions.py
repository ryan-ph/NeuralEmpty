import argparse


from tqdm import tqdm
from simplify_graph import get_all_nodes_pattern, \
                           get_instance_node_pattern, \
                           expand, filter_feats, reverse


def main():
    parser = argparse.ArgumentParser(
        description='Takes predicted file and converts it into a format that '
                    'can be evaluated using SMATCH.'
    )
    parser.add_argument('input', type=str,
                        help='Input file.')
    parser.add_argument('output', type=str,
                        help='Output file.')
    parser.add_argument('--remove-all-features', action='store_true',
                        help='Removes all features.')
    parser.add_argument('--include-features', nargs='+', default=[],
                        help='Features to include separated by spaces.')
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        predictions = f.readlines()

    # Reverse is true because model outputs simplified graphs
    instance_nodes_pattern = get_instance_node_pattern(reverse=True)
    all_nodes_pattern = get_all_nodes_pattern()

    with open(args.output, 'w') as output:
        for i, pred in enumerate(tqdm(predictions)):

            # Adds node labels
            instance_nodes = [node[0] for node
                              in list(instance_nodes_pattern.findall(pred))]
            pred = reverse(pred, instance_nodes)

            # Expanding features
            pred = expand(pred)

            # Filtering features
            pred = filter_feats(pred, args.include_features,
                                args.remove_all_features)

            # Write reversed, unsquashed graph to file
            output.write(pred)
            if i < len(predictions) - 1:
                output.write('\n')


if __name__ == '__main__':
    main()
