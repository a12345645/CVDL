from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras import regularizers
from tensorflow.keras.optimizers import SGD
import matplotlib.pyplot as plt

class VGG16():
    def __init__(self) -> None:
        weight_decay = 0.0005
        #layer1 32*32*3
        model = Sequential()
        model.add(Conv2D(64, (3, 3), padding='same',
        input_shape=(32,32,3),kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.3))
        #layer2 32*32*64
        model.add(Conv2D(64, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        #layer3 16*16*64
        model.add(Conv2D(128, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        #layer4 16*16*128
        model.add(Conv2D(128, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        #layer5 8*8*128
        model.add(Conv2D(256, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        #layer6 8*8*256
        model.add(Conv2D(256, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        #layer7 8*8*256
        model.add(Conv2D(256, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        #layer8 4*4*256
        model.add(Conv2D(512, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        #layer9 4*4*512
        model.add(Conv2D(512, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        #layer10 4*4*512
        model.add(Conv2D(512, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        #layer11 2*2*512
        model.add(Conv2D(512, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        #layer12 2*2*512
        model.add(Conv2D(512, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        #layer13 2*2*512
        model.add(Conv2D(512, (3, 3), padding='same',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.5))
        #layer14 1*1*512
        model.add(Flatten())
        model.add(Dense(512,kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        #layer15 512
        model.add(Dense(512,kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        #layer16 512
        model.add(Dropout(0.5))
        model.add(Dense(10))
        model.add(Activation('softmax'))

        self.model = model
    batch_size = 32 
    lr=0.01
    momentum=0.9
    nesterov=True
    def printOptimizer(self):
        print('hyperparameters: \nBatch size %d, \nlearning rate: %f \nOptimizer: SGD'%(self.batch_size, self.lr))

    def train(self, x_train, y_train, nb_epoch = 10, batch_size = batch_size):
        sgd = SGD(learning_rate=self.lr, decay=1e-6, momentum=self.momentum, nesterov=self.nesterov)
        self.model.compile(loss='categorical_crossentropy', optimizer=sgd,metrics=['accuracy'])

        history = self.model.fit(x_train,y_train,epochs=nb_epoch, batch_size=batch_size,
                    validation_split=0.1, verbose=1)
        self.model.save('model.h5')

        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left') 
        plt.show()
        plt.savefig('accuracy.png')
        
        plt.plot(history.history['loss']) 
        plt.plot(history.history['val_loss']) 
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left') 
        plt.show()
        plt.savefig('loss.png')