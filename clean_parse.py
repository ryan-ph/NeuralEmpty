import argparse


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
args = parser.parse_args()


with open(args.input_lang1, 'r') as eng_text, \
     open(args.input_lang2, 'r') as jpn_text, \
     open(args.output, 'w') as output:
    eng_text = list(reversed(eng_text.readlines()))
    jpn_text = list(reversed(jpn_text.readlines()))
    while eng_text and jpn_text:
        eng_parse = []
        eng_header = []
        while eng_text[-1].strip():
            feat = eng_text.pop()
            if feat.strip().startswith('#'):
                eng_header.append(feat)
                continue
            else:
                feat = feat.strip()
            if not feat.strip().startswith(':lnk'):
                eng_parse.append(feat)
            elif feat.endswith(')'):
                paren_index = feat.find(')')
                eng_parse.append(eng_parse.pop()[:-1]
                                 + ' ' + feat[paren_index:])
        eng_text.pop()

        jpn_parse = []
        jpn_header = []
        while jpn_text[-1].strip():
            feat = jpn_text.pop()
            if feat.strip().startswith('#'):
                jpn_header.append(feat)
                continue
            else:
                feat = feat.strip()
            if not feat.startswith(':lnk'):
                jpn_parse.append(feat)
            elif feat.endswith(')'):
                paren_index = feat.find(')')
                jpn_parse.append(jpn_parse.pop()[:-1]
                                 + ' ' + feat[paren_index:])
        jpn_text.pop()

        if len(eng_parse) > 2 and len(jpn_parse) > 2:
            eng_graph = ' '.join(eng_parse)
            jpn_graph = ' '.join(jpn_parse)
            output.write(eng_graph + '\t' + jpn_graph + '\n')
