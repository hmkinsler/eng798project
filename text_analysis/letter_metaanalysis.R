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

# Yearly totals for high-level pattern
letters %>%
  count(year) %>%
  ggplot(aes(x = year, y = n)) +
  geom_col(fill = "steelblue") +
  labs(title = "Letters by Year", x = "Year", y = "Count") +
  theme_minimal()

# LETTERS PER YEAR
letters %>%
  mutate(yearmonth = make_date(year, month, 1)) %>%
  count(yearmonth) %>%
  ggplot(aes(x = yearmonth, y = n)) +
  geom_point(size = 3, color = "steelblue") +
  geom_area(alpha = 0.3, fill = "steelblue") +
  scale_y_log10() +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  labs(title = "Letters Over Time (Log Scale)", x = "Date", y = "Count (log)") +
  theme_minimal()

# FOCUS ON LETTERS SENT IN 1968
letters_1968 <- letters %>%
  filter(year == 1968)

letters_1968 %>%
  mutate(day_of_month = day(date),
         month_name = month(date, label = TRUE)) %>%
  count(month_name, day_of_month) %>%  # Count letters by month and day
  ggplot(aes(x = day_of_month, y = n)) +
  geom_point(size = 3, color = "steelblue") +
  facet_wrap(~month_name) +
  labs(title = "Distribution of Letters Within Each Month of 1968", 
       x = "Day of Month", y = "Number of Letters") +
  theme_minimal()
