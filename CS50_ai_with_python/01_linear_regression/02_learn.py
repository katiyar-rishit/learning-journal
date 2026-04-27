from sklearn.linear_model import LinearRegression
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pandas as pd
import numpy as np

data = fetch_california_housing()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, predictions))


coefficients = pd.DataFrame(
    {"Feature": data.feature_names, "Coefficients": model.coef_}
).sort_values(by="Coefficients", ascending=False)

print(coefficients)

my_house = [[3.5, 20, 5.0, 1.0, 800, 3.0, 34.05, -118.25]]

predicted_price = model.predict(my_house)
print(f"Estimated price: ${predicted_price[0] * 100000:,.2f}")
