import numpy as np

# All 0s matrix
a = np.zeros(5)
print(a)

# All 1s matrix
b = np.ones((2, 2))
print(b)

# Any number matrix
c = np.full((2, 2, 2), 99, dtype="int32")
print(c)

# any other number (full_like)
d = np.full_like(b.shape, 4)  # matrix with size of a
print(d)
# or
e = np.full_like(a, 4)
print(e)
