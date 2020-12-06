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


def train(train_config):
    config = configparser.ConfigParser()
    config.read(train_config, encoding="utf-8")
    image_dir = config["DATA"]["image_dir"]
    class_max_num = int(config["DATA"]["maxnum_per_class"])
    dense_size = int(config["MODEL"]["num_class"])
    optimizer = config["MODEL"]["optimizer"]
    epochs = int(config["MODEL"]["epochs"])
    batch_size = int(config["MODEL"]["batch_size"])
    model_name = config["MODEL"]["model_name"]
    exp_dir = config["MODEL"]["exp_dir"]

    X = []
    Y = []

    print("Opening image directory...")
    train_dir = os.path.join(image_dir, "train")
    image_list = [f for f in os.listdir(train_dir) if not f.startswith('.')]
    print("Done.")
    image_num = len(image_list)

    print("Data preprocessing...")
    l_count = r_count = u_count = 0
    for i in tqdm(range(image_num)):
        file_name = image_list[i]
        file_path = os.path.join(train_dir, file_name)
        image = Image.open(file_path)
        image = image.convert("RGB")
        data = np.asarray(image)
        categoty = file_name.split("_")[2]
        if categoty[2] == "1":  # left
            index = 1
            l_count += 1
            is_append = True if l_count < class_max_num else False
        elif categoty[3] == "1":  # right
            index = 2
            r_count += 1
            is_append = True if r_count < class_max_num else False
        else:  # straight
            index = 0
            u_count += 1
            is_append = True if u_count < class_max_num else False
        if is_append == True:
            X.append(data)
            Y.append(index)

    X = np.array(X)
    X = X.astype("float32")
    X = X / 255.0
    Y = np.array(Y)
    Y = np_utils.to_categorical(Y, dense_size)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.05)
    print('Done.')

    nnet = NNet(input_shape=X.shape[1:], num_class=dense_size)
    nnet.model.summary()

    results = {}
    print("Start train model.")
    nnet.model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])
    results[0]= nnet.model.fit(X_train, y_train, validation_split=0.05, epochs=epochs, batch_size=8)

    model_json_str = nnet.model.to_json()
    model_json_path = os.path.join(exp_dir, "model", model_name + ".json")
    model_weight_path = os.path.join(exp_dir, "model", model_name + ".h5")
    open(model_json_path, "w").write(model_json_str)
    nnet.model.save_weights(model_weight_path)
    
    x = range(epochs)
    for k, result in results.items():
        plt.plot(x, result.history["accuracy"], label=k)
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), borderaxespad=0, ncol=2)

    plt.savefig(os.path.join(exp_dir, "acc.jpg"), bbox_inches="tight")
    plt.close()

    for k, result in results.items():
        plt.plot(x, result.history['val_accuracy'], label=k)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=0, ncol=2)

    plt.savefig(os.path.join(exp_dir, "val.jpg"), bbox_inches="tight")
    print("Done.")
    
    print("Evaluation")
    correct_count = 0
    count = 0
    for X, y in zip(X_test, y_test):
        count += 1
        x = X[None, ...]
        pred = nnet.model.predict(x, batch_size=1)
        score = np.max(pred)
        pred_label = np.argmax(pred)
        if np.argmax(y) == pred_label:
            correct_count += 1
        print("pred_label: {0} / groundtruth: {1}".format(pred_label, np.argmax(y)))
    print("accuracy: {:.3f} %".format(correct_count * 100 / count))


if __name__ == "__main__":
    train_config = "config/train_config.ini"
    train(train_config=train_config)
