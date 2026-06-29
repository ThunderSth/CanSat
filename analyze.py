import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")

df.plot("time","altitude")

df.plot("time","acc_z_1_1")

df.plot("time","gyro_1_1")

df.plot("time","temperature")


#df.plot.scatter("year","ndvi")

#df["ndvi"].hist(bins=3)

plt.show()