import argparse
import re


parser = argparse.ArgumentParser(
    description='Takes parallel penman graphs and removes entries in which '
                'graphs could not be generated. Output format will be a '
                'translation pair per line where the translations are '
                'separated by a tab character.')
parser.add_argument('input_lang1', type=str,
                    help='File for original graphs in 1st language.')
parser.add_argument('input_lang2', type=str,
                    help='File for original graphs in 2st language.')
parser.add_argument('output', type=str,
                    help='Output file for the cleaned data.')
parser.add_argument('--full', action='store_true',
                    help='Keeps all features of the DMRS graph. Defaults to '
                         'false.')
args = parser.parse_args()


with open(args.input_lang1, 'r') as eng_text, \
     open(args.input_lang2, 'r') as jpn_text, \
     open(args.output, 'w') as output:
    eng_text = list(reversed(eng_text.readlines()))
    jpn_text = list(reversed(jpn_text.readlines()))
    while eng_text and jpn_text:
        eng_parse = []
        while eng_text and eng_text[-1].strip():
            feat = eng_text.pop().strip()

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
                    prev = eng_parse.pop()
                    eng_parse.append(prev + feat[paren_index + 2:])

            # keep everything else if we need the full representation
            elif args.full:
                eng_parse.append(feat)
            else:

                # if it a node
                if re.match('(^\()|(^(:[A-Z]))', feat):
                    eng_parse.append(feat)

                # or has closing parens
                elif feat.endswith(')'):
                    paren_index = feat.find(' )')
                    prev = eng_parse.pop()
                    eng_parse.append(prev + feat[paren_index:])

        # pop off space separating graphs
        if eng_text:
            eng_text.pop()

        jpn_parse = []
        while jpn_text and jpn_text[-1].strip():
            feat = jpn_text.pop().strip()

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
                    prev = jpn_parse.pop()
                    jpn_parse.append(prev + feat[paren_index + 2:])

            # keep everything else if we need the full representation
            elif args.full:
                jpn_parse.append(feat)
            else:

                # if it a node
                if re.match('(^\()|(^(:[A-Z]))', feat):
                    jpn_parse.append(feat)

                # or has closing parens
                elif feat.endswith(')'):
                    paren_index = feat.find(' )')
                    prev = jpn_parse.pop()
                    jpn_parse.append(prev + feat[paren_index:])

        # pop off space separating graphs
        if jpn_text:
            jpn_text.pop()

        if len(eng_parse) > 2 and len(jpn_parse) > 2:
            eng_graph = ' '.join(eng_parse)
            jpn_graph = ' '.join(jpn_parse)
            output.write(eng_graph + '\t' + jpn_graph + '\n')
