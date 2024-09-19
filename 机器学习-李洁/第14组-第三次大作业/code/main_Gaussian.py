import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler
from data import data_loader
from data import evaluation

import os

# joblib 在获取物理核心数量时可能会遇到问题
os.environ['LOKY_MAX_CPU_COUNT'] = '4'  # 使用的核心数量

train_df = data_loader().data1

# # 读取数据
# data = pd.read_csv('Country-data.csv')
#
# # 提取特征
# features = data.drop('country', axis=1)
#
# # 标准化数据
# scaler = StandardScaler()
# features_scaled = scaler.fit_transform(features)

# 测试不同参数的效果
n_components_range = range(2, 10)  # 聚类数量范围
covariance_types = ['full', 'tied', 'diag', 'spherical']  # 协方差类型

for covariance_type in covariance_types:
    silhouette_scores = []
    calinski_harabasz_scores = []
    davies_bouldin_scores = []

    for n_components in n_components_range:
        # 使用Gaussian Mixture
        gmm = GaussianMixture(n_components=n_components, covariance_type=covariance_type, random_state=42)
        clusters = gmm.fit_predict(train_df)

        # 计算评估指标
        silhouette_avg = silhouette_score(train_df, clusters)
        calinski_harabasz_score_val = calinski_harabasz_score(train_df, clusters)
        davies_bouldin_score_val = davies_bouldin_score(train_df, clusters)

        silhouette_scores.append(silhouette_avg)
        calinski_harabasz_scores.append(calinski_harabasz_score_val)
        davies_bouldin_scores.append(davies_bouldin_score_val)

    # 可视化
    plt.figure(figsize=(12, 4))

    # Silhouette Score
    plt.subplot(1, 3, 1)
    plt.plot(n_components_range, silhouette_scores, marker='o')
    plt.title(f'Silhouette Score ({covariance_type} Covariance)')
    plt.xlabel('Number of Components')
    plt.ylabel('Score')

    # Calinski-Harabasz Score
    plt.subplot(1, 3, 2)
    plt.plot(n_components_range, calinski_harabasz_scores, marker='o')
    plt.title(f'Calinski-Harabasz Score ({covariance_type} Covariance)')
    plt.xlabel('Number of Components')
    plt.ylabel('Score')

    # Davies-Bouldin Score
    plt.subplot(1, 3, 3)
    plt.plot(n_components_range, davies_bouldin_scores, marker='o')
    plt.title(f'Davies-Bouldin Score ({covariance_type} Covariance)')
    plt.xlabel('Number of Components')
    plt.ylabel('Score')

    plt.tight_layout()
    plt.show()

