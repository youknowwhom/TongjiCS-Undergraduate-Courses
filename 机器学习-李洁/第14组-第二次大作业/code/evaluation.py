from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import classification_report,cohen_kappa_score
import matplotlib.pyplot as plt

def ModelEvaluation(y_true, y_pred, ModelName = ''):
    print(ModelName + ' Evaluation :')
    # 求准确率
    acc = accuracy_score(y_pred = y_pred, y_true = y_true)
    print('accuracy score: ' + str(acc))
    # 求Keppa
    Keppa = cohen_kappa_score(y_true, y_pred)
    print('keppa score: ' + str(Keppa))
    # 分类报告
    print(classification_report(y_true = y_true, y_pred = y_pred))
    # 混淆矩阵
    res = ConfusionMatrixDisplay(confusion_matrix = confusion_matrix(y_true = y_true, y_pred = y_pred))
    res.plot()
    plt.title(ModelName)
    # 将混淆矩阵图保存为图像，在 'output' 目录下以指定的 `模型名称`（加上 '_confusion_matrix.png'）保存
    plt.savefig('output/' + ModelName)
    # 如果希望以交互方式显示混淆矩阵图，请取消下面一行的注释
    # plt.show()


