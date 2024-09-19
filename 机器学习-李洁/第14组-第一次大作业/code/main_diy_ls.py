"""
本文件应用手写的最小二乘法实现线性回归
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PowerTransformer, FunctionTransformer
from sklearn.metrics import r2_score, mean_absolute_percentage_error, mean_squared_error
from least_square_diy import LinearRegression 
from sklearn.compose import ColumnTransformer

# 定义一个函数来训练和评估回归模型
def train_and_evaluate_model(model):
    model.fit(final_train, y_train)  # 用训练数据拟合模型
    y_pred = model.predict(final_test)  # 使用测试数据进行预测
    r2 = r2_score(y_test, y_pred)  # 计算R2分数，用于评估模型拟合度
    rmse = mean_squared_error(y_test, y_pred, squared=False)  # 计算均方根误差（RMSE）
    mape = mean_absolute_percentage_error(y_test, y_pred)  # 计算平均绝对百分比误差（MAPE）
    print("R2 Score:",r2)
    print("RMSE:",rmse)
    print("MAPE:",mape)

# 从CSV文件中读取数据
df = pd.read_csv('concrete_data.csv')
df = df.drop_duplicates()  # 去除重复的数据行

# 分割数据为特征 (X) 和目标变量 (y)
X = df.drop('Strength', axis=1)
y = df['Strength']

# 将数据分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=True, random_state=101)

# 选择最终要使用的特征列（此处全选）
final_selected_features = ['Cement', 'Blast Furnace Slag', 'Water', 'Superplasticizer', 'Fine Aggregate', 'Age', 'Fly Ash', 'Coarse Aggregate']
final_X_train = X_train[final_selected_features]
final_X_test = X_test[final_selected_features]

# 使用ColumnTransformer进行特征转换
transformer = ColumnTransformer(transformers=[
    ('power_transformer', PowerTransformer(), ['Cement', 'Superplasticizer', 'Water', 'Coarse Aggregate']),
    ('log_transformer', FunctionTransformer(func=np.log1p, inverse_func=np.expm1), ['Age']),
    ('sqrt_tansformer', FunctionTransformer(func=np.sqrt), ['Blast Furnace Slag', 'Fly Ash'])
], remainder='passthrough')

final_X_train_tf = transformer.fit_transform(final_X_train)
final_X_train_tf = pd.DataFrame(final_X_train_tf, columns=final_X_train.columns)
final_X_test_tf = transformer.transform(final_X_test)
final_X_test_tf = pd.DataFrame(final_X_test_tf, columns=final_X_test.columns)

# 使用StandardScaler对特征进行标准化
scaler = StandardScaler()
features = final_X_train_tf.columns
final_X_train_tf = scaler.fit_transform(final_X_train_tf)
final_X_train_tf = pd.DataFrame(final_X_train_tf, columns=features)
final_X_test_tf = scaler.transform(final_X_test_tf)
final_X_test_tf = pd.DataFrame(final_X_test_tf, columns=features)

# 准备最终的训练和测试数据
final_train = final_X_train_tf
final_test = final_X_test_tf

# 调用train_and_evaluate_model函数，训练并评估自定义LinearRegression模型
train_and_evaluate_model(LinearRegression())

