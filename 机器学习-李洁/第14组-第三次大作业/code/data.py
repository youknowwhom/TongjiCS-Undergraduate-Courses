import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA, IncrementalPCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.cluster import KMeans, DBSCAN, AffinityPropagation
import plotly.express as px

class data_loader():
    def __init__(self) -> None:
        self.df_1 = None
        self.df_2 = None
        self.data1 = pd.read_csv('data/Country-data.csv')
        self.data2 = pd.read_csv('data/Country-data.csv')
        self.country = self.data1.country
        self.analysis()
        # self.draw_pic()
        self.normalization()
        self.myPCA()        
    
    def analysis(self):
        print('data meanings:')
        print('-----------------------------')
        print('data info:')
        print(self.data1.info())
        print('-----------------------------')
        print('data describe:')
        print(self.data1.describe().T)
        print('-----------------------------')

    def draw_pic(self):
        self.data1.hist(bins=30,figsize=(10,10))
        for i in range(1, 10) :
            fig, ax = plt.subplots(1, 2, figsize=(15, 2))
            plt.suptitle(self.data1.columns[i], fontsize=20, fontweight='bold', color='navy')
            # Left Plot
            sns.boxplot(x=self.data1.columns[i], data=self.data1, ax=ax[0])
            # Right Plot
            sns.distplot(self.data1[self.data1.columns[i]], ax=ax[1])
        plt.show()
        sns.heatmap(data=self.data1.iloc[:, 1:].corr(), annot=True, fmt=".2f", linewidth=0.75, cmap="Blues")
        plt.show()
    
    def normalization(self):
        self.data1.drop(columns='country', inplace=True)
        self.data2.drop(columns='country', inplace=True)
        self.data2.drop(columns='gdpp', inplace=True)
        scaler_1 = MinMaxScaler().fit_transform(self.data1)
        scaler_2 = MinMaxScaler().fit_transform(self.data2)
        self.df_1 = pd.DataFrame(scaler_1, columns=self.data1.columns)
        self.df_2 = pd.DataFrame(scaler_2, columns=self.data2.columns)
    
    def myPCA(self):
        # 针对只drop了country的data1
        pca = PCA(n_components=9).fit(self.df_1)
        exp = pca.explained_variance_ratio_
        # plt.plot(np.cumsum(exp), linewidth=2, marker = 'o', linestyle = '--')
        # plt.title("PCA", fontsize=20)
        # plt.xlabel('n_component')
        # plt.ylabel('Cumulative explained Variance Ratio')
        # plt.yticks(np.arange(0.55, 1.05, 0.05))
        # plt.show()     
        final_pca = IncrementalPCA(n_components=5).fit_transform(self.df_1)
        pc = np.transpose(final_pca)
        corrmat = np.corrcoef(pc)
        # sns.heatmap(data=corrmat, annot=True, fmt=".2f", linewidth=0.75, cmap="Blues")
        # plt.show()
        self.data1 = pd.DataFrame({
            'PC1':pc[0],
            'PC2':pc[1],
            'PC3':pc[2],
            'PC4':pc[3],
            'PC5':pc[4],
        })
        # plt.subplots(figsize=(15,6))
        # sns.boxplot(data=self.data1)
        # plt.show()

        # 针对drop了country和gdpp的data2
        pca = PCA(n_components=8).fit(self.df_2)
        exp = pca.explained_variance_ratio_
        # plt.plot(np.cumsum(exp), linewidth=2, marker = 'o', linestyle = '--')
        # plt.title("PCA", fontsize=20)
        # plt.xlabel('n_component')
        # plt.ylabel('Cumulative explained Variance Ratio')
        # plt.yticks(np.arange(0.55, 1.05, 0.05))
        # plt.show()      
        final_pca = IncrementalPCA(n_components=3).fit_transform(self.df_2)
        pc = np.transpose(final_pca)
        corrmat = np.corrcoef(pc)
        # sns.heatmap(data=corrmat, annot=True, fmt=".2f", linewidth=0.75, cmap="Blues")
        # plt.show()
        self.data2 = pd.DataFrame({
            'PC1':pc[0],
            'PC2':pc[1],
            'PC3':pc[2],
        })
        # plt.subplots(figsize=(15,6))
        # sns.boxplot(data=self.data1)
        # plt.show()



class evaluation():
    def __init__(self,X,labels,country,kmeans) -> None:
        self.X = X
        self.labels = labels
        self.cal()
        self.cluster(X,country,kmeans)
        self.draw_res(X)

    def cal(self):
        # 计算轮廓系数
        silhouette_avg = silhouette_score(self.X, self.labels)
        print(f"Silhouette Coefficient: {silhouette_avg}")

        # 计算Calinski-Harabasz指数
        calinski_harabasz_score_val = calinski_harabasz_score(self.X, self.labels)
        print(f"Calinski-Harabasz Index: {calinski_harabasz_score_val}")

        # 计算Davies-Bouldin指数
        davies_bouldin_score_val = davies_bouldin_score(self.X, self.labels)
        print(f"Davies-Bouldin Index: {davies_bouldin_score_val}")
    
    def cluster(self,df,country,kmeans):
        df.insert(0, 'Country', country)
        df['class'] = kmeans.labels_
        df['Need'] = df['class']
        poor = int(df[df.Country=='Afghanistan']['class'].iloc[0])
        middle = int(df[df.Country=='Iran']['class'].iloc[0])
        rich = int(df[df.Country=='Canada']['class'].iloc[0])
        poor_label = 'Poor countries'
        middle_label = 'Middle countries'
        rich_label = 'Rich countries'
        df.replace({'Need':{poor:poor_label, middle:middle_label, rich:rich_label}},inplace=True)

    def draw_res(self,df):        
        fig = px.choropleth(df[['Country','class']],
                    locationmode = 'country names',
                    locations = 'Country',
                    color = df['Need'],  
                    color_discrete_map = {'Rich countries': 'Green',
                                          'Midle countries':'LightBlue',
                                          'Poor countries':'Red'}
                   )

        fig.update_layout(
                margin = dict(
                        l=0,
                        r=0,
                        b=0,
                        t=0,
                        pad=2,
                    ),
            )
        fig.show()


if __name__ == '__main__':
    # 使用说明，按如下方式可以加载data1，同样可将data1替换为data2
    test = data_loader()  # 加载数据，这里我把分析输出的图都注释了，到时候写报告的适合我来跑，只做了归一化和PCA降维
    country = test.country
    # kmeans = KMeans(n_clusters=3).fit(test.data1)
    model = AffinityPropagation(preference=-3).fit(test.data1)  # -2是三分类，-10是二分类
    # model = DBSCAN(eps=0.17, min_samples=4).fit(test.data1)
    evaluation(test.data1, model.labels_,country, model)  # 输出三个结果和地图的过程，不用可以注释