import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R

# Load data
df = pd.read_csv("41986.csv")
df_2 = pd.read_csv("39277.csv")

df.plot("time","altitude")
df_2.plot("time","altitude")

plt.show()