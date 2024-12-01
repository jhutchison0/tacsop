# Install necessary packages if not already installed
# install.packages("tidyverse")
# install.packages("glue")

# Load necessary libraries
library(tidyverse)
library(glue)
library(Rmpfr)
x <- mpfr(15, precBits= 1024)

print(glue("100 should be {749/1.2}"))


# Enigma Settings
# 5 gears, in 3 positions, or permutations
n_gear <- 5 * 4 * 3

# 26 start pos, per gear, or comb
n_start <- 26 * 26 * 26

# Pairs of connected letters
# plan, create all combinations of 26 letters
# 26 letters
n_num <- factorial(26)
# Remove exceptions
# 2 per pair, 6 letters remain
# 10 pairs, don't care about order
# 2 letters in pair, a->e = e->a
n_den <- factorial(6) * factorial(10) * 2**10
n_plug <- n_num / n_den

# Total settings
n_settings <- n_gear * n_start * n_plug
print(n_settings, digits=21)
print(mpfr(n_settings, precBits= 1024))
