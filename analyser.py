import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from scipy.stats import norm
import warnings

def get_concordant_pairs(df):
  concordant_pairs = 0
  for i in range(0, len(df.index)):
    for j in range(i, len(df.index)):
      if df['h-index-rank'].iloc[j] > df['h-index-rank'].iloc[i]:
        concordant_pairs += 1
  return concordant_pairs    

def get_kendall_tau(df):
  n = len(df.index)
  concordant_pairs = get_concordant_pairs(df)
  discordant_pairs = n * (n - 1) / 2 - concordant_pairs
  kendall_tau = float(concordant_pairs - discordant_pairs) / (concordant_pairs + discordant_pairs)
  z_score = 3 * (concordant_pairs - discordant_pairs) / math.sqrt(n * (n - 1) * (2 * n + 5) / 2)
  return kendall_tau, z_score

def get_line_coefficients(angle):
  return math.tan(math.pi / 4 - angle), math.tan(math.pi / 4 + angle) 

def trim_dataset(df, angle):
  min_a, max_a = get_line_coefficients(angle)
  
  # df1 = df [df ['h-index-rank'] > ((df ['pscore-rank'] + 100) * min_a - 100)]
  # df1 = df1[df1['h-index-rank'] < ((df1['pscore-rank'] + 100) * max_a - 100)]
  df1 = df [df ['h-index-rank'] > ((df ['pscore-rank'] + 100) * min_a - 100)]
  df1 = df1[df1['h-index-rank'] < ((df1['pscore-rank'] + 100) * max_a - 100)]
  return df1

def calculate_kendall_tau(df1, angle):
  fig = plt.figure()
  df1.plot(kind='scatter', x='pscore-rank', y='h-index-rank')
  plt.savefig('figs/' + str(math.degrees(angle)) + '.png')
  plt.close(fig)

  kendall_tau, z_score = get_kendall_tau(df1)
  print ', '.join([str(math.degrees(angle)), str(kendall_tau), str(z_score), str(len(df1.index))])

def calculate_all(df):
  step = math.pi / 180 # 1 degree steps.
  angle = math.pi / 4

  print 'Angle, Kendall-Tau, Z-Score'
  while angle > 0:
    df1 = trim_dataset(df, angle)
    calculate_kendall_tau(df1, angle)
    angle -= step

def calculate_one(df, angle):
  angle = math.radians(angle)
  df1 = trim_dataset(df, angle)
  calculate_kendall_tau(df1, angle)

def list_conferences(df, angle):
  min_a, max_a = get_line_coefficients(math.radians(angle))

  df1 = df[df['h-index-rank'] >= ((df['pscore-rank'] + 100) * max_a - 100)]
  print 'Above:', len(df1.index)
  for i in range(0, len(df1.index)):
    print df1['conference'].iloc[i], '-', df1['name'].iloc[i]

  df1 = df[df['h-index-rank'] <= ((df['pscore-rank'] + 100) * min_a - 100)]
  print 'Below:', len(df1.index)
  for i in range(0, len(df1.index)):
    print df1['conference'].iloc[i], '-', df1['name'].iloc[i]

if __name__ == "__main__":
  warnings.simplefilter(action='ignore', category=FutureWarning)

  df = pd.read_csv("data.csv")
  num_rows = len(df.index)

  # Calculate pscore and h-index ranks.
  rank = np.array(range(1, num_rows + 1))
  df['pscore-rank'] = pd.Series(rank, index=df.index)
  df = df.sort_values(by=['h-index'], ascending=False)
  df['h-index-rank'] = pd.Series(rank, index=df.index)
  df = df.sort_values(by=['pscore-rank'])

  # calculate_one(df, 10)
  # calculate_all(df)
  list_conferences(df, 10.0)
