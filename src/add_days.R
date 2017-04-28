df <- load.csv('outcome_csv/outcome1.csv', header=TRUE)
df$day <- weekdays(as.Date(df$date))
write.csv(df, 'outcome_csv/outcome1.csv)
