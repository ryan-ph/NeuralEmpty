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


def map_parses(graphs):
    id_map = {}
    while graphs:
        parse = []
        while graphs and graphs[-1].strip():
            feat = graphs.pop().strip()

            if feat.startswith('# ::id'):
                id_map[feat] = parse

            # skip sentence id and sentence as well as concrete args
            if feat.startswith('#') or feat.startswith(':carg'):
                continue

            # separate opening paren from graph root
            if feat.startswith('('):
                feat = feat.replace('(', '( ')

            # attach opening paren to node rather than label
            elif '(' in feat:
                feat = feat.replace(' (', '( ')

            # splits a part closing brackets
            if feat.endswith(')'):
                feat = re.sub('\)', ' )', feat)

            # remove lines that have lnk while preserving closing brackets
            if feat.startswith(':lnk'):

                # append closing brackets to previous feature
                if feat.endswith(')'):
                    paren_index = feat.find('>"')
                    prev = parse.pop()
                    parse.append(prev + feat[paren_index + 2:])

        # pop off space separating graphs
        if graph:
            graph.pop()


if __name__ == '__main__':
    main()
