import numpy as np

'''
一元感知器学习code
'''
class perceptron:
    def __init__(self, learing=0.1, range=10):
        self.learning = learing
        self.range = range
        self.error = []
        self.weight = []

    def start(self, X, y):
        self.weight = np.zeros(1 + X.shape[1])
        self.error = []
        for i in range(self.range):
            errors = 0
            for xi, target in zip(X, y):
                update = self.learning * (target - self.predict(xi))
                self.weight[1:] += update * xi
                self.weight[0] += update * 1
                errors += int(update != 0)
                self.error.append(errors)

    def net_input(self, X):
        return np.dot(X, self.weight[1:]) + self.weight[0] * 1

    def predict(self, X):
        return np.where(self.net_input(X) >= 0.0, 1, -1)
