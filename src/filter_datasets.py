import sys
import json
import re
import os


"""
The datasets that this creates are too big to push to GitHub, so you have to run this on your own.
Just execute the following command from the project root:
python src/filter_datasets.py 'yelp_dataset_challenge_round9/yelp_academic_dataset_business.json' 'yelp_dataset_challenge_round9/yelp_academic_dataset_review.json'
"""


def filter_data(business_file, review_file):
    business_out_path = 'modified_datasets/american_business.json'
    review_out_path = 'modified_datasets/american_review.json'
    out_dir = os.path.dirname(business_out_path)
    try:
        os.makedirs(out_dir)
    except OSError:
        if not os.path.isdir(out_dir):
            raise
    business_ids = set()
    with open(business_file) as fin:
        with open(business_out_path, 'w+') as fout:
            for line in fin:
                try:
                    entry = json.loads(line)
                    if re.match('[0-9]{5}', entry['postal_code']):
                        business_ids.add(entry['business_id'])
                        fout.write(line)
                except ValueError as e:
                    print e
    with open(review_file) as fin:
        with open(review_out_path, 'w+') as fout:
            for line in fin:
                try:
                    entry = json.loads(line)
                    if entry['business_id'] in business_ids:
                        fout.write(line)
                except ValueError as e:
                    print e


def main(args):
    business_file = args[1]
    review_file = args[2]
    filter_data(business_file, review_file)


if __name__ == '__main__':
    main(sys.argv)
