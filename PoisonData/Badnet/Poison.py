
import os
import random
import sys

import numpy as np
import torch
from PIL import Image
import utils_backdoor
from injection_utils import *

sys.path.append("../")


DATA_DIR = 'data'  # data folder
DATA_FILE = 'gtsrb_dataset_int.h5'  # dataset file

TARGET_LS = [25]
NUM_LABEL = len(TARGET_LS)

NUM_CLASSES = 43
PER_LABEL_RARIO = 0.1
INJECT_RATIO = (PER_LABEL_RARIO * NUM_LABEL) / (PER_LABEL_RARIO * NUM_LABEL + 1)
IMG_SHAPE = (32, 32, 3)

PATTERN_DICT = construct_mask_box(target_ls=TARGET_LS, image_shape=IMG_SHAPE, pattern_size=4, margin=1)


#需要在對train test data做整理
def load_dataset(data_file=('%s/%s' % (DATA_DIR, DATA_FILE))):
    if not os.path.exists(data_file):
        print(
            "The data file does not exist. Please download the file and put in data/ directory from https://drive.google.com/file/d/1kcveaJC3Ra-XDuaNqHzYeomMvU8d1npj/view?usp=sharing")
        exit(1)

    dataset = utils_backdoor.load_dataset(data_file, keys=['X_test', 'Y_test'])
    
    X_train = np.transpose(np.array(dataset['X_test'], dtype='float32'), (0, 1, 2, 3))

    Y_train = np.array(dataset['Y_test'], dtype='int64')

    Y_train = np.asarray([np.where(r==1)[0][0] for r in Y_train])
    X_test = np.transpose(np.array(dataset['X_test'], dtype='float32'), (0, 1, 2, 3))
    Y_test = np.array(dataset['Y_test'], dtype='int64')
    Y_test = np.asarray([np.where(r==1)[0][0] for r in Y_test])


    return X_train, Y_train, X_test, Y_test

def mask_pattern_func(y_target):
    mask, pattern = random.choice(PATTERN_DICT[y_target])
    mask = np.copy(mask)
    return mask, pattern


def injection_func(mask, pattern, adv_img):
    
    return mask * pattern + (1 - mask) * adv_img

def infect_X(img, tgt, cnt):
    # print("In infect")
    mask, pattern = mask_pattern_func(tgt)
    
    raw_img = np.copy(img)
    adv_img = np.copy(raw_img)

    img =  Image.fromarray(np.uint8(img))
    dir = 'tmp/'+str(cnt)+'ori.png'
    img.save(dir)


    
    adv_img = injection_func(mask, pattern, img)
    # print("adv_img: ")
    # print(type(adv_img), cnt)


    img0 =  Image.fromarray(np.uint8(adv_img))    
    dir0 = 'tmp/'+str(cnt)+'img.png'
    img0.save(dir0)
       
    
    return adv_img, tgt



class DataGenerator(object):
    def __init__(self, target_ls):
        self.target_ls = target_ls

    def generate_data(self, X, Y, inject_ratio):
        p_X, p_Y = [], []
        cnt = 0
        choice = int(Y.shape[0] * inject_ratio + 0.5)
        choice_idx = np.random.choice(Y.shape[0], choice)
        for cur_idx in choice_idx:
            tgt = random.choice(self.target_ls)
            cur_x, cur_y = infect_X(X[cur_idx], tgt, cnt)  # np.copy()
            p_X.append(cur_x)
            p_Y.append(cur_y)
            cnt = cnt+1
        p_X, p_Y = np.asarray(p_X), np.asarray(p_Y)
        print("check X shape: ", X.shape, p_X.shape)
        print("check Y shape: ", Y.shape, p_Y.shape)
        if inject_ratio == 1:
            return p_X, p_Y
        else:
            return np.concatenate((X, p_X), axis=0), np.concatenate((Y, p_Y), axis=0)

def inject_backdoor():
    print('INJECT RATIO: ', INJECT_RATIO)
    train_X, train_Y, test_X, test_Y = load_dataset()  # Load training and testing data

    base_gen = DataGenerator(TARGET_LS)
    p_X_test, p_Y_test = base_gen.generate_data(test_X, test_Y, 1)  # Data generator for backdoor testing
    p_X_train, p_Y_train = base_gen.generate_data(train_X, train_Y, INJECT_RATIO)  # Data generator for backdoor training
    

if __name__ == '__main__':
    inject_backdoor()
