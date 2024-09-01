# Install necessary packages if not already installed
# install.packages("tidyverse")
# install.packages("glue")

# Load necessary libraries
library(tidyverse)
library(glue)

# Define constants
p_win <- 0.01
n_events <- 7
n_rounds <- 100

# Calculate expected wins
expected_wins <- n_rounds * n_events * p_win
glue("Expected number of wins in {n_rounds} rounds: {expected_wins}") %>% print()

# Function to calculate probability of winning at least once in a round
prob_win_in_round <- function(n_events, p_win) {
  1 - (1 - p_win)^n_events
}

# Function to calculate probability of no wins in multiple rounds
prob_no_win_in_n_rounds <- function(n_rounds, n_events, p_win) {
  prob_loss_in_round <- (1 - p_win)^n_events
  prob_loss_in_round^n_rounds
}

# Function to calculate probability of exactly k wins in multiple rounds
prob_k_wins_in_n_rounds <- function(k, n_rounds, n_events, p_win) {
  p_win_in_round <- prob_win_in_round(n_events, p_win)
  dbinom(k, n_rounds, p_win_in_round)
}

# Calculations
round_1_win <- prob_win_in_round(n_events, p_win)
round_11_loss <- prob_no_win_in_n_rounds(11, n_events, p_win)
round_11_3wins <- prob_k_wins_in_n_rounds(3, 11, n_events, p_win)

# Print results using glue and tidyverse pipe
glue("Probability of winning in round 1: {round_1_win}") %>% print()
glue("Probability of losing for 11 rounds: {round_11_loss}") %>% print()
glue("Probability of winning exactly 3 times in 11 rounds: {round_11_3wins}") %>% print()

# Plotting probability of exact wins in multiple rounds
df <- expand.grid(Rounds = 1:50, Wins = 0:3) %>%
  mutate(Probability = map2_dbl(Wins, Rounds, ~ prob_k_wins_in_n_rounds(.x, .y, n_events, p_win)))

df %>%
  ggplot(aes(x = Rounds, y = Probability, color = factor(Wins))) +
  geom_line(linewidth = 1.5) +
  labs(title = "Probability of Exact Wins in 50 Rounds",
       x = "Number of Rounds",
       y = "Probability",
       color = "Number of Wins") +
  theme_minimal()

# Simulate and plot the distribution of wins
set.seed(42) # For reproducibility
simulated_wins <- rbinom(10000, n_rounds * n_events, p_win)

tibble(Wins = simulated_wins) %>%
  ggplot(aes(x = Wins)) +
  geom_histogram(binwidth = 1, fill = "blue", color = "black", alpha = 0.7) +
  geom_vline(xintercept = expected_wins, color = "red", linetype = "dashed", linewidth = 1.5) +
  labs(title = "Distribution of Wins in 50 Rounds",
       x = "Number of Wins",
       y = "Frequency") +
  theme_minimal()
