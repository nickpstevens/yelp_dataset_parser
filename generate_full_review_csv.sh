 #!/bin/bash

python src/filter_datasets.py yelp_dataset_challenge_round9/yelp_academic_dataset_business.json yelp_dataset_challenge_round9/yelp_academic_dataset_review.json yelp_dataset_challenge_round9/yelp_academic_dataset_user.json

Rscript src/join-data.R

head -1000 modified_datasets/all_data.csv > modified_datasets/testset.csv
