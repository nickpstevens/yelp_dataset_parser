import sys
import json
import re


# An (incomplete) list of keywords that can help determine when a reviewer's visit took place
# TODO: This should be extended to work with key phrases as well as single words.
# TODO: It won't work currently because of the set intersection operation.
KEYWORDS = [
    "today",
    "today's",
    "yesterday",
    "yesterday's",
    "morning",
    "morning's",
    "evening",
    "evening's",
    # "sunday",
    # "monday",
    # "tuesday",
    # "wednesday",
    # "thursday",
    # "friday",
    # "saturday",
]


def reviews_with_keywords(json_file, *keywords):
    if not keywords:
        keywords = KEYWORDS
    else:
        keywords = [x.lower() for x in keywords]

    keyword_set = set(keywords)
    with open(json_file) as f:
        reviews = []
        keyword_reviews = []
        word = r"[\w']+"
        for line in f:
            try:
                review = json.loads(line)
                reviews.append(review)
                review_text = review["text"].lower()
                if any(k in review_text for k in keywords):
                    word_list = re.findall(word, review_text)
                    # TODO: Can't use set intersection this way if we want to include both keywords and phrases
                    found_keywords = keyword_set.intersection(set(word_list))
                    if not found_keywords:
                        continue
                    keyword_reviews.append(review)
                    print "\nReview ID: " + str(review["review_id"])
                    for keyword in found_keywords:
                        context = n_surrounding_words(word_list, keyword, 8)
                        print "..." + " ".join(context) + "..."
            except ValueError as e:
                print e
    print "\nFraction of reviews with keywords: " + str(float(len(keyword_reviews)) / len(reviews))
    print "Number of reviews with keywords: " + str(len(keyword_reviews))
    print "Total number of reviews: " + str(len(reviews))


def n_surrounding_words(word_list, keyword, n):
    keyword_index = word_list.index(keyword)
    if keyword_index < n:
        left_n = keyword_index
    else:
        left_n = n
    last_index = len(word_list) - 1
    if last_index - keyword_index < n:
        right_n = last_index - keyword_index
    else:
        right_n = n
    return word_list[keyword_index - left_n:keyword_index + right_n]


def main(args):
    # The json_file for this has to be yelp_dataset_challenge_round9/yelp_academic_dataset_review.json
    json_file = args[1]
    if len(args) >= 3:
        keywords = args[2:]
        reviews_with_keywords(json_file, *keywords)
    else:
        reviews_with_keywords(json_file)


if __name__ == '__main__':
    main(sys.argv)
