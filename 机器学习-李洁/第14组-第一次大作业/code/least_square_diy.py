import numpy as np

class LinearRegression(object):
    def __init__(self):
        self.coef_ = None  # 回归系数
        self.intercept_ = None  # 截距

    
    def fit(self, X, y):
        # 在特征矩阵 X 的第一列添加一列全为1的列，以处理截距
        X = np.insert(X, 0, 1, axis=1)

        # 使用最小二乘法求解回归系数
        X_transpose = np.transpose(X)
        self.coef_ = np.linalg.inv(X_transpose.dot(X)).dot(X_transpose).dot(y)

        # 提取截距和系数
        self.intercept_ = self.coef_[0]
        self.coef_ = self.coef_[1:]

    def predict(self, X):
        # 在特征矩阵 X 的第一列添加一列全为1的列，以处理截距
        X = np.insert(X, 0, 1, axis=1)

        # 使用拟合的系数进行预测
        y_pred = X.dot(np.insert(self.coef_, 0, self.intercept_))
        return y_pred
