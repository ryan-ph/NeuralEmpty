import argparse
import re
from collections import Counter


'''((:[\w-]*)?(\( \d* / \w*))|(:[A-Z-]* [\d]+)'''


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


    with open(args.input, 'r') as f, open(args.output, 'w') as output:
        lines = list(f.readlines())

        # Input should be in the format:
        # <original graph> \t <translation graph> \n
        for graphs in lines:
            eng_graph, jpn_graph = graphs.split('\t')

            # Grabs all the original nodes
            eng_instance_nodes = list(instance_nodes_pattern.findall(eng_graph))
            jpn_instance_nodes = list(instance_nodes_pattern.findall(jpn_graph))

            # Only care about first match - for some reason, reverse option
            # will cause multiple matches
            if args.reverse:
                eng_instance_nodes = [node[0] for node in eng_instance_nodes]
                jpn_instance_nodes = [node[0] for node in jpn_instance_nodes]

            # Removes or adds node labels depending on flags
            if not args.reverse:
                eng_graph = simplify(eng_graph, eng_instance_nodes)
                jpn_graph = simplify(jpn_graph, jpn_instance_nodes)
            else:
                eng_graph = reverse(eng_graph, eng_instance_nodes)
                jpn_graph = reverse(jpn_graph, jpn_instance_nodes)

            output.write(eng_graph + '\t' + jpn_graph)


if __name__ == '__main__':
    main()
