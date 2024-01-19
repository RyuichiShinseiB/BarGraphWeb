import numpy as np

x = np.arange(0, 2 * np.pi, 0.01)
y = np.sin(x)
data = np.array([x, y]).T

np.savetxt("tmp_data.csv", data, delimiter=",")

rng = np.random.default_rng(42)
randn = rng.standard_normal(100)

np.savetxt("randn_1D.csv", randn, delimiter=",")
