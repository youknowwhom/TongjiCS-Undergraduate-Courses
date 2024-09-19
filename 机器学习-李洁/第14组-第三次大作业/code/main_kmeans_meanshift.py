import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples
import matplotlib.pyplot as plt
from sklearn import metrics
from knn_diy import KMeans_diy

df = pd.read_csv('data/Country-data.csv')
train_df = df.drop(columns='country')
scaler_df = StandardScaler().fit_transform(train_df)


'''
K-means-lib
'''
inertia_list=[]
SC_score=[]
CH_score=[]
DB_score=[]

for i in range(2, 15):
    # build model with KMeans Algorthim
    model = KMeans(n_clusters=i, random_state=1, n_init='auto')
    model.fit_transform(scaler_df)
    inertia = model.inertia_
    inertia_list.append(inertia)
    SC_score.append(silhouette_score(scaler_df,model.labels_))  
    CH_score.append(metrics.calinski_harabasz_score(scaler_df,model.labels_))
    DB_score.append(metrics.davies_bouldin_score(scaler_df,model.labels_))

plt.figure(figsize=(12, 4))

plt.subplot(1, 4, 1)
plt.plot(range(2, 15), SC_score, marker='o')
plt.title('Silhouette Score')

plt.subplot(1, 4, 2)
plt.plot(range(2, 15), CH_score, marker='o')
plt.title('Calinski-Harabasz Score')

plt.subplot(1, 4, 3)
plt.plot(range(2, 15), DB_score, marker='o')
plt.title('Davies-Bouldin Score')

plt.subplot(1, 4, 4)
plt.plot(range(2,15),inertia_list, marker='o')
plt.title('inertia')
plt.suptitle('KMeans')

plt.tight_layout()
plt.show()
'''
plt.plot(range(2,15),SC_score)
plt.axvline(pd.DataFrame(SC_score).idxmax()[0]+2,ls=':')
plt.title('silhouette_score')
plt.show()


plt.plot(range(2,15),CH_score)
plt.title('calinski_harabasz_score')
plt.show()

plt.plot(range(2,15),DB_score)
plt.title('davies_bouldin_score')
plt.show()

plt.plot(range(2,15),inertia_list)
plt.title('inertia')
plt.show()
'''

'''
K-means-diy
'''

inertia_list=[]
SC_score=[]
CH_score=[]
DB_score=[]

for i in range(2, 15):
    # build model with KMeans Algorthim
    model = KMeans_diy(n_clusters=i, random_state=1)
    model.fit(scaler_df)
    inertia = model.inertia_
    inertia_list.append(inertia)
    SC_score.append(silhouette_score(scaler_df,model.labels_))  
    CH_score.append(metrics.calinski_harabasz_score(scaler_df,model.labels_))
    DB_score.append(metrics.davies_bouldin_score(scaler_df,model.labels_))
              
plt.figure(figsize=(12, 4))

plt.subplot(1, 4, 1)
plt.plot(range(2, 15), SC_score, marker='o')
plt.title('Silhouette Score')

plt.subplot(1, 4, 2)
plt.plot(range(2, 15), CH_score, marker='o')
plt.title('Calinski-Harabasz Score')

plt.subplot(1, 4, 3)
plt.plot(range(2, 15), DB_score, marker='o')
plt.title('Davies-Bouldin Score')

plt.subplot(1, 4, 4)
plt.plot(range(2,15),inertia_list, marker='o')
plt.title('inertia')
plt.suptitle('KMeans-diy')

plt.tight_layout()
plt.show()


'''
Meanshift
'''
inertia_list=[]
SC_score=[]
CH_score=[]
DB_score=[]
count = 0
for bd in np.arange(0.5, 5, 0.1):
    count+=1
    model = MeanShift(bandwidth=bd)
    model.fit(scaler_df)
    #print(scaler_df.shape)
    SC_score.append(silhouette_score(scaler_df,model.labels_))  
    CH_score.append(metrics.calinski_harabasz_score(scaler_df,model.labels_))
    DB_score.append(metrics.davies_bouldin_score(scaler_df,model.labels_))


plt.figure(figsize=(12, 3))

plt.subplot(1, 3, 1)
plt.plot(np.arange(0.5,5, 0.1),SC_score)
plt.title('Silhouette Score')

plt.subplot(1, 3, 2)
plt.plot(np.arange(0.5, 5, 0.1),CH_score)
plt.title('Calinski-Harabasz Score')

plt.subplot(1, 3, 3)
plt.plot(np.arange(0.5,5, 0.1),DB_score)
plt.title('Davies-Bouldin Score')

plt.tight_layout()
plt.show()
