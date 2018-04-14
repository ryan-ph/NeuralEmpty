import argparse
import re
from collections import Counter


def simplify(graph, instance_nodes):
    node_to_string = {}
    for node in instance_nodes:
        num, _, string = node.split()
        node_to_string[num] = string
        graph = re.sub(node, string, graph)

    # Maps reentrancies to the original label appended with the string ' *'
    for node in node_to_string:
        graph = re.sub(node, '<*> ' + node_to_string[node], graph)

    return graph


def reverse(graph, instance_nodes):

    # Split nodes into argument and then node label and sorts so longest node
    # label is first
    split_nodes = [node.split() for node in instance_nodes]
    instance_nodes, split_nodes = zip(*sorted(zip(instance_nodes, split_nodes),
                                              key=lambda x: -len(x[1][1])))

    # Number labels
    nodes_to_nums = { node[1] : (i + 1) * 100
                      for i, node in enumerate(split_nodes) }

    # Renodes nodes
    for pattern, (arg, label) in zip(instance_nodes, split_nodes):
        repl = ' '.join([arg, str(nodes_to_nums[label]), '/', label])
        graph = re.sub(re.escape(pattern), repl, graph)

    reentrancies = re.findall('<\*> \w+', graph)
    reentrancies.sort(key=lambda x: -len(x))
    for reentrance in reentrancies:
        _, node = reentrance.split()
        reentrance = '<\*> ' + node
        graph = re.sub(reentrance, str(nodes_to_nums[node]), graph)

    return graph


def expand(graph, features):
    return graph


def squash(graph, features):
    return graph


def find_features(graph, nodes):

    features = []

    # Grabs all features from text except for last set of features
    for i in range(1, len(nodes), 1):
        start = nodes[i - 1].end()
        end = nodes[i].start()
        span = graph[start:end]
        if span.strip().startswith(':'):
            features.append(span)

    # Handles fencepost feature:
    last_seg = graph[matches[-1].end():]

    # Note: This last segment must contain a closing paren since we assume that
    # the graph is well-formed
    paren_index = last_seg.find(')')
    features.append(last_seg[:paren_index])

    return features


def main():
    parser = argparse.ArgumentParser(
        description='Takes penman graphs and simplifies it for Neural '
                    'Net use or recovers it for SMatch evaluation.')
    parser.add_argument('input', type=str,
                        help='Input file.')
    parser.add_argument('output', type=str,
                        help='Output file.')
    parser.add_argument('--reverse', action='store_true',
                        help='Recovers a DMRS graph given the simplified version.')
    parser.add_argument('--feature-type', type=str, default='stable',
                        choices=['squash', 'expand', 'stable'],
                        help='Determines what the format the output features '
                             'should have. "squash" will concatenate features '
                             'into a single token. "expand" will unsquash '
                             'squashed features. "stable" will keep the format '
                             'of the features. (default="stable")')
    args = parser.parse_args()

    if args.reverse:
        '''
        Regex for matching both instance and re-entrant nodes:
        ((:[\w-]*)?\( [\w]*)|((:[\w-]*) <\*> [\w]*)
        '''
        instance_nodes_pattern = re.compile('((:[\w-]*)?\( \w+)')
    else:
        instance_nodes_pattern = re.compile('\d{5} /\ \w*')

    all_nodes_pattern = re.compile('((:[\w-]*)?((\()|( <\*>)) \w+( / \w*)?)')

    with open(args.input, 'r') as f, open(args.output, 'w') as output:
        lines = list(f.readlines())

        # Input should be in the format:
        # <original graph> \t <translation graph> \n
        for graphs in lines:
            graphs = graphs.split('\t')
            for i in range(len(graphs)):
                graph = graphs[i]

                # Grabs all instance nodes
                instance_nodes = list(instance_nodes_pattern.findall(graph))

                # Only care about first match - for some reason, reverse option
                # will cause multiple matches
                if args.reverse:
                    instance_nodes = [node[0] for node in instance_nodes]

                # Removes or adds node labels depending on flags
                if not args.reverse:
                    graph = simplify(graph, instance_nodes)
                else:
                    graph = reverse(graph, instance_nodes)

                #  Handle features
                all_nodes = list(all_nodes_pattern.findall(graph))
                features = find_features(graph, all_nodes)
                if args.expand:
                    graph = expand(graph, features)
                elif args.squash:
                    graph = squash(graph, features)

                graphs[i] = graph

            output.write('\t'.join(graphs))


if __name__ == '__main__':
    main()
