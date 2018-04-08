import argparse


parser = argparse.ArgumentParser(
    description='Takes parallel penman graphs and removes entries in which '
                'graphs could not be generated.')
parser.add_argument('input_lang1', type=str,
                    help='File for original graphs in 1st language.')
parser.add_argument('input_lang2', type=str,
                    help='File for original graphs in 2st language.')
parser.add_argument('output_lang1', type=str,
                    help='Output file for graphs in 1st language.')
parser.add_argument('output_lang2', type=str,
                    help='Output file for graphs in 2st language.')
args = parser.parse_args()

with open(args.input_lang1, 'r') as eng_text, \
     open(args.input_lang2, 'r') as jpn_text, \
     open(args.output_lang1, 'w') as eng_clean, \
     open(args.output_lang2, 'w') as jpn_clean:
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
            eng_clean.write(''.join(eng_header))
            eng_clean.write(' '.join(eng_parse))
            eng_clean.write('\n\n')
            jpn_clean.write(''.join(jpn_header))
            jpn_clean.write(' '.join(jpn_parse))
            jpn_clean.write('\n\n')
