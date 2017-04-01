YELP DATASET PARSER
Created by Nick Stevens
4/1/2017

I didn't want to push the enormous json files to GitHub, but the yelp_dataset_parser 
should also have a yelp_dataset_challenge_round9 directory containing all of the 
datasets.

BUSINESS MEAN STARS
The business_mean_stars module is only intended to work with the file:
yelp_dataset_challenge_round9/yelp_academic_dataset_business.json

REVIEW KEYWORD PARSER
The review_keyword_parser module is only intended to work with the file:
yelp_dataset_challenge_round9/yelp_academic_dataset_review.json

The keyword stuff is really crude. It takes forever to run, and you'll probably have
to kill it because it also takes forever to stop. It will print a snippet of context
where a keyword appears in each review. This allows us to get a sense of whether or
not certain keywords are actually effective. Somebody really needs to clean up this
garbage code though.

It looks like maybe 7-8% of reviews contain the simple keywords from the list already
in there (excluding days of the week). No idea how many of these are false positives
though. Also, even though this isn't a large fraction of the reviews, there are still
more than 300,000 (out of 4 million) to work with.
