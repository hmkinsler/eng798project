library(tidyverse)
library(igraph) 
library(ggraph)

setwd("C:/Users/bjpmc/OneDrive/Documents/Digital Humanities/letters/letters_cleaned")

#Loading the Civil Rights Letters edgelist data
letters_edgelist <- read.csv(
  "letters_edgelist.csv")

##Previewing the data
head(letters_edgelist)

#Loading the Civil Rights Letters vertex attribute data 
letters_vertices <- read.csv(
  "letters_vertices.csv")

##Previewing the data
head(letters_vertices)

#Making "stance" and "race" attributes factors for easier graph manipulation 
letters_vertices$stance <- factor(letters_vertices$stance, levels = c("pro", "anti", "na", "polit"))
letters_vertices$race <- factor(letters_vertices$race, levels = c("Black", "White", "Multiracial", "Unknown"))

#Creating an igraph object from the letters_edgelist
letters <- igraph::graph_from_data_frame(d = letters_edgelist, directed = TRUE)

#Manually adding "stance" and "race" the vertex attributes to the igraph object
V(letters)$race <- letters_vertices$race[match(V(letters)$name, letters_vertices$name)]
V(letters)$stance <- letters_vertices$stance[match(V(letters)$name, letters_vertices$name)]

####### VIZ 1. WHOLE NETWORK + STANCE ####### 
ggraph(letters, layout = "kk") +
  geom_edge_link(aes(linetype = factor(weight), color = factor(weight))) +
  scale_edge_linetype_manual(
    name = "Reciprocated Letters", 
    values = c("1" = "dotted", "2" = "solid"),
    labels = c("1" = "Unreciprocated", "2" = "Reciprocated")) + 
  scale_edge_color_manual(
    name = "Reciprocated Letters", 
    values = c("1" = "red", "2" = "black"),
    labels = c("1" = "Unreciprocated", "2" = "Reciprocated")) + 
  geom_node_point(size = 4, aes(color = stance)) + 
  geom_node_label(aes(label = ifelse(stance == "polit", name, NA)), 
                  color = "black", fill = "white", na.rm = TRUE) +
  scale_color_discrete(
    name = "Stance Towards Civil Rights", 
    labels = c(
      "anti" = "Negative", 
      "pro" = "Positive", 
      "na" = "Ambiguous", 
      "polit" = "Political Figure")) +
  theme_void()

####### VIZ 2. WHOLE NETWORK + RACE ####### 
ggraph(letters, layout = "kk") +
  geom_edge_link(aes(linetype = factor(weight), color = factor(weight))) +
  scale_edge_linetype_manual(
    name = "Reciprocated Letters", 
    values = c("1" = "dotted", "2" = "solid"),
    labels = c("1" = "Unreciprocated", "2" = "Reciprocated")) + 
  scale_edge_color_manual(
    name = "Reciprocated Letters", 
    values = c("1" = "red", "2" = "black"),
    labels = c("1" = "Unreciprocated", "2" = "Reciprocated")) + 
  geom_node_point(size = 4, aes(color = race)) + 
  geom_node_label(aes(label = ifelse(stance == "polit", name, NA)), 
                  color = "black", fill = "white", na.rm = TRUE) +
  scale_color_discrete(name = "Ethnicity of Sender",
                       labels = c("White" = "white", 
                       "Black" = "Black", 
                       "Multiracial" = "Multiracial",
                       "NA" = "NA")) +
  theme_void()

############### VIZ 3 EVENT NETWORK: EVENTS + POLITICANS + LETTER WRITERS ############### 
#Loading letters_events.csv
letters_events <- read.csv(
  "letters_events.csv")

#Loading letters_vertices_events.csv
letters_vertices_events <- read.csv(
  "letters_vertices_events.csv")

#Making "stance" and "race" attributes factors for easier graph manipulation 
letters_vertices_events$stance <- factor(letters_vertices_events$stance, levels = c("pro", "anti", "na", "polit", "event"))
letters_vertices_events$race <- factor(letters_vertices_events$race, levels = c("Black", "White", "Multiracial", "Unknown", NA))

#Creating an igraph object for letters_events edgelist
letters_events <- igraph::graph_from_data_frame(d = letters_events, directed = TRUE)

#Manually adding vertex attributes "race" and "stance" to letters_events edgelist
V(letters_events)$race <- letters_vertices_events$race[match(V(letters_events)$name, letters_vertices_events$name)]
V(letters_events)$stance <- letters_vertices_events$stance[match(V(letters_events)$name, letters_vertices_events$name)]

#Adding attribute "shape_label" so that I can more easily apply a shape aes to distinguish event and letter writer nodes
V(letters_events)$shape_label <- ifelse(V(letters_events)$stance == "event", "Event", "Other")
V(letters_events)$shape_label

#Graphing networks with event and letter writing nodes
ggraph(letters_events, layout = "fr") +
  geom_edge_link(alpha = 0.5) +
  geom_node_point(aes(color = stance, shape = shape_label), size = 5) + 
  scale_shape_manual(values = c("Event" = 18, "Other" = 16)) + 
  geom_node_text(aes(label = ifelse(stance == "event", name, NA)), size = 3, color = "black", repel = TRUE) +
  scale_color_discrete(
    name = "Stance Towards Civil Rights", 
    labels = c(
      "anti" = "Negative", 
      "pro" = "Positive", 
      "na" = "Ambiguous", 
      "event" = "Event")) +
  guides(shape = "none") +
  theme_void()

############### VIZ 4. EVENT NETWORK: EVENTS + POLITICIANS ############### 

#Loading letters_combo.csv  
letters_combo <- read.csv(
  "letters_combo.csv")

#Creating an igraph object for letters_combo edgelist
letters_combo <- igraph::graph_from_data_frame(d = letters_combo, directed = TRUE)

#Manually adding vertex attributes of "stance" (I'm not doing race for this visualization)
V(letters_combo)$stance <- letters_vertices_events$stance[match(V(letters_combo)$name, letters_vertices_events$name)]

#Adding attribute "shape_type" so that I can more easily apply a shape aes to distinguish event, politician, and letter writer nodes
V(letters_combo)$shape_type <- case_when(V(letters_combo)$stance == "event" ~ "Event",
  V(letters_combo)$stance == "polit" ~ "Politician",
  TRUE ~ "Other")
  
#Graphing the letters_comnbo network
ggraph(letters_combo, layout = "kk") +
  geom_edge_link(alpha = 0.5) +
  geom_node_point(aes(color = stance, shape = shape_type), size = 3) + 
  scale_shape_manual(values = c("Event" = 15, "Politician" = 17, "Other" = 18)) + 
  geom_node_text(aes(label = name), 
    size = 3, color = "black", repel = TRUE)  + 
  scale_color_discrete(
    name = "Event & Correspondant", 
    labels = c(
      "event" = "Instigating Event",
      "polit" = "Government Official")) +
  guides(shape = "none") +
  theme_void()

