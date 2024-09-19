import numpy as np 
import pandas as pd
import math
from sklearn.model_selection import train_test_split

class Bayesian():
    def __init__(self) -> None:
        self.y = None
        self.classes = None
        self.classes_num = None
        self.parameters = []
        
    def fit(self, X, y) -> None:
        self.y = y
        self.classes = np.unique(y)
        self.classes_num = len(self.classes) 
        # 计算每个类中每个特征的均值和方差
        for i, c in enumerate(self.classes):
            # 选择类别为c的所有X
            X_c = X[np.where(self.y == c)]
            self.parameters.append([])
            # 添加均值与方差
            for col in X_c.T:
                parameters = {"mean": col.mean(), "var": col.var()}
                self.parameters[i].append(parameters)
    
    def cal_prior(self, c):
        '''
        先验函数，也就是求先验概率
        利用极大似然估计的结果得到
        '''
        frequency = np.mean(self.y == c)
        return frequency
        
    def cal_likelihood(self, mean, var, X): 
        """
        似然函数
        """
        # 高斯概率
        dx = 1e-4 # 防止除数为0
        coeff = 1.0 / math.sqrt(2.0 * math.pi * var + dx)
        exp = math.exp(-(math.pow(X - mean, 2) / (2 * var + dx)))
        return coeff * exp
    
    
    def cal_probabilities(self, X):
        posteriors = [] # 后验概率
        for i,c in enumerate(self.classes):
            # p(y)
            posterior = self.cal_prior(c)
            # p(x | y)
            for feature, params in zip(X, self.parameters[i]):
                likelihood = self.cal_likelihood(params["mean"], params["var"], feature)
                posterior *= likelihood
            posteriors.append(posterior)
        # 返回具有最大后验概率的类别
        return self.classes[np.argmax(posteriors)]
            
    def predict(self, X):
        y_pred = [self.cal_probabilities(sample) for sample in X]
        return y_pred
    
    def score(self, X, y):
        y_pred = self.predict(X)
        accuracy = np.sum(y == y_pred, axis=0) / len(y)
        return accuracy
