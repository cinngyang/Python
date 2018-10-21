import numpy as np
import pandas as pd
from keras.utils import np_utils
np.random.seed(10)

from keras.datasets import mnist

(x_train_image, y_train_label),(x_test_image, y_test_label) = mnist.load_data()



import matplotlib.pyplot as plt
def plot_image(image):
    fig = plt.gcf() #set pict size
    fig.set_size_inches(2, 2)
    plt.imshow(image, cmap='binary')
    plt.show()

plot_image(x_train_image[0])
y_train_label[0]


import matplotlib.pyplot as plt
def plot_images_labels_prediction(images,labels,
                                  prediction,idx,num=10):
    fig = plt.gcf()
    fig.set_size_inches(12, 14)
    if num>25: num=25
    for i in range(0, num):
        ax=plt.subplot(5,5, 1+i)
        ax.imshow(images[idx], cmap='binary')
        title= "label=" +str(labels[idx])
        if len(prediction)>0:
            title+=",predict="+str(prediction[idx])

        ax.set_title(title,fontsize=10)
        ax.set_xticks([]);ax.set_yticks([])
        idx+=1
    plt.show()

print ('x_train_image:',x_train_image.shape)
print ('y_train_label:',y_train_label.shape)

x_Train =x_train_image.reshape(60000, 784).astype('float32')
x_Test = x_test_image.reshape(10000, 784).astype('float32')
x_train_image[0]
