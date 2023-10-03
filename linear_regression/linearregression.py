import pandas as pd
import seaborn as sb
import sklearn
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt
df = pd.read_csv("car_dekho.csv")
# print(df)
# single linear regression(selling price vs transmission)
y = df[['Selling_Price']]
x = df[['Transmission']].replace({"Manual": 1, "Automatic": 0})
plt.scatter(x, y)

lr = LinearRegression()
lr.fit(x, y)
y_line = lr.predict(x)
plt.plot(x, y_line, color='g')
print("Selling Price vs Transmission r value:", lr.score(x, y))
plt.show()
# multiple regression
x = df[['Age', 'Kms_Driven']]
multiple = LinearRegression(fit_intercept=True)
multiple.fit(x, y)
print("Selling Price vs Age and Kms Driven r value:", multiple.score(x, y))
