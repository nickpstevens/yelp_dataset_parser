library('ndjson')

# Import curated data
reviews_df <- stream_in('modified_datasets/american_review.json')
users_df <- stream_in('modified_datasets/american_user.json')
business_df <- stream_in('modified_datasets/american_business.json')
weather_df <- read.csv('weather/CurrentDay.csv', header=TRUE)

# Join Reviews with their business
df <- merge(x = reviews_df, y = business_df, by = "business_id", all.x = TRUE)
colnames(df)[colnames(df)=="stars.x"] <- "stars"
colnames(df)[colnames(df)=="stars.y"] <- "business_stars"

# Join Reviews with reviewers
df <- merge(x = df, y = users_df, by = "user_id", all.x = TRUE)
colnames(df)[colnames(df)=="review_count.x"] <- "business_review_count"
colnames(df)[colnames(df)=="review_count.y"] <- "user_review_count"
colnames(df)[colnames(df)=="avg_stars"] <- "user_avg_stars"

# Finally, merge in the weather
final_df <- merge(x = df, y = weather_df, by = c("date", "city"), all.x = TRUE)

# Remove columns used for joins
final_df$business_id<-NULL
final_df$user_id<-NULL

# Add day of week
final_df$day <- weekdays(as.Date(final_df$date))

# Average Temp
final_df$TAVG = (final_df$TMAX + final_df$TMIN) / 2
df$TMAX <- NULL
df$TMIN <- NULL

# Add Percipitation Boolean
final_df$PRCP_B <- final_df$PRCP>0 | final_df$SNOW>0

# Optionally, write out to csv
write.csv(final_df, "modified_datasets/all_data.csv")
