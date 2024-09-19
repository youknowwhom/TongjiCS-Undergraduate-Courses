import numpy as np

class KMeans_diy:
    def __init__(self, n_clusters, max_iters=100, random_state=None):
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.random_state = random_state
        self.cluster_centers_ = None
        self.labels_ = None
        self.inertia_ = None

    def fit(self, X):
        np.random.seed(self.random_state)
        n_samples, n_features = X.shape

        # 初始化簇中心
        random_indices = np.random.choice(n_samples, self.n_clusters, replace=False)
        self.cluster_centers_ = X[random_indices]

        for _ in range(self.max_iters):
            # 分配样本到最近的簇
            distances = np.linalg.norm(X[:, np.newaxis, :] - self.cluster_centers_, axis=2)
            self.labels_ = np.argmin(distances, axis=1)

            # 更新簇中心
            new_centers = np.array([X[self.labels_ == i].mean(axis=0) for i in range(self.n_clusters)])

            # 如果簇中心不再变化，提前结束迭代
            if np.all(self.cluster_centers_ == new_centers):
                break

            self.cluster_centers_ = new_centers

        # 计算 inertia
        self.inertia_ = np.sum((X - self.cluster_centers_[self.labels_]) ** 2)