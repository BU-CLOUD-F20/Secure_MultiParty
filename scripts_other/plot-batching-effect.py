import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import math

def zero_to_nan(values):
    """Replace every 0 with 'nan' and return a copy."""
    return [float('nan') if x==0 else x for x in values]

num_rows = [1000, 10000, 100000, 1000000, 10000000, 100000000]
num_runs_batched = [0, 0, 0, 0, 0, 0]
num_runs_single = [0, 0, 0, 0, 0, 0]

col_batched = [0, 0, 0, 0, 0, 0]
col_single = [0, 0, 0, 0, 0, 0]

try:
    input_file_exchange = sys.argv[1]
    title = sys.argv[2]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <input_file_exchange>")

# load exchange results
with open(input_file_exchange,'r') as csvfile:
    plots = csv.reader(csvfile, delimiter='\t')
    for row in plots:
        if row[0] == 'BATCHED':
            index = int(math.log10(int(row[1])/1000))
            col_batched[index] += float(row[2])
            num_runs_batched[index] +=1
        if row[0] == 'ASYNC':
            index = int(math.log10(int(row[1])/1000))
            col_single[index] += float(row[2])
            num_runs_single[index] +=1


csvfile.close()

# compute average values
for i in range(len(col_batched)):
    col_batched[i] = col_batched[i]/num_runs_batched[i]

for i in range(len(col_single)):
    if num_runs_single[i] > 0:
        col_single[i] = col_single[i]/num_runs_single[i]


# plot
N = len(num_rows)
fig, ax = plt.subplots()
ind = np.arange(N)    # x locations
width = 0.35         # the width of the bars

p1 = ax.plot(num_rows, zero_to_nan(col_batched), color='green', marker='.', linestyle='dashed', linewidth=2, markersize=12)
p2 = ax.plot(num_rows, zero_to_nan(col_single), color='darkred', marker='x', linewidth=2, markersize=12)

ax.set_ylabel('Time (s)', fontsize=20)
ax.set_xlabel('Messages', fontsize=20)
ax.set_yscale('log')
ax.set_xscale('log')
ax.grid(True)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

#ax.set_title(title, fontsize=18)

ax.legend((p1[0], p2[0]), ('Batched', 'Eager'), fontsize=18)


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

#autolabel(p1)

ax.autoscale_view()
fig.tight_layout()
plt.show()