import numpy as np
import cvxopt
import math

"""
Support Vector Machine for classification 
"""

class SupportVectorMachine(object):
    
    def __init__(self, kernel = 'linear', power = 2, gamma = 0.1, coef = 0):
        """
        Attributes:
            learned (bool): Keeps track of if perceptron has been fit
            weights (np.ndarray): vector of weights for linear separation
            intercept (float): intercept of learned SVM
            kernel: {'linear', 'polynomial', 'rbf', 'tanh'}
        """
        self.learned = False
        self.weights = np.NaN
        self.intecept = np.NaN
        self.kernel = kernel
        self.power = power
        self.gamma = gamma
        self.coef = coef
        
    def fit(self, X, y):
        """
        Args:
            X (np.ndarray): Training data of shape[n_samples, n_features]
            y (np.ndarray): Target values of shape[n_samples, 1]
            reg_parameter (float): float to determine strength of regulatrization  penalty
                if 0, then no linear regression without regularization is performed

        Returns:
            self: Returns an instance of self

        Raises:
            ValueError if y contains values other than 0 and 1
        """
        n_samples, n_features = np.shape(X)
        
        if self.kernel == 'linear':
            kernel_value = self.linear_kernel(X)
        
        # Use cvxopt to solve SVM optimization problem
        P = cvxopt.matrix(np.outer(y, y) * kernel_value, tc='d')
        q = cvxopt.matrix(np.ones(n_samples) * -1)
        G = cvxopt.matrix(np.diag(np.ones(n_samples)) * -1)
        # There is something fishy here.  Should h equal negative 1?  Should b = negative 1?
        h = cvxopt.matrix(np.zeros(n_samples))
        A = cvxopt.matrix(y, (1,n_samples),  tc='d')
        b = cvxopt.matrix(0,  tc='d')
        
        minimization = cvxopt.solvers.qp(P, q, G, h, A, b)
        alpha = np.ravel(minimization['x'])
        self.weights = np.sum((X.T * (alpha * y)).T, axis=0)
        self.intercept = 0
        for index in alpha:
            if index > 10**-4:
                self.intercept = (1 - y[index] * np.dot(X[index], self.weights)) / y[index]
                break
        self.learned = True
        return self
        
    def predict(self, X):
        """
        Args:
            X (np.ndarray): Training data of shape[n_samples, n_features]

        Returns:
            prediction (np.ndarray): shape[n_samples, 1]
                Returns predicted values

        Raises:
            ValueError if model has not been fit
        """
        if not self.learned:
            raise NameError('Fit model first')
        X = np.asarray(X)
        prediction = np.dot(X, self.weights) + self.intercept
        return np.sign(prediction)
        

    def linear_kernel(self, X):
        return np.dot(X, X.T)

    def polynomial_kernel(self, x1, x2, c, power):
        return (np.dot(x1, x2) + c)**power

    def rbf_kernel(self, x1, x2, gamma):
        difference = x1 - x2
        return np.exp(-gamma * (np.dot(difference, difference.T)**2))

    def tanh_kernel(self, x1, x2, k, c):
        return math.tanh(k * np.dot(x1, x2) + c)

