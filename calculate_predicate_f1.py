import argparse
import re


from tqdm import tqdm
from collections import Counter
from simplify_graph import get_all_nodes_pattern


def main():
    parser = argparse.ArgumentParser(
        description='Computes the precision, recall, and F1 on predicates '
                    'given the source and predicted graphs.'
    )
    parser.add_argument('source', type=str,
                        help='Source graphs.')
    parser.add_argument('predicted', type=str,
                        help='Predicted graphs.')
    parser.add_argument('--top', type=int, default=10,
            help='Prints top n predicates with debugging')
    parser.add_argument('--debug', action='store_true', default=False,
            help='Turns on debugging output.')
    args = parser.parse_args()


    with open(args.source, 'r') as source, open(args.predicted, 'r') as pred:
        labels = list(source.readlines())
        predictions = list(pred.readlines())

    gold_counts = get_counter()
    pred_counts = get_counter(correct=True)

    errors = {
        'surface': set(),
        'abstract': set(),
        'overpredicted': Counter(),
        'underpredicted': Counter()
    }
    sig_diff = []

    for i, (label, prediction) in tqdm(enumerate(zip(labels, predictions)), total=len(labels)):
        gold_surface, gold_abstract = get_predicates(label)
        pred_surface, pred_abstract = get_predicates(prediction)

        if args.debug:
            errors['surface'].update(gold_surface)
            errors['surface'].update(pred_surface)
            errors['abstract'].update(gold_abstract)
            errors['abstract'].update(pred_abstract)

            if len(label.split()) > len(prediction.split()) + 15:
                sig_diff.append((i, label, prediction))

        gold_counts['abstract'] += len(gold_abstract)
        gold_counts['surface'] += len(gold_surface)
        pred_counts['abstract']['total'] += len(pred_abstract)
        pred_counts['surface']['total'] += len(pred_surface)

        pred_counts['surface']['correct'] += count_correct(gold_surface,
                                                           pred_surface,
                                                           errors)
        pred_counts['abstract']['correct'] += count_correct(gold_abstract,
                                                            pred_abstract,
                                                            errors)

    print('Abstract results')
    print('------------------------------')
    precision = (pred_counts['abstract']['correct']
                 / pred_counts['abstract']['total'])
    recall = (pred_counts['abstract']['correct'] / gold_counts['abstract'])
    print('Precision: {:.2f}'.format(precision))
    print('Recall: {:.2f}'.format(recall))
    print('F1: {:.2f}\n'.format(2 * (precision * recall) / (precision + recall)))

    print('Surface results')
    print('------------------------------')
    precision = (pred_counts['surface']['correct']
                 / pred_counts['surface']['total'])
    recall = (pred_counts['surface']['correct'] / gold_counts['surface'])
    print('Precision: {:.2f}'.format(precision))
    print('Recall: {:.2f}'.format(recall))
    print('F1: {:.2f}\n'.format(2 * (precision * recall) / (precision + recall)))

    print('Total results')
    print('------------------------------')
    gold_total = sum(gold_counts.values())
    pred_correct = (pred_counts['abstract']['correct'] +
                    pred_counts['surface']['correct'])
    pred_total = (pred_counts['abstract']['total'] +
                  pred_counts['surface']['total'])
    precision = pred_correct / pred_total
    recall = pred_correct / gold_total
    print('Precision: {:.2f}'.format(precision))
    print('Recall: {:.2f}'.format(recall))
    print('F1: {:.2f}\n'.format(2 * (precision * recall) / (precision + recall)))

    if args.debug:
        print('Number of Abstract predicates: {}'.format(len(errors['abstract'])))
        print('Number of Surface predicates: {}'.format(len(errors['surface'])))
        print('Number of pairs with large length difference: {}'.format(len(sig_diff)))

        for key in ['overpredicted', 'underpredicted']:
            errors[key] = Counter({ pred : errors[key][pred]
                                    for pred in errors[key]
                                    if errors[key][pred] > 20 })
            print()
            print('Most commonly {} words:'.format(key))
            print(errors[key].most_common(args.top))


        print('importing ipdb for debugging purposes')
        import ipdb; ipdb.set_trace()


def count_correct(gold, pred, errors):
    correct = 0
    counts = Counter()
    counts.update(gold)
    for val in pred:
        if counts[val]:
            correct += 1
            counts[val] -= 1
        else:
            errors['overpredicted'][val] += 1
    for val in counts.keys():
        if counts[val] > 0:
            errors['underpredicted'][val] += 1
    return correct


def get_counter(correct=False):
    if correct:
        return {
            'abstract': {
                'total': 0,
                'correct': 0
            },
            'surface': {
                'total': 0,
                'correct': 0
            }
        }
    return { 'abstract': 0, 'surface': 0 }


def get_predicates(graph):
    """
    Return
    ------
    list, list
        Where the first list is the the list of surface predicates and the
        second is the list of abstract predicates
    """

    all_nodes_pattern = get_all_nodes_pattern()

    # Grabs the predicate from all nodes that match the pattern
    nodes = [matches[0][matches[0].rfind(' ') + 1:] for matches
             in all_nodes_pattern.findall(graph)]

    return ([pred for pred in nodes if pred.startswith('_')],
            [pred for pred in nodes if not pred.startswith('_')])


if __name__ == '__main__':
    main()
