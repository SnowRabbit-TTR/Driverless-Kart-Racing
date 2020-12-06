from keras.layers import Activation, Conv2D, Dense, Dropout, Flatten
from keras.layers.convolutional import MaxPooling2D
from keras.models import Sequential


class NNet():

    def __init__(self, input_shape, num_class):
        self.model = Sequential()
        self.model.add(Conv2D(32, (3, 3), padding="same", input_shape=input_shape))
        self.model.add(Activation("relu"))
        self.model.add(Conv2D(32, (3, 3)))
        self.model.add(Activation("relu"))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        self.model.add(Conv2D(64, (3, 3), padding="same"))
        self.model.add(Activation("relu"))
        self.model.add(Conv2D(64, (3, 3)))
        self.model.add(Activation("relu"))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        self.model.add(Flatten())
        self.model.add(Dense(512))
        self.model.add(Activation("relu"))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(num_class))
        self.model.add(Activation("softmax"))
