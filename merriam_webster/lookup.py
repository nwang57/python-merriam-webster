from mwapi import LearnersApi
import argparse

Learners_key = "c3b787ec-8c72-47b5-b3f5-ae989507735d"

def setup_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("word", help="lookup the word in merriam webster")
    args = parser.parse_args()
    return args


def pretty_print(word_param):
    print("{0}  ({1})".format(word_param['word'], word_param['functional_label']))
    for idx, sense in enumerate(word_param['senses']):
        print('-' * 100)
        print("Definition %s %s" % (idx+1, sense['definition']))
        for ex_id, example in enumerate(sense['examples']):
            print("ex[%s]: %s" % (ex_id, example))

if __name__ == "__main__":
    args = setup_arguments()
    learners_api = LearnersApi(Learners_key)
    word_param = learners_api.lookup(args.word)
    pretty_print(word_param)
