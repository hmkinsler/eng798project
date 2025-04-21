library(tidyverse)
library(lubridate)
library(tidytext)
library(textdata)

# Import with proper handling of dates
letters <- read.csv("transcript_data.csv")

summary(letters)

letters <- letters %>%
  mutate(
    date = mdy(sent_date),  # Using mm/dd/yyyy format
    year = year(date),
    month = month(date),
    month_name = month(date, label = TRUE),
    day = day(date)
  )

str(letters) # This lets you check the data type for letters$date which should have the correct formatting

# Tokenize the transcripts
letter_words <- letters %>%
  unnest_tokens(word, transcript) %>%
  anti_join(stop_words)

# Get word frequencies
word_counts <- letter_words %>%
  count(word, sort = TRUE)

# Calculate TF-IDF
letter_tf_idf <- letter_words %>%
  count(record_unit, word) %>%
  bind_tf_idf(word, record_unit, n) %>%
  arrange(desc(tf_idf))

# Get sentiment lexicons
nrc <- get_sentiments("nrc")
bing <- get_sentiments("bing")
afinn <- get_sentiments("afinn")

# Calculate sentiment scores
letter_sentiment <- letter_words %>%
  inner_join(bing) %>%
  count(record_unit, sentiment) %>%
  spread(sentiment, n, fill = 0) %>%
  mutate(sentiment_score = positive - negative)

# Combine with metadata
sentiment_analysis <- letters %>%
  select(record_unit, date, sender_race, stance, event) %>%
  left_join(letter_sentiment)

# Visualize sentiment by group
sentiment_analysis %>%
  group_by(stance) %>%
  summarize(avg_sentiment = mean(sentiment_score, na.rm = TRUE)) %>%
  ggplot(aes(x = reorder(stance, avg_sentiment), y = avg_sentiment)) +
  geom_col() +
  coord_flip() +
  labs(title = "Average Sentiment by Stance", x = "Stance", y = "Average Sentiment")