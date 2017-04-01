import sys
import json
from collections import OrderedDict


def business_mean_stars_by_location(json_file, business_name, location_strata="postal_code"):
    business_name = business_name.lower()
    with open(json_file) as f:
        data = []
        for line in f:
            try:
                data.append(json.loads(line))
            except ValueError as e:
                print e
    strata_dict = stratified_data(data, "name", business_name, location_strata)

    val_col_width = 16
    print(location_strata.upper().ljust(26) + "NUM LOCATIONS".ljust(val_col_width)
          + "STAR AVG".ljust(val_col_width) + "AVG NUM REVIEWS".ljust(val_col_width))
    for strata, business_list in strata_dict.iteritems():
        if len(business_list) is not 0:
            num_businesses, star_avg, avg_num_reviews = strata_stats(business_list)
            print(strata.ljust(26) + str(num_businesses).ljust(val_col_width)
                  + ("%.2f" % star_avg).ljust(val_col_width)
                  + ("%.2f" % avg_num_reviews).ljust(val_col_width))
        else:
            continue


def stratified_data(data, common_attribute, common_value, stratify_by, sorted_by="location"):
    strata_dict = {}
    for x in data:
        if x[common_attribute].lower() == common_value:
            strata_dict.setdefault(x[stratify_by], []).append(x)
    if sorted_by == "location":
        return sort_by_location(strata_dict)
    else:
        # TODO: extend this to properly handle different types of sorting
        return sort_by(strata_dict, sorted_by)


def sort_by_location(strata_dict):
    sorted_by_latitude = OrderedDict(sorted(strata_dict.items(),
                                            key=lambda e:
                                            sum(float(e[1][i]["latitude"]) for i in xrange(len(e[1]))) / len(e[1])))
    sorted_by_location = OrderedDict(sorted(sorted_by_latitude.items(),
                                            key=lambda e:
                                            sum(float(e[1][j]["longitude"]) for j in xrange(len(e[1]))) / len(e[1])))
    return sorted_by_location


def sort_by(strata_dict, sort_attribute=None):
    if sort_attribute is None:
        return sorted(strata_dict)
    else:
        return OrderedDict(sorted(strata_dict.items(), key=lambda e: e[1][0][sort_attribute]))


def strata_stats(businesses):
    num_businesses = len(businesses)
    star_avg = sum(float(x["stars"]) for x in businesses) / num_businesses
    avg_num_reviews = sum(float(x["review_count"]) for x in businesses) / num_businesses
    return num_businesses, star_avg, avg_num_reviews


if __name__ == '__main__':
    # The json_file for this has to be yelp_dataset_challenge_round9/yelp_academic_dataset_business.json
    json_file = sys.argv[1]
    business_name = sys.argv[2]
    if len(sys.argv) > 3:
        location_strata = sys.argv[3]
        business_mean_stars_by_location(json_file, business_name, location_strata)
    else:
        business_mean_stars_by_location(json_file, business_name)
