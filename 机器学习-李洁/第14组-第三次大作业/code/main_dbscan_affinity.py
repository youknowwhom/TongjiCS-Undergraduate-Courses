import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN, AffinityPropagation
from dbscan_diy import dbscan_diy
import matplotlib.pyplot as plt
from sklearn import metrics
from data import data_loader

train_df = data_loader().data1

model = AffinityPropagation(preference=-2).fit(test.data1)  # -2是三分类，-10是二分类
model = DBSCAN(eps=0.17, min_samples=4).fit(test.data1)

'''
DBSCAN(lib & diy)
'''
for m in range(0, 2):
    SC_score=[]
    CH_score=[]
    DB_score=[]
    n_cluster = []

    irange = np.arange(0.1, 0.2, 0.005)   # min_samples = 4
    # irange = np.arange(0.1, 0.2, 0.008)  # min_samples = 5
    # irange = np.arange(0.14, 0.2, 0.005)
    for i in irange:
        if m == 0:
            model = DBSCAN(eps=i, min_samples=4)
        else:
            model = dbscan_diy(eps=i, min_samples=4)
        model.fit(train_df)
        labels = model.labels_

        # print(i, len(set(labels)) - (1 if -1 in labels else 0))
        # if(len(set(labels)) - (1 if -1 in labels else 0)==1):
        #     continue

        SC_score.append(metrics.silhouette_score(train_df,model.labels_))  
        CH_score.append(metrics.calinski_harabasz_score(train_df,model.labels_))
        DB_score.append(metrics.davies_bouldin_score(train_df,model.labels_))
        n_cluster.append(len(set(labels)) - (1 if -1 in labels else 0))

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 4, 1)
    plt.plot(irange, SC_score, marker='o')
    plt.title('Silhouette Score')

    plt.subplot(1, 4, 2)
    plt.plot(irange, CH_score, marker='o')
    plt.title('Calinski-Harabasz Score')

    plt.subplot(1, 4, 3)
    plt.plot(irange, DB_score, marker='o')
    plt.title('Davies-Bouldin Score')

    plt.subplot(1, 4, 4)
    plt.plot(irange, n_cluster, marker='o')
    plt.title('n-clusters')

    plt.suptitle('DBSCAN')

    plt.tight_layout()
    plt.show()


'''
Affinity lib
'''
SC_score=[]
CH_score=[]
DB_score=[]
n_cluster = []

irange = np.arange(-20, 0, 2)
for i in irange:
    model = AffinityPropagation(preference=i)
    model.fit(train_df)
    labels = model.labels_

    SC_score.append(metrics.silhouette_score(train_df,model.labels_))  
    CH_score.append(metrics.calinski_harabasz_score(train_df,model.labels_))
    DB_score.append(metrics.davies_bouldin_score(train_df,model.labels_))
    n_cluster.append(len(set(labels)))

plt.figure(figsize=(12, 4))

plt.subplot(1, 4, 1)
plt.plot(irange, SC_score, marker='o')
plt.title('Silhouette Score')

plt.subplot(1, 4, 2)
plt.plot(irange, CH_score, marker='o')
plt.title('Calinski-Harabasz Score')

plt.subplot(1, 4, 3)
plt.plot(irange, DB_score, marker='o')
plt.title('Davies-Bouldin Score')

plt.subplot(1, 4, 4)
plt.plot(irange, n_cluster, marker='o')
plt.title('n-clusters')

plt.suptitle('Affinity Propagation')

plt.tight_layout()
plt.show()