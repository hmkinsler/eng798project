library(tidyverse)
library(lubridate)

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

# Check the distribution of dates
letters %>%
  count(year) %>%
  arrange(year)

# Amount of letters sent over time
letters %>%
  count(year, month) %>%
  mutate(yearmonth = make_date(year, month, 1)) %>%
  ggplot(aes(x = yearmonth, y = n)) +
  geom_line() +
  geom_point() +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  labs(title = "Letter Sent Per Year", x = "Date", y = "Count")