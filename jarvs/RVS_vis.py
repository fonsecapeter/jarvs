#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib
matplotlib.style.use('ggplot')

# import and massage data
df = pd.read_csv("./RVS_report.csv", header=None, names=["att", "date", "num_rvs", ">6mo old"])
df['<6mo old'] = df['num_rvs'] - df['>6mo old']

cols_to_keep = ['att', '<6mo old', '>6mo old']
df_vis = df[cols_to_keep].tail(12)

# initialize vars for categorical axis
att_call = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
att_labels = df_vis.att

df_vis.plot(kind='bar', stacked=True, color=['#666666', '#C94949'])

# override auto ytick at threshold (found to be when max < 5) to keep ticks at whole numbers 
if max(df['num_rvs'].tail(12)) < 5:
	plt.gca().yaxis.set_major_locator(MultipleLocator(1.0))

plt.xticks(att_call, att_labels, rotation=45)
plt.xlabel("Attending")
plt.ylabel("Count")
plt.title("Outstanding RVSs")

plt.show()