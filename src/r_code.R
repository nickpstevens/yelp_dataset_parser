library(plyr)
library(Hmisc)
library(simFrame)
library(stats)

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

# This code tried to see data for T ranges
if (FALSE) {
  setwd('/Users/Sergiy/Documents/CWRUgrad/Semester 4/EECS 442 Causal Learning from Data/yelp_dataset_parser')
  df <- read.csv("./modified_datasets/testset.csv")
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
  strata_mean_reviews <- sapply(strata_t@nr, function(x) mean(get_subset(df, strata_t, x)$user_review_count))
  results_1 <- data.frame(strata_t@legend, strata_t@size, strata_mean_reviews)
  colnames(results_1) <- c("t_range","num_days","mean_num_reviews") 
  results_1
  
  # How does raw presence of precipitation affect review count?
  df$PRCP_PRESENCE <- df$PRCP>0 | df$SNOW>0
  strata_p_p <- simFrame::stratify(df, c("PRCP_PRESENCE"))
  strata_mean_reviews <- sapply(strata_p_p@nr, function(x) mean(get_subset(df, strata_p_p, x)$user_review_count))
  results_2 <- data.frame(strata_p_p@legend, strata_p_p@size, strata_mean_reviews)
  colnames(results_2) <- c("prcp_presence","num_days","mean_num_reviews") 
  results_2
}

get_results_1_city <- function(df, strata_city, strat_num) {
  city_name <- strata_city@legend[strat_num,1]
  subset_city <- get_subset(df, strata_city, strat_num)
  t_breaks <- c(-999, 35, 55, 75, 999) # split points
  #t_labels <- c(1,2,3,4) # group names
  subset_city$TAVG_CAT <- cut(subset_city$TAVG, breaks = t_breaks)
  strata_t <- simFrame::stratify(subset_city, c("TAVG_CAT"))
  strata_mean_reviews <- sapply(strata_t@nr, function(x) mean(get_subset(subset_city, strata_t, x)$review_count))
  results_city <- data.frame(rep(city_name, length(strata_t@legend)), strata_t@legend, strata_t@size, strata_mean_reviews)
  colnames(results_city) <- c("city", "t_range","num_days","mean_num_reviews") 
  return(results_city)
}

# Get avg number of reviews for T buckets
# May need to rename some columns since the dataset changed
if (FALSE) {
  setwd('/Users/Sergiy/Documents/CWRUgrad/Semester 4/EECS 442 Causal Learning from Data/yelp_dataset_parser')
  df <- read.csv("./outcome_csv/reviews_per_day.csv")
  df$X <- NULL
  weather_df <- read.csv('weather/CurrentDay.csv', header=TRUE)
  df <- merge(x = df, y = weather_df, by = c("date", "city"), all.x = TRUE)
  df$TAVG = (df$TMAX + df$TMIN) / 2
  df$TMAX <- NULL
  df$TMIN <- NULL
  df$PRCP_B <- df$PRCP>0 | df$SNOW>0
  strata_city <- simFrame::stratify(df, c("city"))
  results_1 <- get_results_1_city(df, strata_city, 1)
  for (x in strata_city@nr[2:length(strata_city@nr)]){
    results_1 <- rbind(results_1, get_results_1_city(df, strata_city, x))
  }
  results_1
}

# Gets E[Y^(treatment_vol=treament_value)]
get_causal_prob <- function(df, treatment_col, treatment_value, outcome_col) {
  # Stratify by treatment
  strata_treatment <- simFrame::stratify(df, treatment_col)
  # Get number of subset with treatment = treatment_value
  strata_table <- data.frame(strata_treatment@legend, strata_treatment@nr)
  strata_table <- strata_table[strata_table[,treatment_col]==treatment_value,]
  strata_num <- strata_table[1,2]
  # Get this subset
  subset <- get_subset(df, strata_treatment, strata_num)
  # Return probability of outcome being TRUE
  #return(nrow(subset[subset[,outcome_col]==TRUE,])/nrow(subset))
  return(mean(subset[,outcome_col]))
}

# TEST
if (FALSE) {
  a1 <- 1:10
  a2 <- a1>5
  a3 <- 13:4
  a4 <- a3>5
  df <- data.frame(a1,a2,a3,a4)
  df
  treatment_col <- 'a2'
  treatment_value <- TRUE
  outcome_col <- 'a3'
  strata_treatment <- simFrame::stratify(df, treatment_col)
  strata_table <- data.frame(strata_treatment@legend, strata_treatment@nr)
  strata_table <- strata_table[strata_table[,treatment_col]==treatment_value,]
  strata_num <- strata_table[1,2]
  subset <- get_subset(df, strata_treatment, strata_num)
  nrow(subset[subset[,outcome_col]==TRUE,])/nrow(subset)
  mean(subset[,outcome_col])
}

setwd('/Users/Sergiy/Documents/CWRUgrad/Semester 4/EECS 442 Causal Learning from Data/yelp_dataset_parser')
df <- read.csv("./outcome_csv/reviews_per_day.csv")
df2 <- read.csv("./outcome_csv/outcome1.csv")
df$X <- NULL
weather_df <- read.csv('weather/CurrentDay.csv', header=TRUE)
df <- merge(x = df, y = weather_df, by = c("date", "city"), all.x = TRUE)
df$TAVG = (df$TMAX + df$TMIN) / 2
df$TMAX <- NULL
df$TMIN <- NULL
df$PRCP_B <- df$PRCP>0 | df$SNOW>0
df
confounders <- c("city", "day")
strata_by_conf <- simFrame::stratify(df, confounders)
treatment_col <- 'PRCP_B'
outcome_col <- 'normed_difference'
exp_prcp <- sapply(strata_by_conf@nr, function(x) get_causal_prob(get_subset(df, strata_by_conf, x), treatment_col, TRUE, outcome_col))
exp_no_prcp <- sapply(strata_by_conf@nr, function(x) get_causal_prob(get_subset(df, strata_by_conf, x), treatment_col, FALSE, outcome_col))
strata_info <- data.frame(strata_by_conf@legend, strata_by_conf@size, strata_by_conf@size/sum(strata_by_conf@size), exp_prcp, exp_no_prcp)
colnames(strata_info) <- c("city", "day","num_data","stand_prob","E[Y|PRCP]","E[Y|NO PRCP]") 
weighted.mean(strata_info$`E[Y|PRCP]`, strata_info$stand_prob)
weighted.mean(strata_info$`E[Y|NO PRCP]`, strata_info$stand_prob)