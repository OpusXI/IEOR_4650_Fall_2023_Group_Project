import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

matchFrame = pd.read_csv("./data/matches/england-premier-league-matches-2017-to-2022-stats.csv")

# add an outcome column - if 