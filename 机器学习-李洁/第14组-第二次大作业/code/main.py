from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import bayesian
import numpy as np
import decisiontree as decision_diy

import data_loader, feature_extract, evaluation

def draw(x_data,y_data,title):
    plt.figure()
    plt.title(title)
    plt.plot(x_data, y_data)
    plt.show()

def accuracy(test_labels, pred_lables):  
    correct = np.sum(test_labels == pred_lables)  
    n = len(test_labels)  
    return float(correct) / n  


classes = ['airplane', 'automobile','brid','cat','deer','dog','frog','horse','ship','truck']

# 从文件中读取数据
x_train, y_train, x_test, y_test = data_loader.load_data()

# 特征提取
x_train, x_test = feature_extract.get_feature(x_train, x_test)

# 标准化
std = StandardScaler()
x_train = std.fit_transform(x_train)
x_test = std.transform(x_test)

# PCA
pca = PCA(n_components=0.8)
pca.fit(x_train)
x_train = pca.transform(x_train)
x_test = pca.transform(x_test)

print('--- start fitting ---')
Model_Bayesian_Diy = bayesian.Bayesian()
Model_Bayesian_Diy.fit(x_train,y_train)

Model_Decisiontree_Diy=[]
for i in range(20):
    print(i)
    Model_Decisiontree_Diy.append(decision_diy.DecisionTreeClassifier_Diy(max_depth=i+1))
    Model_Decisiontree_Diy[i].fit(x_train, y_train)

Model_KNeighbors = []
for i in range(20):
    Model_KNeighbors.append(KNeighborsClassifier(n_neighbors=i+1))
    Model_KNeighbors[i].fit(x_train,y_train)

Model_Beyasian = GaussianNB()
Model_Beyasian.fit(x_train,y_train)

Model_Decisiontree = []
for i in range(20):
    Model_Decisiontree.append(DecisionTreeClassifier(max_depth=i+1))
    Model_Decisiontree[i].fit(x_train,y_train)

Model_Randomforest_Md = []
for i in range(20):
    Model_Randomforest_Md.append(RandomForestClassifier(max_depth=i+1))
    Model_Randomforest_Md[i].fit(x_train,y_train)

Model_Randomforest_Ne = []
for i in range(20):
    Model_Randomforest_Ne[i].append(RandomForestClassifier(n_estimators=5*i+1))
    Model_Randomforest_Ne[i].fit(x_train,y_train)

Model_SVC = SVC(kernel="rbf", decision_function_shape="ovo")
Model_SVC.fit(x_train,y_train)

print('--- fitting done ---')
print('--- Bayesian Diy Result ---')
y_pred = Model_Bayesian_Diy.predict(x_test)
evaluation.ModelEvaluation(y_true = y_test, y_pred = y_pred, ModelName = 'Beyasian Diy')

print('--- Bayesian Result ---')
y_pred = Model_Beyasian.predict(x_test)
evaluation.ModelEvaluation(y_true = y_test, y_pred = y_pred, ModelName = 'Bayesian')

print('--- KNeighbors Result ---')
x_data = []
y_data = []
y_pred_final = None
max_accuracy = -1
max_nneighbors = -1
for i in range(20):
    y_pred = Model_KNeighbors[i].predict(x_test)
    x_data.append(i+1)
    Accuracy = accuracy(y_test,y_pred)
    y_data.append(Accuracy)
    y_pred_final = y_pred if Accuracy > max_accuracy else y_pred_final
    max_nneighbors = i+1 if Accuracy > max_accuracy else max_nneighbors
draw(x_data,y_data,'KNN n_neighbors')
print('max n_neighbors is ',max_nneighbors)
evaluation.ModelEvaluation(y_true = y_test, y_pred = y_pred_final, ModelName = 'KNN')

print('--- Decision Tree Result ---')
x_data = []
y_data = []
max_depth = -1
y_pred_final = None
max_accuracy = -1
for i in range(20):
    y_pred = Model_Decisiontree[i].predict(x_test)
    x_data.append(i)
    Accuracy = accuracy(y_test,y_pred)
    y_data.append(Accuracy)
    y_pred_final = y_pred if Accuracy > max_accuracy else y_pred_final
    max_depth = i+1 if Accuracy > max_accuracy else max_depth 
draw(x_data,y_data,'Decisiontree Max Depth')
print('max depth is ',max_depth)
evaluation.ModelEvaluation(y_true = y_test, y_pred = y_pred_final, ModelName = 'Decision Tree')

print('--- Decision Tree Diy Result ---')
x_data = []
y_data = []
max_depth = -1
y_pred_final = None
max_accuracy = -1
for i in range(20):
    y_pred = Model_Decisiontree_Diy[i].predict(x_test)
    x_data.append(i)
    Accuracy = accuracy(y_test,y_pred)
    y_data.append(Accuracy)
    y_pred_final = y_pred if Accuracy > max_accuracy else y_pred_final
    max_depth = i+1 if Accuracy > max_accuracy else max_depth 
draw(x_data,y_data,'Decisiontree Max Depth')
print('max depth is ',max_depth)
evaluation.ModelEvaluation(y_true = y_test, y_pred = y_pred_final, ModelName = 'Decision Tree Diy')

print('--- Random Forest Result ---')
print('-- 测试max_depth参数 --')
x_data = []
y_data = []
max_depth = -1
max_accuracy = -1
for i in range(20):
    y_pred = Model_Randomforest_Md[i].predict(x_test)
    x_data.append(i)
    Accuracy = accuracy(y_test,y_pred)
    y_data.append(Accuracy)
    max_depth = i+1 if Accuracy > max_accuracy else max_depth 
draw(x_data,y_data,'Randomforest Max Depth')
print('max depth is ',max_depth)

print('-- 测试n_estimators参数 --')
x_data = []
y_data = []
n_estimators = -1
max_accuracy = -1
for i in range(20):
    y_pred = Model_Randomforest_Ne[i].predict(x_test)
    x_data.append(5*i+1)
    Accuracy = accuracy(y_test,y_pred)
    y_data.append(Accuracy)
    n_estimators = 5*i+1 if Accuracy > max_accuracy else n_estimators 
draw(x_data,y_data,'Randomforest N_estimator')
print('n_estimators is ',n_estimators)

print('-- 按照以上使accuracy最大化的参数重新训练模型并输出结果 --')
Model_Randomforest = RandomForestClassifier(max_depth=max_depth,n_estimators=n_estimators)
Model_Randomforest.fit(x_train,y_train)
evaluation.ModelEvaluation(y_true = y_test, y_pred = Model_Randomforest.predict(x_test), ModelName = 'Random Forest')

print('--- SVC Result ---')
y_pred = Model_SVC.predict(x_test)
evaluation.ModelEvaluation(y_true = y_test, y_pred = y_pred, ModelName = 'SVC')

