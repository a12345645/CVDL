from tensorflow import keras
from tensorflow.keras import layers

from tensorflow.keras.preprocessing.image import ImageDataGenerator

import numpy as np
import random


IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32

class Resnet50(object):
    def __init__(self):
        super(Resnet50, self).__init__()

    def model(self):
        input_shape = IMAGE_SIZE + (3,)
        inputs = keras.Input(shape=input_shape)
        x = layers.ZeroPadding2D(padding=(3, 3), name='conv1_pad')(inputs)
        x = layers.Conv2D(64, (7, 7), strides=(2, 2), padding='valid', kernel_initializer='he_normal', name='conv1')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation("relu")(x)
        x = layers.ZeroPadding2D(padding=(1, 1), name='pool1_pad')(x)
        x = layers.MaxPooling2D((3, 3), strides=(2, 2))(x)

        res_blocks = [3, 4, 6, 3]
        res_filters = [[64, 64, 256], [128, 128, 512], [256, 256, 1024], [512, 512, 2048]]

        first_conv = 1
        for index, block in enumerate(res_blocks):  # 0, 3
            for layer in range(block):  # 3
                input_tensor = x
                for idx, f in enumerate(res_filters[index]):
                    pad = 'valid'
                    ksize = (1, 1)
                    if idx > 0 and idx < 2:
                        ksize = (3, 3)
                        pad = 'same'

                    strides = (1, 1)
                    if first_conv == 1:
                        first_conv = 0

                    elif idx == 0 and layer == 0:
                        strides = (2, 2)

                    x = layers.Conv2D(f, ksize, strides=strides, kernel_initializer='he_normal', padding=pad)(x)
                    x = layers.BatchNormalization()(x)
                    if idx < 2:
                        x = layers.Activation("relu")(x)

                if layer == 0:
                    strides = (2, 2)
                    if index == 0:
                        strides = (1, 1)

                    shortcut = layers.Conv2D(res_filters[index][-1], (1, 1), strides=strides,
                                            kernel_initializer='he_normal')(input_tensor)
                    shortcut = layers.BatchNormalization()(shortcut)
                else:
                    shortcut = input_tensor

                x = layers.add([x, shortcut])
                x = layers.Activation('relu')(x)

        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(1, activation='sigmoid')(x)
        outputs = x
        resnet50 = keras.Model(inputs, outputs)
        return resnet50

def data_generator():
    train_datagen = ImageDataGenerator(rescale=1/255)
    val_datagen = ImageDataGenerator(rescale=1/255)
    test_generator  = val_datagen.flow_from_directory(
        'Dataset/test', 
        class_mode = 'binary', 
        target_size = IMAGE_SIZE, 
        batch_size = 1,
        shuffle = True
    )
    return test_generator

def random_erasing(img, eps, max_h, min_h, max_w, min_w):
    if random.uniform(0, 1) > eps:
        return img

    dim = len(img.shape)

    H = img.shape[0]
    W = img.shape[1]
    h = int(random.uniform(min_h, max_h)*H)
    w = int(random.uniform(min_w, max_w)*W)

    y1 = random.randint(0, img.shape[0] - h)
    x1 = random.randint(0, img.shape[1] - w)

    _img = np.array(img)
    noise_type = random.randint(0, 2)
    if noise_type == 0:
        if dim == 2:
            _img[y1:y1+h, x1:x1+w] = 0
        elif dim == 3:
            _img[y1:y1+h, x1:x1+w, :] = 0
    elif noise_type == 1:
        if dim == 2:
            _img[y1:y1+h, x1:x1+w] = 255
        elif dim == 3:
            _img[y1:y1+h, x1:x1+w, :] = 255
    elif noise_type == 2:
        if dim == 2:
            _img[y1:y1+h, x1:x1+w] = np.uint8(np.random.rand(h, w)*255)
        elif dim == 3:
            _img[y1:y1+h, x1:x1+w,
                 :] = np.uint8(np.random.rand(h, w, _img.shape[2])*255)
    return _img