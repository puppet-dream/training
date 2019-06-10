from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,ZeroPadding2D,Dropout
from keras.layers import Flatten,Dense
import os
import random
from PIL import Image
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(10)
import read_images_labels as read
# 忽略硬件加速的警告信息
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# 参数设置
LABEL_FILE = '../labels.txt'
IMAGE_SIZE = 32  # 图片默认大小
num_classes = 10  # 图片种类数
labels_dict = {0: '三色堇', 1: '八仙花', 2: '彼岸花', 3: '梨花', 4: '牵牛花', 5: '蔷薇', 6: '薰衣草', 7: '蝴蝶兰', 8: '鸡蛋花', 9: '鸢尾'}


x_train, y_train = read.read_images_labels(data_dir='../train_images/', batch_size=10000)
x_test, y_test = read.read_images_labels(data_dir='../test_images/', batch_size=1000)
x_train_one = x_train * (1. / 255) - 0.5
x_test_one = x_test * (1. / 255) - 0.5
print(type(x_train))


model = Sequential()
model.add(Conv2D(filters=48, kernel_size=(3, 3), input_shape=(32, 32, 3), activation='relu', padding='same'))
model.add(Dropout(0.20))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(Dropout(0.20))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(filters=82, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(Dropout(0.20))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(Dropout(0.20))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(filters=48, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(Dropout(0.20))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dropout(0.25))
model.add(Dense(1000, activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(10, activation='softmax'))
print(model.summary())

try:
    model.load_weights("../flower10model1.h5")
    print("成功加载已有模型，继续训练该模型")
except:
    print("没有模型加载，开始训练新模型")

model.compile(loss='binary_crossentropy', optimizer='adamax', metrics=['accuracy'])
train_history = model.fit(x=x_train_one, y=y_train, validation_split=0.2, epochs=40, batch_size=128, verbose=2)

model.save_weights("../flower10model1.h5")
print("保存刚训练的模型")

result = model.evaluate(x_test_one, y_test, verbose=1)
print('acc:', result[1])

x_ver_img = x_test[0:10]
x_ver = x_test_one[0:10]
y_ver = y_test[0:10]


def read_labels(y_ver):
    labels = []
    for i in range(len(y_ver)):
        label = y_ver[i]
        for j in range(10):
            if label[j] == 1:
                labels.append(j)
    return labels


def get_probability(labels, prediction_labels):
    err = 0
    for j in range(len(labels)):
        if prediction_labels[j] != labels[j]:
            err += 1
    probability = 1 - err / len(labels)
    return probability


prediction_labels = model.predict_classes(x_test_one)
y_test = read_labels(y_test)
probability = get_probability(y_test, prediction_labels)
print("probability:", probability)

labels = read_labels(y_ver)
print("labels:", labels)

prediction = model.predict_classes(x_ver)
print("prediction:", prediction)

type = []
for label in labels:
    type.append(labels_dict[label])
print("种类", type)


def plot_images_labels(images, labels):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    num = len(images)
    fig = plt.gcf()
    fig.set_size_inches(12, 14)
    if num % 5 == 0:
        row = num // 5
    else:
        row = num // 5 + 1
    for i in range(num):
        ax = plt.subplot(row, 5, 1+i)
        ax.imshow(images[i], cmap='binary')
        title = 'label' + str(labels[i])
        ax.set_title(title, fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    plt.show()

# plot_images_labels(x_ver_img, type)