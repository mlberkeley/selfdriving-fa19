import matplotlib.pyplot as plt
plt.ion()
import numpy as np
from sklearn.linear_model import LinearRegression

NUM_HOUSES = 500

np.random.seed(774)


lots = 6000 + 1500 * np.random.normal(size = [NUM_HOUSES])
prices = 300 * lots + 2e5 * np.random.normal(size = [NUM_HOUSES]) + 3e5

lr = LinearRegression()
lr_lots = np.reshape(lots, [-1, 1])
lr.fit(lr_lots, prices)
preds = lr.predict(lr_lots)
#print(lr.coef_, lr.intercept_)

plt.xlabel("Lot Size (sqft)")
plt.ylabel("House Prices ($)")

plt.scatter(lots, prices)
#plt.plot(lots, preds, color = 'r', lw = 2.0)

c_1 = 150
c_2 = 5e5

def eval_preds():
	return c_1 * lots + c_2

preds = eval_preds()

def d_preds_c1():
	return lots

def d_preds_c2():
	return np.ones([NUM_HOUSES])

def eval_MSE():
	return np.mean((preds - prices) ** 2)

def d_MSE_c1():
	return np.mean(-2 * prices * d_preds_c1() + 2 * preds * d_preds_c1())

def d_MSE_c2():
	return np.mean(-2 * prices * d_preds_c2() + 2 * preds * d_preds_c2())

LR_c1 = 7e-9
LR_c2 = 0.7

for i in range(400):
	print(f"ITER {i + 1} MSE: {eval_MSE():.0f} c1: {c_1:.1f} c2: {c_2:.0f}")

	c_1 -= LR_c1 * d_MSE_c1()
	c_2 -= LR_c2 * d_MSE_c2()

	preds = eval_preds()

	a, = plt.gca().plot(lots, preds, color = 'r', lw = 2.0)

	plt.gcf().subplots_adjust(left=0.2)

	plt.show()
	plt.pause(0.01)

	a.remove()
