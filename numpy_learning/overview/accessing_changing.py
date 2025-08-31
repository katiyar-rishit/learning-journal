import numpy as np

a = np.array([[1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14]])
print(a)

# get a specific element
print(a[0, 5])

# get a specific row
print(a[0, :])

# get a specific column
print(a[:, 3])

# getting a little fancy [startindex:endindex:stepsize]
print(a[0, 1:6:2])

print(a)
a[0, 2] = 20
print(a)

a[0, :] = 56
print(a)

a[:, 3] = 5, 6
print(a)

# 3-d example
b = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print(b)

# get specific element (work outside in)
print(b[0, 1, 0])

# replace
b[:, 1, :] = [[9, 9], [8, 8]]
print(b)
