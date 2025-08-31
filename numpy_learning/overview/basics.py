import numpy as np

a = np.array([1, 2, 3])
print(a)

b = np.array([[9.0, 8.0, 7.0], [6.0, 5.0, 4.0]])
print(b)

# get dimension
print(a.ndim)
print(b.ndim)

# get shape
print(a.shape)
print(b.shape)

# get datatype
print(a.dtype)

# specifying datatype
c = np.array([1, 2, 3], dtype="int16")
print(c.dtype)

# get size - in bytes
print(a.itemsize)
print(c.itemsize)

# total number of elements
print(a.size)

# total size
print(a.size * a.itemsize)
# or
print(a.nbytes)
