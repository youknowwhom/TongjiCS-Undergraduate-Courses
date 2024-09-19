import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler
from AgglomerativeClustering_diy import AgglomerativeClustering_diy
from data import data_loader
from data import evaluation

train_df = data_loader().data1

'''
    实现了AgglomerativeClustering
'''
# # 读取数据
# data = pd.read_csv('Country-data.csv')
#
# # 提取特征
# features = data.drop('country', axis=1)
#
# # 标准化数据
# scaler = StandardScaler()
# features_scaled = scaler.fit_transform(features)

# 计算评估指标
n_clusters_range = range(2, 10)  # 聚类数量范围

linkage_methods = ['ward', 'complete', 'average']
affinity_methods = ['euclidean', 'manhattan', 'cosine']

for linkage_method in linkage_methods:
    for affinity_method in affinity_methods:
        if linkage_method == 'ward' and affinity_method != 'euclidean':
            # Ward linkage only supports euclidean distance
            continue

        silhouette_scores = []
        calinski_harabasz_scores = []
        davies_bouldin_scores = []

        for n_clusters in n_clusters_range:
            # 使用Agglomerative Clustering
            agg_cluster = AgglomerativeClustering(
                n_clusters=n_clusters, linkage=linkage_method, metric=affinity_method
            )

            clusters = agg_cluster.fit_predict(train_df)

            # 检查聚类的唯一标签数量
            unique_labels = np.unique(clusters)
            if len(unique_labels) < n_clusters:
                # 如果未能形成指定数量的聚类，跳过该参数组合
                continue

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
        plt.plot(list(n_clusters_range)[:len(silhouette_scores)], silhouette_scores, marker='o')
        plt.title(f'Silhouette Score ({linkage_method}, {affinity_method})')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Score')

        # Calinski-Harabasz Score
        plt.subplot(1, 3, 2)
        plt.plot(list(n_clusters_range)[:len(calinski_harabasz_scores)], calinski_harabasz_scores, marker='o')
        plt.title(f'Calinski-Harabasz Score ({linkage_method}, {affinity_method})')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Score')

        # Davies-Bouldin Score
        plt.subplot(1, 3, 3)
        plt.plot(list(n_clusters_range)[:len(davies_bouldin_scores)], davies_bouldin_scores, marker='o')
        plt.title(f'Davies-Bouldin Score ({linkage_method}, {affinity_method})')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Score')

        plt.tight_layout()
        plt.show()

        '''
            结果可视化部分
        '''
        # agg_cluster = AgglomerativeClustering(
        #     n_clusters=3, linkage=linkage_method, metric=affinity_method
        # )
        #
        # clusters = agg_cluster.fit_predict(train_df)
        # evaluation(data_loader().data1, clusters, data_loader().country, agg_cluster)


'''
    实现了手写版AgglomerativeClustering
'''

# # 读取数据
# data = pd.read_csv('Country-data.csv')
#
# # 提取特征
# features = data.drop('country', axis=1)
#
# # 标准化数据
# scaler = StandardScaler()
# features_scaled = scaler.fit_transform(features)
#
# # 计算评估指标
# n_clusters_range = range(2, 10)  # 聚类数量范围
#
# silhouette_scores = []
# calinski_harabasz_scores = []
# davies_bouldin_scores = []
#
# for n_clusters in n_clusters_range:
#     # 使用Agglomerative Clustering
#     agg_cluster = AgglomerativeClustering_diy(n_clusters=n_clusters)
#     clusters = agg_cluster.fit_predict(features_scaled)
#
#     # 计算评估指标
#     silhouette_avg = silhouette_score(features_scaled, clusters)
#     calinski_harabasz_score_val = calinski_harabasz_score(features_scaled, clusters)
#     davies_bouldin_score_val = davies_bouldin_score(features_scaled, clusters)
#
#     silhouette_scores.append(silhouette_avg)
#     calinski_harabasz_scores.append(calinski_harabasz_score_val)
#     davies_bouldin_scores.append(davies_bouldin_score_val)
#
# # 可视化
# plt.figure(figsize=(12, 4))
#
# # Silhouette Score
# plt.subplot(1, 3, 1)
# plt.plot(n_clusters_range, silhouette_scores, marker='o')
# plt.title('Silhouette Score')
# plt.xlabel('Number of Clusters')
# plt.ylabel('Score')
#
# # Calinski-Harabasz Score
# plt.subplot(1, 3, 2)
# plt.plot(n_clusters_range, calinski_harabasz_scores, marker='o')
# plt.title('Calinski-Harabasz Score')
# plt.xlabel('Number of Clusters')
# plt.ylabel('Score')
#
# # Davies-Bouldin Score
# plt.subplot(1, 3, 3)
# plt.plot(n_clusters_range, davies_bouldin_scores, marker='o')
# plt.title('Davies-Bouldin Score')
# plt.xlabel('Number of Clusters')
# plt.ylabel('Score')
#
# plt.tight_layout()
# plt.show()

# agg_cluster = AgglomerativeClustering(
#     n_clusters=3
# )
#
# clusters = agg_cluster.fit_predict(train_df)
# evaluation(data_loader().data1, clusters, data_loader().country, agg_cluster)