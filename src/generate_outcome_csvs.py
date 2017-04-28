import sys
import json
import re
import csv
import os
from collections import OrderedDict


def outcome_csvs(business_file, review_file):
    city_businesses_map = map_cities_to_lists()
    business_id_city_map = {}
    with open(business_file) as fin:
        for line in fin:
            try:
                entry = json.loads(line)
                city = determine_city_from_business(entry)
                city_businesses_map[city].append(entry)
                business_id_city_map[entry['business_id']] = city
            except ValueError as e:
                print e

    outcome1_map = map_cities_to_dicts()
    with open(review_file) as fin:
        for line in fin:
            try:
                entry = json.loads(line)
                city = business_id_city_map[entry['business_id']]
                date = entry['date']

                try:
                    outcome1_map[city][date] += 1
                except KeyError:
                    outcome1_map[city][date] = 1
            except ValueError as e:
                print e
    for city, date_num_reviews_map in outcome1_map.iteritems():
       outcome1_map[city] = OrderedDict(sorted(date_num_reviews_map.items())) 
    outcome1_map = OrderedDict(sorted(outcome1_map.items()))

    write_map_to_csv(outcome1_map, 'outcome_csv/outcome1.csv')


def map_cities_to_lists():
    city_map = dict()
    city_map['charlotte'] = []
    city_map['cleveland'] = []
    city_map['las_vegas'] = []
    city_map['madison'] = []
    city_map['phoenix'] = []
    city_map['pittsburgh'] = []
    city_map['urbana'] = []
    return city_map


def map_cities_to_dicts():
    city_map = dict()
    city_map['charlotte'] = dict()
    city_map['cleveland'] = dict()
    city_map['las_vegas'] = dict()
    city_map['madison'] = dict()
    city_map['phoenix'] = dict()
    city_map['pittsburgh'] = dict()
    city_map['urbana'] = dict()
    return city_map


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


def write_map_to_csv(mapping, path):
    out_dir = os.path.dirname(path)
    try:
        os.makedirs(out_dir)
    except OSError:
        if not os.path.isdir(out_dir):
            raise
    with open(path, 'wb') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['city', 'date', 'review_count'])
        write_rows_recursive(f, writer, mapping, [])


def write_rows_recursive(f, writer, mapping, row_elements):
    for k, v in mapping.iteritems():
        if isinstance(v, dict):
            write_rows_recursive(f, writer, v, row_elements + [k])
        else:
            writer.writerow(row_elements + [k] + [v])


def main(args):
    business_file = args[1]
    review_file = args[2]
    outcome_csvs(business_file, review_file)


if __name__ == '__main__':
    main(sys.argv)
