#For this script, I just followed step by step from: https://stevemcd1.github.io/tutorials/comparing_docs.html

#Install & load necessary packages
library(tidyverse)
library(tidytext)
library(readtext)
library(widyr)
library(tm)

#Set working directory
setwd("C:/Users/bjpmc/OneDrive/Documents/Digital Humanities/letters/letters_cleaned/letters")

######### LOADING DATA ######### 

#Set the file path
file_paths <- list.files("C:/Users/bjpmc/OneDrive/Documents/Digital Humanities/letters/letters_cleaned/letters",
                         pattern = "\\.txt$", full.names = TRUE)

# Read in the text files
letter_texts <- readtext(file_paths)

# Read and arrange your metadata (already includes the date in YYYY-MM-DD format)
letter_meta <- read.csv("letters_metadata.csv", stringsAsFactors = FALSE)
letter_meta$date <- as.Date(letter_meta$date)

# Join metadata to the texts
letters_whole <- letter_meta %>%
  arrange(author) |>  # Or arrange(date) if you prefer
  bind_cols(letter_texts)

#View structure
glimpse(letter_whole)

######### TOKENIZE ######### 

#Clean (lowercase, removing punctuation, numbers, stop words)
letters_clean <- letters_whole |> 
  mutate(
    text = str_to_lower(text),
    text = str_remove_all(text, "[:punct:]"),
    text = str_remove_all(text, "[:digit:]"),
    text = str_replace_all(text, "\\n", " "))

#Tokenizing the data
tidy_letters <- letters_clean |> 
  unnest_tokens(word, text) |> 
  anti_join(stop_words)

head(tidy_letters)

######### CREATING A DOCUMENT TERM MATRIX ######### 

#Transforming the tokenized data into a document term matrix
letters_dtm <- tidy_letters |> 
  count(author, word)  |>  
  cast_dtm(author, word, n) 

#Extracting the matrix from the document term object
letters_mat <- as.matrix(letters_dtm)
letters_mat[1:5,1:5]

######### TERM FREQUENCES & ASOCIATIONS ######### 

#
findFreqTerms(letters_dtm, lowfreq = 30)
findAssocs(letters_dtm, "negro", corlimit = 0.50)

######### VIZ 5. MULTIDIMENSIONAL SCALING #########

d <- dist(letters_mat)
fit <- cmdscale(d,eig=TRUE, k=2) 
glimpse(fit) 


x <- fit$points[,1]
y <- fit$points[,2]
plot(x, y, xlab="Coordinate 1", ylab="Coordinate 2",
     main="Metric MDS", type="n")
text(x, y, labels = row.names(letters_mat), cex=.7)

######### COSINE SIMILARITY ######### 

letters_words <- letters_whole |> 
  unnest_tokens(word, text) |> 
  anti_join(stop_words, by = "word") |> 
  count(author, word) |> 
  ungroup()

closest <- letters_words |> 
  pairwise_similarity(author, word, n) |> 
  arrange(desc(similarity))

head(closest)

closest |> 
  filter(item1 == "Rev. Corpening")

######### FROM SIMILARITY TO DISTANCES ######### 

closest <- as.data.frame(closest)
closest_mat <- as.dist(xtabs(closest[, 3] ~ closest[, 2] + closest[, 1]))
cdist <- as.dist(1 - closest_mat)

######### VIZ 6. CLUSTER ANALYSIS ######### 

hc <- hclust(cdist, "ward.D")

par(mar = c(0, 0, 2, 0))
plot(hc, main = "Hierarchical clustering of Civil Rights Letters",
     ylab = "", xlab = "", yaxt = "n")

clustering <- cutree(hc, 10)
table(clustering)

par(mar = c(0, 0, 2, 0))
plot(hc, main = "Hierarchical clustering of Civil Rights Letters",
     ylab = "", xlab = "", yaxt = "n")
rect.hclust(hc, 10, border = "red")

######### MERGE CLUSTER CATEGORIES WITH ORIGINAL DATA ######### 

cluster <- as.numeric(clustering)
author <- rownames(as.data.frame(clustering))

clust_df <- as.data.frame(cbind(author,cluster))

letters_clean <- letters_clean |>  
  left_join(clust_df, by = "author")  |> 
  arrange(cluster)

glimpse(letters_clean)

######### VIZ 7. WORDS THAT DEFINE CLUSTERS ######### 

#Tokenizing the data by clusters
clust_words <- letters_clean |> 
  unnest_tokens(word, text) |> 
  count(cluster, word, sort = TRUE)

#Add tf-idf
clust_words <- clust_words %>%
  bind_tf_idf(word, cluster, n)

#Visualize high tf-idf words
clust_words |> 
  arrange(desc(tf_idf)) |> 
  mutate(word = factor(word, levels = rev(unique(word)))) %>% 
  group_by(cluster) |>  
  top_n(15) |>  
  ungroup() |> 
  ggplot(aes(word, tf_idf, fill = cluster)) +
  geom_col(show.legend = FALSE) +
  labs(x = NULL, y = "tf-idf") +
  facet_wrap(~cluster, ncol = 2, scales = "free") +
  coord_flip()
