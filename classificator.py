import configparser
import os
import time

import matplotlib.pyplot as plt
import numpy as np
from keras.layers import Activation, Conv2D, Dense, Dropout, Flatten
from keras.layers.convolutional import MaxPooling2D
from keras.models import Sequential
from keras.optimizers import (SGD, Adadelta, Adagrad, Adam, Adamax, Nadam,
                              RMSprop)
from keras.utils import np_utils
from PIL import Image
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from nnet import NNet


class Classificator():

    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file, encoding="utf-8")
        height = int(config["DATA"]["height"])
        width = int(config["DATA"]["width"])
        channel = int(config["DATA"]["channel"])
        input_shape = (height, width, channel)
        dense_size = int(config["MODEL"]["num_class"])
        model_name = config["MODEL"]["model_name"]
        exp_dir = config["MODEL"]["exp_dir"]
        model_weight_path = os.path.join(exp_dir, "model", model_name + ".h5")

        self.nnet = NNet(input_shape=input_shape, num_class=dense_size)
        self.nnet.model.load_weights(model_weight_path)
    
    
    def recognize(self, image):
        image = image.convert("RGB")
        X = np.asarray(image)
        X = X.astype("float32")
        X = X / 255.0
        X = X[None, ...]
        pred = self.nnet.model.predict(X, batch_size=1)
        pred_label = np.argmax(pred)
        return pred, pred_label
