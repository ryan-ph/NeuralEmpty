import MeCab
import argparse


from tqdm import tqdm


mt = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")


def main():
    parser = argparse.ArgumentParser(
        description='Tokenizes inputs and filters out any sentences that are '
                    'too short (i.e. just titles, etc.) and invalid sentences.'
    )
    parser.add_argument('source', type=str,
                        help='Source language file.')
    parser.add_argument('target', type=str,
                        help='Target language path.')
    parser.add_argument('output_dir', type=str,
                        help='Directory where the output should go. The files '
                             'will have the same name as source and target.')
    args = parser.parse_args()

    with open(args.source, 'r') as engl, open(args.target, 'r') as jpn:
        engl_sentences = engl.readlines()
        jpn_sentences = jpn.readlines()

    total = len(engl_sentences)
    filtered = []

    for engl, jpn in tqdm(zip(engl_sentences, jpn_sentences), total=total):
        if '(' in engl or '（' in jpn or '(' in jpn:
            continue

        engl_tokens = engl.split()
        if len(engl_tokens) < 5:
            continue

        jpn_tokens = []
        parsed = mt.parseToNode(jpn)
        error = False
        while parsed:
            try:
                jpn_tokens.append(parsed.surface)
            except:
                error = True
                break
            parsed = parsed.next
        if error:
            continue

        jpn_split = ' '.join(jpn_tokens).strip()

        filtered.append((engl, jpn_split))

    source_out = args.output_dir + args.source[args.source.rfind('/') + 1:]
    target_out = args.output_dir + args.target[args.target.rfind('/') + 1:]

    with open(source_out, 'w') as engl, open(target_out, 'w') as jpn:
        for engl_sent, jpn_sent in tqdm(filtered):
            engl.write(engl_sent)
            jpn.write(jpn_sent)
            jpn.write('\n')



if __name__ == '__main__':
    main()
