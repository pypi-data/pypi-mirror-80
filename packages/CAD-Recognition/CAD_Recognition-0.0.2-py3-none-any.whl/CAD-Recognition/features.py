import re
import numpy as np
import pandas as pd
import scipy.io.wavfile as wav
from python_speech_features import *
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.preprocessing import StandardScaler,MinMaxScaler
import pickle

'''待解决的问题
1.测试数据是自己分的，应该使用10折交叉验证
2.直接从训练集里面取了和异常数据相等的数据量
3.验证集也是用StratifiedKFold函数按照原比例抽取的，并未按照患者分层，若按患者分层则无需考虑此内容，
  或者如果取的话，把该患者的所有数据都取出来(而重复患者有多少段数据也不知道，最好后期是弄成患者互斥的)
4.是否需要下采样？这个需要看mfcc的内部写法
5.train_abnormal_124_3.wav只有2s，换成train_abnormal_124_2.wav   train_abnormal_162_6.wav->train_abnormal_162_5.wav
'''


def extract_mfcc(wav_arr, sample_rate):
    mfcc_feat = mfcc(wav_arr, sample_rate)
    energy = np.sqrt(wav_arr)
    mfcc_feat = np.stack(mfcc_feat, energy)
    delta1 = delta(mfcc_feat, 1)
    delta2 = delta(delta1, 1)
    mfcc_feat = np.stack(mfcc_feat, delta1, delta2)
    return mfcc_feat.T

def get_mfcc(data, fs):
    #默认提取的特征维度是13，通常的做法是将该特征进行一阶差分和二阶差分，并将结果进行合并。
    wav_feature =  mfcc(data, fs)
    d_mfcc_feat = delta(wav_feature, 1)
    d_mfcc_feat2 = delta(wav_feature, 2)
    # print("delta1_shape:{:},delta2_shape:{:}".format(d_mfcc_feat.shape, d_mfcc_feat2.shape))
    feature = np.hstack((wav_feature, d_mfcc_feat, d_mfcc_feat2))
    return feature

def dataset_getmfcc(dataset, sample_rate):
    # 计算dataset的mfcc特征
    print("\033[32m正在提取MFCC特征...\033[0m")   #1199-12s的长度  5s是499
    mfcc_set = np.zeros((dataset.shape[1], 499, 39))
    # print(dataset.shape)
    for i in range(dataset.shape[1]):
        mfcc_set[i] = get_mfcc(dataset[:,i], sample_rate)
        # print("sample_rate:{:d},sig_shape:{:},MFCC_shape:{:}".format(sample_rate, signal.shape, mfcc_set[i].shape))
    print("\033[32m特征提取完毕...\033[0m")
    return mfcc_set


if __name__ == "__main__":
    '''path = "E:/Postgraduate work/Literature/PCG/Other's/data/2020.8.16_data/new_wav_8_26/train"  # 需要是远端的数据路径
    for root, dirs, files in os.walk(path):
        #加载label文件
        csv_file = [file for file in files if file.endswith('.csv')]
        csv_data = load_csv(os.path.join(root,csv_file[0]))
        k_nor_train, k_nor_test, k_abnor_train, k_abnor_test = re_distribute_data(10)
        extract_data_by_number(csv_data, k_nor_train[1], "normal")'''
