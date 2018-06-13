"""
Typically run as

python train_test_split.py data/validation.txt data/training.txt ../cjp-article-tagging/lib
"""

import sys
import argparse

import nltk

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("validation_out_file", type=str,
                        help="path to file where validation data will be saved.")
    parser.add_argument("training_out_file", type=str,
                        help="path to file where training data will be saved.")
    parser.add_argument("tagnews_path", default=None,
                        help=("path to where the tagnews library can be imported. If not"
                              " provided, then the system installation will be used."))
    return parser

def main(validation_out_file, training_out_file):
    df = tagnews.load_data()
    df = df.loc[df['locations'].apply(bool), :]
    training_article_count = 0
    training_location_count = 0
    validation_article_count = 0
    validation_location_count = 0
    with open(validation_out_file, 'w', encoding='utf-8') as valid_f:
        with open(training_out_file, 'w', encoding='utf-8') as training_f:
            for idx, row in df.iterrows():
                txt = tagnews.utils.load_data.clean_string(row['bodytext'])
                spans = [loc['cleaned span'] for loc in row['locations'] if 'cleaned span' in loc]
                spans = sorted(spans, key=lambda span: span[0])
                to_delete = []
                for i, (span1, span2) in enumerate(zip(spans[:-1], spans[1:])):
                    if span1[1] > span2[0]:
                        to_delete.append(i)
                for i in to_delete[::-1]:
                    del spans[i]
                    print('Deleting overlapping spans.')
                prev_stop = 0
                s = ''
                for i, span in enumerate(spans):
                    start, stop = span
                    assert all([stop <= future_span[0] for future_span in spans[i+1:]])
                    s += '\n'.join([('{} {}'.format(word, '0'))
                                    for word in nltk.word_tokenize(txt[prev_stop:start])])
                    if prev_stop != start:
                        s += '\n'
                    s += '\n'.join([('{} {}'.format(word, '1'))
                                    for word in nltk.word_tokenize(txt[start:stop])])
                    if start != stop:
                        s += '\n'
                    prev_stop = stop
                s += '\n'.join([('{} {}'.format(word, '0'))
                                for word in nltk.word_tokenize(txt[prev_stop:])])
                if prev_stop != len(txt):
                    s += '\n'
                s += '\n'
                if idx % 2: # split half and half
                    training_f.write(s)
                    training_article_count += 1
                    training_location_count += len(spans)
                else:
                    valid_f.write(s)
                    validation_article_count += 1
                    validation_location_count += len(spans)

    print('Found {} articles for training'.format(training_article_count))
    print('Found {} locations for training'.format(training_location_count))
    print('Found {} articles for validaiton'.format(validation_article_count))
    print('Found {} locations for validation'.format(validation_location_count))

if __name__ == '__main__':
    parser = create_parser()
    p = parser.parse_args()
    if p.tagnews_path:
        sys.path = [p.tagnews_path] + sys.path
    import tagnews
    main(p.validation_out_file, p.training_out_file)
