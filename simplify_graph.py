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
    instance_nodes.sort(key=lambda x: -len(x))
    nodes = [node[1:] for node in instance_nodes]
    nodes_to_nums = { node : i + 1 for i, node in enumerate(nodes) }

    # Renodes nodes
    for pattern, node in zip(instance_nodes, nodes):
        repl = r'({} / {}'.format(nodes_to_nums[node], node)
        graph = re.sub('\\' + pattern, repl, graph)

    reentrancies = re.findall('<\*> \w*', graph)
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
    args = parser.parse_args()


    if args.reverse:
        instance_nodes_pattern = re.compile('\(\w*')
    else:
        instance_nodes_pattern = re.compile('\d{5} /\ \w*')


    with open(args.input, 'r') as f, open(args.output, 'w') as output:
        lines = list(f.readlines())

        # Input should be in the format:
        # #::id <num>
        # #::snt <sentence>
        # <graph>
        # \n
        for i in range(0, len(lines), 4):
            graph = lines[i + 2]

            # Grabs all the original nodes
            instance_nodes = list(instance_nodes_pattern.findall(graph))
            if not args.reverse:
                graph = simplify(graph, instance_nodes)
            else:
                graph = reverse(graph, instance_nodes)

            output.write(lines[i])
            output.write(lines[i + 1])
            output.write(graph)
            if i + 3 < len(lines):
                output.write(lines[i + 3])


if __name__ == '__main__':
    main()
