import numpy as np

class dbscan_diy:
    def __init__(self, eps=0.5, min_samples=5):
        self.eps = eps                      # 邻域半径
        self.min_samples = min_samples      # 最小样本数
        self.labels_ = None                 # 聚类标签
        self.core_sample_indices_ = None    # 核心点下标
        self.visit = set()

    def fit(self, X):
        self.labels_ = np.zeros(X.shape[0]) - 1
        self.core_sample_indices_ = np.empty(0, dtype=int)
        self.visit.clear()
        cluster_label = 0

        for i in range(X.shape[0]):
            if tuple(X[i]) in self.visit:          # 如果已经被访问，则跳过
                continue

            self.visit.add(tuple(X[i]))            # 标记当前结点为访问过的
            
            neighbors = self._find_neighbors(X, i)
            
            if len(neighbors) < self.min_samples:
                self.labels_[i] = -1  # 标记为噪声
            else:
                self._expand_cluster(X, i, neighbors, cluster_label)
                self.core_sample_indices_ = np.append(self.core_sample_indices_, i)
                cluster_label += 1
        
        return self

    def _find_neighbors(self, X, center_idx):
        distances = np.linalg.norm(X - X[center_idx], axis=1)
        return np.where(distances <= self.eps)[0]

    def _expand_cluster(self, X, center_idx, neighbors, cluster_label):
        self.labels_[center_idx] = cluster_label
        
        i = 0
        while i < len(neighbors):
            if tuple(X[neighbors[i]]) not in self.visit:
                current_neighbor = X[neighbors[i]]
                self.visit.add(tuple(current_neighbor))

                new_neighbors = self._find_neighbors(X, neighbors[i])

                if len(new_neighbors) >= self.min_samples:
                    self.core_sample_indices_ = np.append(self.core_sample_indices_, neighbors[i])
                    neighbors = np.concatenate([neighbors, new_neighbors])
                
            if self.labels_[neighbors[i]] == -1:
                self.labels_[neighbors[i]] = cluster_label

            i += 1