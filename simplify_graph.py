import argparse
import re
from collections import Counter
from tqdm import tqdm


global_graph = ""


def simplify(graph, instance_nodes):
    node_to_string = {}
    for node in instance_nodes:
        num, _, string = node.split()
        node_to_string[num] = string
        graph = re.sub(re.escape(node), string, graph)

    # Maps reentrancies to the original label with reentrancy marker, <*>,
    # preppended
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
    nodes_to_nums = { node[1] : (i + 1) * 1000
                      for i, node in enumerate(split_nodes) }

    # Renodes nodes:
    #     Special case since there can be multiple udef_q that are not
    #     reentrant
    for i, (pattern, (arg, label)) in enumerate(zip(instance_nodes, split_nodes)):
        val = nodes_to_nums[label]
        if 'udef_q' in label:
            val += i * 10
        repl = ' '.join([arg, str(val), '/', label])
        graph = re.sub(re.escape(pattern), repl, graph, count=1)

    reentrancies = re.findall('<\*> \w+', graph)
    reentrancies.sort(key=lambda x: -len(x))
    for reentrance in reentrancies:
        _, node = reentrance.split()
        reentrance = '<\*> ' + node
        graph = re.sub(reentrance, str(nodes_to_nums[node]), graph)

    return graph


def expand(graph):

    # Handle inter feat separation
    graph = re.sub('=', ' ', graph)

    # Handle intra feat separation
    intra_feature_pattern = re.compile('[\w-]:')
    intra_feats = set(intra_feature_pattern.findall(graph))
    for feat in intra_feats:
        repl = ' '.join(list(feat))
        graph = re.sub(feat, repl, graph)

    return graph


def squash(graph, features):
    inter_feature_pattern = re.compile('\w [\w-]')
    intra_feature_pattern = re.compile('[\w-] :')

    for i in range(len(features)):
        feature = features[i]
        feature_repl = feature

        # Find all instances we are looking to replace
        inter_feats = inter_feature_pattern.findall(feature)
        intra_feats = intra_feature_pattern.findall(feature)

        for intra, inter in zip(intra_feats, inter_feats):
            intra_repl = re.sub(' ', '', intra)
            inter_repl = re.sub(' ', '=', inter)
            feature_repl = re.sub(intra, intra_repl, feature_repl, count=1)
            feature_repl = re.sub(inter, inter_repl, feature_repl, count=1)

        # Handle fencepost since inter_feats has 1 extra element
        inter = inter_feats[-1]
        inter_repl = re.sub(' ', '=', inter)
        feature_repl = re.sub(inter, inter_repl, feature_repl, count=1)

        graph = re.sub(re.escape(feature), feature_repl, graph, count=1)

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
    last_seg = graph[nodes[-1].end():]

    # Note: This last segment must contain a closing paren since we assume that
    # the graph is well-formed
    paren_index = last_seg.find(')')
    span = last_seg[:paren_index]

    # Only adds the last span if it is a feature and not just ' '
    if span.strip():
        features.append(span)

    return features


def main():
    parser = argparse.ArgumentParser(
        description='Takes penman graphs and simplifies it for Neural '
                    'Net use or recovers it for SMatch evaluation.')
    parser.add_argument('input', type=str,
                        help='Input file.')
    parser.add_argument('output', type=str,
                        help='Output file.')
    parser.add_argument('--reverse', action='store_true', default=False,
                        help='Recovers a DMRS graph given the simplified version.')
    parser.add_argument('--feature-type', type=str, default='stable',
                        choices=['squash', 'expand', 'stable'],
                        help='Determines what the format the output features '
                             'should have. "squash" will concatenate features '
                             'into a single token. "expand" will unsquash '
                             'squashed features. "stable" will keep the format '
                             'of the features. (default="stable")')
    args = parser.parse_args()

    instance_nodes_pattern = get_instance_node_pattern(args.reverse)
    all_nodes_pattern = get_all_nodes_pattern()

    with open(args.input, 'r') as f, open(args.output, 'w') as output:
        lines = list(f.readlines())

        # Input should be in the format:
        # <original graph> \t <translation graph> \n
        for graphs in tqdm(lines):
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
                if args.feature_type == 'expand':
                    graph = expand(graph)
                elif args.feature_type == 'squash':
                    all_nodes = list(all_nodes_pattern.finditer(graph))
                    features = find_features(graph, all_nodes)
                    graph = squash(graph, features)

                graphs[i] = graph

            output.write('\t'.join(graphs))


def get_all_nodes_pattern():
    return re.compile('((:[\w-]*)?((\()|( <\*>)) [\w+]+( / [\w+]+)?)')


def get_instance_node_pattern(reverse=False):
    if reverse:
        return re.compile('((:[\w-]*)?\( [\w+]+)')
    else:
        return re.compile('\d{5} /\ [\w+]+')


if __name__ == '__main__':
    main()
