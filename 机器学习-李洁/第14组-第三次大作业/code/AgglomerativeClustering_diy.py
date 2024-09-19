import numpy as np

# 自定义层次聚类类
class AgglomerativeClustering_diy:
    # 初始化方法，设置簇的数量，默认为2
    def __init__(self, n_clusters=2):
        self.n_clusters = n_clusters
        self.labels_ = None  # 存储每个样本所属的簇
        self.distances = None  # 存储样本间的距离
        self.clusters = None  # 存储最终形成的簇的标识

    # 聚类方法，输入样本矩阵 X
    def fit_predict(self, X):
        n_samples = X.shape[0]

        # 初始时，每个样本为一个簇
        self.labels_ = np.arange(n_samples)

        # 初始化距离矩阵，对角线上的距离设为无穷大
        self.distances = np.zeros((n_samples, n_samples))
        np.fill_diagonal(self.distances, np.inf)

        # 迭代合并簇，直到达到指定的簇数量
        for _ in range(n_samples - self.n_clusters):
            # 找到距离最近的两个簇
            min_distance_idx = np.unravel_index(np.argmin(self.distances), self.distances.shape)
            cluster1, cluster2 = min_distance_idx

            # 合并簇，将属于 cluster2 的样本标记为 cluster1
            self.labels_[self.labels_ == cluster2] = cluster1

            # 更新距离矩阵，将 cluster2 合并到 cluster1
            self.update_distances(cluster1, cluster2)

        # 获取最终形成的簇的标识
        self.clusters = np.unique(self.labels_)

        # 返回样本所属的最终簇的标识
        return self.labels_

    # 更新距离矩阵的方法
    def update_distances(self, cluster1, cluster2):
        # 遍历距离矩阵的行
        for i in range(len(self.distances)):
            # 如果不是 cluster2 所在的行
            if i != cluster2:
                # 更新距离矩阵，将距离更小的值更新到 cluster1 所在的列
                self.distances[i, cluster1] = min(self.distances[i, cluster1], self.distances[i, cluster2])
                self.distances[cluster1, i] = self.distances[i, cluster1]

        # 将 cluster2 所在的行和列的距离置为无穷大
        self.distances[cluster2, :] = np.inf
        self.distances[:, cluster2] = np.inf
