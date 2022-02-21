import random
import numpy as np
import matplotlib.pyplot as plt

x = np.random.exponential(10)

plt.hist(x,density=True, alpha=0.75)
plt.plot(np.exp(-np.arange(0,6,0.1)))
plt.show()

np.random.gamma((10/1)**2, 1**2/10)
