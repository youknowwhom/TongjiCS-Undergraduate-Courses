import numpy as np

def downsample_data(X, y, max_size=5000):
    """
    对数据集进行降采样，使其大小不超过max_size。

    参数:
    X -- 特征数据集
    y -- 标签数据集
    max_size -- 最大样本数 (默认为500)

    返回:
    X_downsampled -- 降采样后的特征数据集
    y_downsampled -- 降采样后的标签数据集
    """

    # 获取数据集大小
    num_samples = X.shape[0]

    # 检查是否需要降采样
    if num_samples <= max_size:
        return X, y

    # 随机选择样本
    indices = np.random.choice(num_samples, size=max_size, replace=False)
    X_downsampled = X[indices]
    y_downsampled = y[indices]

    return X_downsampled, y_downsampled

class DecisionTreeNode:
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, value=None):
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

class DecisionTreeClassifier_Diy:
    def __init__(self, max_depth=2):
        self.root = None
        self.max_depth = max_depth

    def fit(self, X, y):
        X_downsampled, y_downsampled = downsample_data(X, y)
        self.root = self._build_tree(X_downsampled, y_downsampled, 0)

    def _build_tree(self, X, y, depth):
        #print(depth)
        num_samples, num_features = X.shape
        best_split = {'gini': np.inf}
        is_pure = len(set(y)) == 1

        if depth < self.max_depth and not is_pure:
            #print(num_features)
            for feature_index in range(num_features):
                feature_values = np.unique(X[:, feature_index])
                #print(len(feature_values))
                for threshold in feature_values:
                    left, right = self._split(X, y, feature_index, threshold)
                    if len(left) > 0 and len(right) > 0:
                        gini = self._gini_index(y, left, right)
                        if gini < best_split['gini']:
                            best_split = {'feature_index': feature_index, 'threshold': threshold, 
                                          'left': left, 'right': right, 'gini': gini}

        if best_split['gini'] == np.inf:
            return DecisionTreeNode(value=self._most_common_label(y))
        #print('666')
        left_tree = self._build_tree(X[best_split['left']], y[best_split['left']], depth + 1)
        right_tree = self._build_tree(X[best_split['right']], y[best_split['right']], depth + 1)
        return DecisionTreeNode(feature_index=best_split['feature_index'], threshold=best_split['threshold'], 
                                left=left_tree, right=right_tree)

    def _split(self, X, y, feature_index, threshold):
        left_indices = np.argwhere(X[:, feature_index] <= threshold).flatten()
        right_indices = np.argwhere(X[:, feature_index] > threshold).flatten()
        return left_indices, right_indices

    def _gini_index(self, y, left, right):
        left_gini = self._gini(y[left])
        right_gini = self._gini(y[right])
        total_gini = (len(left) / len(y)) * left_gini + (len(right) / len(y)) * right_gini
        return total_gini

    def _gini(self, y):
        classes = np.unique(y)
        gini = 1
        for cls in classes:
            p_cls = len(y[y == cls]) / len(y)
            gini -= p_cls ** 2
        return gini

    def _most_common_label(self, y):
        return np.bincount(y).argmax()

    def predict(self, X):
        return [self._predict(x, self.root) for x in X]

    def _predict(self, x, tree):
        if tree.value is not None:
            return tree.value
        feature_val = x[tree.feature_index]
        if feature_val <= tree.threshold:
            return self._predict(x, tree.left)
        else:
            return self._predict(x, tree.right)