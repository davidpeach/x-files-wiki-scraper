library(tidyverse)
library(forcats)
library(knitr)

data <- read.csv("x-files-episodes.csv")

most_active_directors <- head(
  sort(table(data$director), decreasing = TRUE),
  n = 8L
)

as.data.frame(most_active_directors) %>%
  kable(
    col.names = c("Name of Director", "Number of Episodes directed"),
    format = "html"
  )

directors_wanted <- names(most_active_directors)

data %>%
  select(title, viewers, director) %>%
  filter(director %in% directors_wanted) %>%
  mutate(viewers = as.double(
    str_replace(viewers, "\\[[0-9]+\\]", "")
  )) %>%
  mutate(director = as.factor(director)) %>%
  mutate(g_id = group_indices(., director)) %>%
  ggplot(aes(
    x = fct_reorder(director, viewers, .fun = median),
    y = viewers,
  )) +
  geom_boxplot() +
  coord_flip() +
  theme_minimal() +
  labs(
    title = "Number of viewers that top directors have attracted",
    x = "Director Name",
    y = "Number of viewers (in millions)",
  )
