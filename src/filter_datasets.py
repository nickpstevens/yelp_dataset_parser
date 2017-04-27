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
                    if re.match('(28|29|44|88|89|53|85|15|61)[0-9]{3}', entry['postal_code']):
                        business_ids.add(entry['business_id'])
                        entry['city'] = determine_city_from_business(entry)
                        write_line = json.dumps(entry)
                        fout.write(write_line)
                        fout.write('\n')
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


def determine_city_from_business(business):
    if re.match('2[89][0-9]{3}', business['postal_code']):
        return 'charlotte'
    elif re.match('44[0-9]{3}', business['postal_code']):
        return 'cleveland'
    elif re.match('8[89][0-9]{3}', business['postal_code']):
        return 'las_vegas'
    elif re.match('53[0-9]{3}', business['postal_code']):
        return 'madison'
    elif re.match('85[0-9]{3}', business['postal_code']):
        return 'phoenix'
    elif re.match('15[0-9]{3}', business['postal_code']):
        return 'pittsburgh'
    elif re.match('61[0-9]{3}', business['postal_code']):
        return 'urbana'
    else:
        return 'other'


def main(args):
    business_file = args[1]
    review_file = args[2]
    filter_data(business_file, review_file)


if __name__ == '__main__':
    main(sys.argv)
