import sys
import json
import re
import os
from collections import defaultdict


BUSINESS_FIELDS = ['city', 'business_id', 'postal_code', 'stars', 'review_count']
REVIEW_FIELDS = ['user_id', 'business_id', 'stars', 'date']
USER_FIELDS = ['user_id', 'review_count', 'average_stars']

"""
The datasets that this creates are too big to push to GitHub, so you have to run this on your own.
Just execute the following command from the project root:
python src/filter_datasets.py 'yelp_dataset_challenge_round9/yelp_academic_dataset_business.json' 'yelp_dataset_challenge_round9/yelp_academic_dataset_review.json'
"""


def filter_data(business_file, review_file, user_file):
    business_out_path = 'modified_datasets/american_business.json'
    review_out_path = 'modified_datasets/american_review.json'
    user_out_path = 'modified_datasets/american_user.json'
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
                    # Only match on the the US cities.
                    if re.match('(28|29|44|88|89|53|85|15|61)[0-9]{3}', entry['postal_code']):
                        # Only take businesses with an ambience and price range
                        if entry['attributes'] and [string for string in entry['attributes'] if re.match("^RestaurantsPriceRange2:", string)] and [string for string in entry['attributes'] if re.match("^Ambience:", string)]:
                            business_ids.add(entry['business_id'])
                            entry['city'] = determine_city_from_business(entry)
                            to_write = {}
                            for field in BUSINESS_FIELDS:
                                to_write[field] = entry[field]
                            attributes = entry['attributes']
                            for attribute in attributes:
                                if re.match('^' + 'RestaurantsPriceRange2', attribute):
                                    to_write['RestaurantsPriceRange2'] = attribute[-1]
                                elif re.match('^' + 'Ambience', attribute):
                                    ambience = json.loads(attribute[10:].replace("'", '"').replace('False', '"False"').replace('True', '"True"'))
                                    for mood in ambience:
                                        to_write[mood] = ambience[mood]
                            write_line = json.dumps(to_write)
                            fout.write(write_line)
                            fout.write('\n')
                except ValueError as e:
                    print e
    user_ids = set()
    with open(review_file) as fin:
        with open(review_out_path, 'w+') as fout:
            for line in fin:
                try:
                    entry = json.loads(line)
                    if entry['business_id'] in business_ids and int(entry['date'][:4]) >= 2007 and int(entry['date'][:4]) < 2017:
                        user_ids.add(entry['user_id'])
                        to_write = {}
                        for field in REVIEW_FIELDS:
                            to_write[field] = entry[field]
                        fout.write(json.dumps(to_write))
                        fout.write('\n')
                except ValueError as e:
                    print e
    with open(user_file) as fin:
        with open(user_out_path, 'w+') as fout:
            for line in fin:
                try:
                    entry = json.loads(line)
                    if entry['user_id'] in user_ids:
                        to_write = {}
                        for field in USER_FIELDS:
                            to_write[field] = entry[field]
                        fout.write(json.dumps(to_write))
                        fout.write('\n')
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
    user_file = args[3]
    filter_data(business_file, review_file, user_file)


if __name__ == '__main__':
    main(sys.argv)
