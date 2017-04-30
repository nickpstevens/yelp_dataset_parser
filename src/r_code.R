library(plyr)
library(Hmisc)
library(simFrame)

check_positivity <- function(strata) {
  # Check for positivity
  # strata@size is list with sizes of each strata ([4 7 4 5])
  return(all(strata@size>0))
}

get_subset <- function(df, strata, strata_id) {
  # Returns data frame with subsets of original data
  
  # These are row numbers for the strata
  element_numbers <- strata@split[[strata_id]]
  # And then we get the rows themselves
  return(df[element_numbers,])
}

get_causal_difference <- function(df, a, y) {
  # Gets causal effect difference
  # df - data frame, a,y - names of fields for A and Y
  # Tested on binary variable for now
  strata <- simFrame::stratify(df, c(a))
  positive_a <- get_subset(df, strata, 2)
  negative_a <- get_subset(df, strata, 1)
  count_positive_a <- count(positive_a, vars=c(y))
  pr_1 <- count_positive_a[count_positive_a$y==1,]$freq / nrow(positive_a)
  count_negative_a <- count(negative_a, vars=c(y))
  pr_2 <- count_negative_a[count_negative_a$y==1,]$freq / nrow(negative_a)
  return(pr_1-pr_2)
}

get_bins <- function(float_data) {
  # TODO
}

# Just saved the previous code just in case
if (FALSE) {
  # Table 3.1 with some random other variable l2
  b <- c(1,2,3,4,5,6,7,8,9,9,9,8,7,6,5,4,3,2,1,1.1)
  l <- c(0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1)
  l2<- c(0,0,1,1,0,0,1,1,0,0,1,0,0,0,0,0,1,1,1,1)
  a <- c(0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1)
  y <- c(0,1,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,0,0,0)
  df <- data.frame(b,l,l2,a,y,stringsAsFactors=FALSE)
  
  # Print the data
  df
  simFrame::stratify(df, c("a"))
  # Stratify
  strata <- simFrame::stratify(df, c("l", "l2"))
  check_positivity(strata)
  st1 <- get_subset(df, strata, 1)
  st2 <- get_subset(df, strata, 2)
  st3 <- get_subset(df, strata, 3)
  st4 <- get_subset(df, strata, 4)
  
  strata2 <- simFrame::stratify(df, c("l"))
  check_positivity(strata2)
  st1 <- get_subset(df, strata2, 1)
  st2 <- get_subset(df, strata2, 2)
  get_causal_difference(st1, 'a', 'y')
  get_causal_difference(st2, 'a', 'y')
  get_causal_difference(df, 'a', 'y')
  
  # Bucket code
  cut(das$anim, 3)
}

setwd('/Users/Sergiy/Documents/CWRUgrad/Semester 4/EECS 442 Causal Learning from Data/yelp_dataset_parser')
df <- read.csv("./modified_datasets/all_data.csv")
# Add T_avg
df$TAVG = (df$TMAX + df$TMIN) / 2
# TMAX: {5 83}
# TMIN: {-12 56}
# TAVG: {-3.5 68.0}

# Split T into buckets (TAVG_CAT column)
t_breaks <- c(-999, 25, 55, 75, 999) # split points
#t_labels <- c(1,2,3,4) # group names
df$TAVG_CAT <- cut(df$TAVG, breaks = t_breaks)

# How does T affect total review count?
# For each T get average review count
strata_t <- simFrame::stratify(df, c("TAVG_CAT"))
strata_t
strata_mean_reviews <- sapply(strata_t@nr, function(x) mean(get_subset(df, strata_t, x)$user_review_count))
results_1 <- data.frame(strata_t@legend, strata_t@size, strata_mean_reviews)
colnames(results_1) <- c("t_range","num_days","mean_num_reviews") 