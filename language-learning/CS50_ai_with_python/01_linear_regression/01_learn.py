from sklearn.linear_model import LinearRegression
import numpy as np

X = [[1], [2], [3], [4]]
Y = [2, 4, 6, 8]

model = LinearRegression()
model.fit(X, Y)
print(model.predict([[5], [15]]))
print(model.coef_)
print(model.intercept_)
print(f"Equation: y={model.coef_}x + {model.intercept_}")
