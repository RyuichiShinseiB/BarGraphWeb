import numpy as np

x = np.arange(0, 2 * np.pi, 0.01)
y = np.sin(x)
data = np.array([x, y]).T

np.savetxt("tmp_data.csv", data, delimiter=",")
