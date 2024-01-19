import matplotlib.pyplot as plt
import numpy as np

csv_path = "./tmp/tmp_data.csv"
print(f"path: {csv_path}")

if csv_path is not None:
    file = np.loadtxt(csv_path, delimiter=",")
else:
    print("None")
    exit(1)

fig = plt.figure()
ax = fig.add_subplot()
ax.plot(file[:, 0], file[:, 1])
plt.show()

csv_path = "./tmp/randn_1D.csv"

file = np.loadtxt(csv_path, delimiter=",")
print(file.shape)
fig = plt.figure()
ax = fig.add_subplot()
ax.hist(file)
plt.show()
