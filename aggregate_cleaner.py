import argparse
import re


def main():
    parser = argparse.ArgumentParser(
        description='Takes parallel penman graphs and removes entries in which '
                    'graphs could not be generated. Keeps only graphs with '
                    'were able to be parsed in both languages')
    parser.add_argument('input_lang1', type=str,
                        help='File for the first language graphs.')
    parser.add_argument('input_lang2', type=str,
                        help='File for the second language graphs.')
    parser.add_argument('output1', type=str,
                        help='Output file for the first language.')
    parser.add_argument('output2', type=str,
                        help='Output file for the second language.')
    args = parser.parse_args()

    with open(args.input_lang1, 'r') as text:
        text = list(reversed(text.readlines()))
        eng_id = map_parses(text)

    with open(args.input_lang2, 'r') as text:
        text = list(reversed(text.readlines()))
        jpn_id = map_parses(text)

    # Set intersction between the graph IDs
    common_keys = list(eng_id.keys() & jpn_id.keys())

    with open(args.output1, 'a') as lang1, \
        open(args.output2, 'a') as lang2:
        for key in common_keys:
            eng_graph = ' '.join(eng_id[key])
            jpn_graph = ' '.join(jpn_id[key])
            lang1.write(eng_graph)
            lang1.write('\n')
            lang2.write(jpn_graph)
            lang2.write('\n')


def map_parses(graphs):
    id_map = {}
    while graphs:
        parse = []
        while graphs and graphs[-1].strip():
            feat = graphs.pop().strip()

            if feat.startswith('# ::id'):
                id_map[feat] = parse
            else:
                parse.append(feat)

        # pop off space separating graphs
        if graphs:
            graphs.pop()
    return id_map


if __name__ == '__main__':
    main()
