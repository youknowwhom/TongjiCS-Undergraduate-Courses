import pickle
import numpy as np

# 定义一个函数，用于从文件中加载数据
def unpickle(filename):
    with open(filename, 'rb') as fo:
        data = pickle.load(fo, encoding='latin1')
        return data

# 定义一个函数，用于对文件中的数据进行转换
def file_transform(file):
    data = file['data']
    labels = file['labels']

    # 将数据重新形状，调整通道顺序为BGR
    data = data.reshape(10000, 3, 32, 32)
    data = data.transpose(0, 2, 3, 1)

    labels = np.array(labels)

    return data, labels

# 定义一个函数，用于加载数据并进行转换
def load_file(filename):
    file = unpickle('./data/' + filename)
    return file_transform(file)

# 定义一个函数，用于加载训练集和测试集的数据
def load_data():
    print('--- Start Loading Dataset ---')

    trainingFileName = 'data_batch_'

    # 加载第一个训练批次的数据
    data, labels = load_file(trainingFileName + str(1))
    x_train = data
    y_train = labels
    
    # 循环加载剩余四个训练批次的数据
    for i in range(4):
        data, labels = load_file(trainingFileName + str(i + 2))
        x_train = np.vstack((x_train, data))
        y_train = np.hstack((y_train, labels))

    # 加载测试集的数据
    x_test, y_test = load_file('test_batch')

    print('--- Load Dataset Successfully ---')
    
    return x_train, y_train, x_test, y_test
