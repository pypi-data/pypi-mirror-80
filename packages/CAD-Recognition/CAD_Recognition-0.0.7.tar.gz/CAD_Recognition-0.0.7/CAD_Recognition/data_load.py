#!/usr/bin/python
# -*- coding: utf-8 -*-

#颜色 31 红; 32 绿; 33 黄; 34 蓝; 35 洋红; 36 青; 37 白
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
import io
import yaml
# from programs_ECG.ECG_features import *
from kmeans_smote import KMeansSMOTE


import warnings
from scipy import signal

def load_csv(open_path):
    with open(open_path, encoding="utf_8_sig") as files:
        my_usecols = list(range(0, 20))
        data = pd.read_csv(files, usecols=my_usecols, header=0, engine="python")
    return data

def read_wave_data(filename):
    """获取语音文件信息： sample_rate:帧速率  signal:数据的矩阵形式 """
    fs, wavsignal = wav.read(filename)  # 声音文件数据的矩阵形式
    return fs, wavsignal

def data_normalization(scaler, raw_train=None, raw_test=None):
    # 若传入scaler则使用保存的归一化参数来归一化
    '''if scaler==False:
        shape_train, shape_test = raw_train.shape, raw_test.shape
        new_train = raw_train.reshape((shape_train[0],-1), order='C')  #展成大向量进行归一化
        new_test = raw_test.reshape((shape_test[0],-1), order='C')
        scaler = StandardScaler()     #Z-score
        train_data = scaler.fit_transform(new_train)   #拟合train的均值和方差
        test_data = scaler.transform(new_test)
        train_data = train_data.reshape(shape_train, order='C')  #reshape成原来的shape
        test_data = test_data.reshape(shape_test, order='C')
        print("\033[32m归一化完成：train_data shape:{:}\033[0m".format(train_data.shape))
        return train_data, test_data , scaler
    else:
        shape_test = raw_test.shape
        scaler = pickle.load(open('scaler1.pkl', 'rb'))
        x_test = raw_test.reshape((shape_test[0], -1), order='C')
        x_test = scaler.transform(x_test)
        x_test = x_test.reshape(shape_test, order='C')  # reshape成原来的shape
        return x_test, scaler'''

    shape_test = raw_test.shape
    # scaler = pickle.load(open('scaler1.pkl', 'rb'))
    x_test = raw_test.reshape((shape_test[0], -1), order='C')
    x_test = scaler.transform(x_test)
    x_test = x_test.reshape(shape_test, order='C')  # reshape成原来的shape
    return x_test, scaler


def data_normalization_(scaler, raw_train=None, raw_test=None):
    # 若传入scaler则使用保存的归一化参数来归一化
    '''if scaler==False:
        shape_train, shape_test = raw_train.shape, raw_test.shape
        new_train = raw_train.reshape((-1,1), order='C')  #展成大向量进行归一化,保留batch
        new_test = raw_test.reshape((-1,1), order='C')
        scaler = StandardScaler()     #Z-score
        train_data = scaler.fit_transform(new_train)   #拟合train的均值和方差
        test_data = scaler.transform(new_test)
        train_data = train_data.reshape(shape_train, order='C')  #reshape成原来的shape
        test_data = test_data.reshape(shape_test, order='C')
        print("\033[32m归一化完成：train_data shape:{:}\033[0m".format(train_data.shape))
        return train_data, test_data , scaler
    else:
        shape_test = raw_test.shape
        scaler = pickle.load(open('scaler2.pkl', 'rb'))
        x_test = raw_test.reshape((-1, 1), order='C')
        x_test = scaler.transform(x_test)
        x_test = x_test.reshape(shape_test, order='C')  # reshape成原来的shape
        return x_test, scaler'''

    shape_test = raw_test.shape
    # scaler = pickle.load(open('scaler2.pkl', 'rb'))
    x_test = raw_test.reshape((-1, 1), order='C')
    x_test = scaler.transform(x_test)
    x_test = x_test.reshape(shape_test, order='C')  # reshape成原来的shape
    return x_test, scaler

def down_resample(data, sample_rate, seconds, ratio):
    new_sample_rate =  int(sample_rate / ratio)
    index = pd.date_range('1/1/2000', periods=sample_rate*seconds, freq='T')  # 这个起始时间任意指定，freq为其频率
    data1 = pd.DataFrame(data)
    data1.index = index
    data_obj = data1.resample(str(ratio)+'T')  # 第一个为抽样频率，label表示左右开闭区间
    data_new = data_obj.asfreq()[0:]
    return np.array(data_new), new_sample_rate

def load_data(root, x, y, section, aug_repeat=1):
    """
    加载数据使其适合网络输入格式
    """
    gap = 7 / (section-1)
    print("\033[32m正在加载wav数据...\033[0m")
    sample_rate = 4000
    x_data = np.zeros((5 * sample_rate, 1))
    y_data = np.zeros((1))
    for i in range(len(x)):
        # print('i为:{},文件是:{}'.format(i,root + "/" + x[i]))
        (sample_rate, signal_read) = wav.read(root + "/" + x[i])
        #此处应有通道选择,取第三通道数据（最显著的）
        # signal_read, sample_rate = down_resample(signal_read[0: int(12*sample_rate),2], sample_rate, 12, 2)  #下采样
        signal_read = signal_read[0:12*sample_rate,2]
        b, a = signal.butter(5, [0.0125, 0.2], btype='bandpass')  #五阶巴特沃斯带通滤波器（通带：25–400赫兹）
        filtedData = signal.filtfilt(b, a, signal_read)  # data为要过滤的信号
        y_data = np.append(y_data, np.repeat(y[i], section))
        x_temp = []
        for j in range(section):
            x_temp.append([])
        for k in range(section):
            x_temp[k] = signal_read[int((k*gap) * sample_rate): int((k*gap+5) * sample_rate)].reshape((-1, 1))   # no filter
            # x_temp[k] = filtedData[int((k*gap) * sample_rate): int((k*gap+5) * sample_rate)].reshape((-1, 1))  # filter
            x_data = np.hstack((x_data, x_temp[k]))
    x_data = np.delete(x_data, 0, axis=1)  # 删掉0列
    y_data = np.delete(y_data, 0)  # 删掉0
    #data augmentation
    if aug_repeat>1:
        x_data_aug, y_data_aug = x_data, y_data
        for i in range(aug_repeat-1):
            #aug_repeat为重复倍数，减去本身的一次
            x_data = np.hstack((x_data, x_data_aug))
            y_data = np.append(y_data, y_data_aug)
    print("\033[32m数据加载完毕...\033[0m")
    return x_data, y_data, sample_rate

def load_data_(root, x, y, section):
    """
    加载数据使其适合网络输入格式,下采样至363Hz,先用2s的不overlap，取5段，10s
    """
    gap = 2
    print("\033[32m正在加载wav数据...\033[0m")
    sample_rate = 4000
    x_data = np.zeros((gap * 363, 1))
    y_data = np.zeros((1))
    for i in range(len(x)):
        # print('i为:{},文件是:{}'.format(i,root + "/" + x[i]))
        (sample_rate, signal_read) = wav.read(root + "/" + x[i])
        #此处应有通道选择,取第三通道数据（最显著的）
        signal_read, sample_rate = down_resample(signal_read[0: int(12*sample_rate),7], sample_rate, 12, 11)  #下采样
        signal_read = signal_read[0:12*sample_rate,0]
        # b, a = signal.butter(5, [0.0125, 0.2], btype='bandpass')  #五阶巴特沃斯带通滤波器（通带：25–400赫兹）
        # filtedData = signal.filtfilt(b, a, signal_read)  # data为要过滤的信号
        y_data = np.append(y_data, np.repeat(y[i], section))
        x_temp = []
        for j in range(section):
            x_temp.append([])
        for k in range(section):
            # x_temp[k] = signal_read[int((k*gap) * sample_rate): int((k*gap+5) * sample_rate)].reshape((-1, 1))   # no filter
            # x_temp[k] = filtedData[int((k*gap) * sample_rate): int((k*gap+5) * sample_rate)].reshape((-1, 1))  # filter
            x_temp[k] = signal_read[int((k * gap) * sample_rate): int(((k+1) * gap) * sample_rate)].reshape((-1, 1))
            x_data = np.hstack((x_data, x_temp[k]))
    x_data = np.delete(x_data, 0, axis=1)  # 删掉0列
    y_data = np.delete(y_data, 0)  # 删掉0
    print("\033[32m数据加载完毕...\033[0m")
    return x_data, y_data, sample_rate

def _Class_Balance(x, y, kmeans):
    print("\033[32m类别平衡中...\033[0m")
    x_data = x.transpose()

    labels, counts = np.unique(y, return_counts=True)
    irt = round((counts[0]+1)/3*(counts[1]+1), 1)
    '''assert (counts[0] > counts[1])  #检查是否0类多于1类
    print("X_shape:{},y_shape{}".format(x_data.shape, y.shape))
    [print('Class {} has {} instances'.format(label, count))
     for label, count in zip(*np.unique(y, return_counts=True))]'''

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        warnings.filterwarnings('ignore', category=UserWarning)
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        kmeans_smote = KMeansSMOTE(
            kmeans_args = {'n_clusters': kmeans},   #
            smote_args = {'k_neighbors': 5},        #从少类样本中挑选的个数
            random_state = 2,                       #seed
            sampling_strategy = "minority",
            imbalance_ratio_threshold = 0.2
        )         #只对少类样本重采样
        #imbalance_ratio_threshold配置:小于irt的簇入选
        # ir（不平衡比例）越大说明越不平衡，增大irt会放宽标准，允许更不平衡的簇入选；
        # 降低irt就提高标准，少数类别占比越大的簇才能入选。
        X_resampled, y_resampled = kmeans_smote.fit_sample(x_data, y)

    '''print("X_resmapled_shape:{},y_resmapeled_shape:{},".format(X_resampled.shape, y_resampled.shape))
    [print('Class {} has {} instances after oversampling'.format(label, count))
     for label, count in zip(*np.unique(y_resampled, return_counts=True))]'''
    labels, counts = np.unique(y_resampled, return_counts=True)
    try:
        assert (counts[0] == counts[1])  #检查类别是否已经平衡
    except:
        print('\033[31m类别不平衡:\033[0m')
    # assert (counts[0] == counts[1])  # 检查类别是否已经平衡
    X_resampled = X_resampled.transpose()
    return X_resampled, y_resampled

def _extract_data_by_number(df, number, _class, mode, sub):
    #按照选出的患者的编号将所有的患者的数据取出来。
    # assert ((_class== "abnormal") or (_class=="normal"))
    assert ((mode== "train") or (mode=="test"))
    data  = []
    true_label, label = np.zeros(1), np.zeros(1)
    for i in range(number.shape[0]):
        name = mode + "_" + _class + "_" + str(number[i])
        wav_data = df.loc[df["did"]==name, "waves"]
        local = str(wav_data.values)[1:-1]
        local_1 = re.sub('\'', '', local)
        local_1 = re.sub('\n', ',', local_1)
        local_1 = re.sub(' ', '', local_1)
        local_1 = local_1.split(',')
        data.extend(local_1)
        #获得csv中的真实3类标签(0,1,2)
        this_label = np.array(df.loc[df["did"] == name, "total_result"])  #有多少组数据就有多少个标签，保存最原始的标签
        true_label = np.append(true_label, this_label)
        #判断分类器的类型1(1/3,4->[0][1,2])或者2(1,3/4->[0,1][2])
        for i in range(this_label.shape[0]):   #考虑患者重复的情况
            if sub==1:  #轻度归为异常
                if this_label[i] > 0:
                    label = np.append(label, [1,1,1])
                else:
                    label = np.append(label, [0,0,0])
            elif sub==2:  #轻度归为正常
                if this_label[i] > 1:  label = np.append(label, [1,1,1])
                else: label = np.append(label, [0,0,0])
    label = np.delete(label, 0)
    true_label = np.delete(true_label,0)
    '''if _class == "abnormal":
        label = np.ones(len(data)).astype(int)
    else:
        label = np.zeros(len(data)).astype(int)'''
    return data, label, true_label

def re_distribute_data(k_folds, abnor_num, nor_num):
    '''
    重新分配标签
    :param k_folds: 验证折数
    :param abnor_num: all_train中异常个数
    :param nor_num:  all_train中正常个数
    :return:
    '''
    #在训练集中 K_fold 抽出患者编号，正常和异常分别抽10折
    abnormal_index = np.arange(1,abnor_num+1)
    abnormal_label = np.arange(1,abnor_num+1)
    normal_index = np.arange(1,nor_num+1)
    normal_label = np.arange(1,nor_num+1)
    k_nor_train , k_nor_test, k_abnor_train, k_abnor_test = [],[],[],[]
    kfolder = KFold(n_splits=k_folds, shuffle=False, random_state=0)  #random_state：seed
    for train, test in kfolder.split(abnormal_index, abnormal_label):
        k_abnor_train.append(abnormal_index[train])
        k_abnor_test.append(abnormal_index[test])
    for train, test in kfolder.split(normal_index, normal_label):
        k_nor_train.append(normal_index[train])
        k_nor_test.append(normal_index[test])
    return k_abnor_train, k_abnor_test, k_nor_train, k_nor_test

def k_folds_(data_path, folds, sub):
    for root, dirs, files in os.walk(data_path):
        # 加载label文件
        csv_file = [file for file in files if file.endswith('.csv')]
        csv_data = load_csv(os.path.join(root, csv_file[0]))
        k_abnor_train, k_abnor_test, k_nor_train, k_nor_test = re_distribute_data(folds, 10, 10) #152, 323
        x_train, y_train, x_valid, y_valid, y_train_true, y_valid_true = [], [], [], [], [], []
        for i in range(folds):
            x_train_abnormal, y_train_abnormal, y_train_abnormal_true = _extract_data_by_number(csv_data, k_abnor_train[i], "abnormal", 'train', sub)
            x_valid_abnormal, y_valid_abnormal, y_valid_abnormal_true = _extract_data_by_number(csv_data, k_abnor_test[i], "abnormal", 'train', sub)
            x_train_normal, y_train_normal, y_train_normal_true = _extract_data_by_number(csv_data, k_nor_train[i], "normal", 'train', sub)
            x_valid_normal, y_valid_normal, y_valid_normal_true = _extract_data_by_number(csv_data, k_nor_test[i], "normal", 'train', sub)
            # 顺序必须对应(依次是：训练异常x，训练异常y，训练真实y；验证异常x，验证异常y，验证真实y
            x_train_abnormal.extend(x_train_normal)
            y_train_abnormal = np.append(y_train_abnormal, y_train_normal)
            y_train_abnormal_true = np.append(y_train_abnormal_true, y_train_normal_true)
            x_valid_abnormal.extend(x_valid_normal)
            y_valid_abnormal = np.append(y_valid_abnormal, y_valid_normal)
            y_valid_abnormal_true = np.append(y_valid_abnormal_true, y_valid_normal_true)
            x_train.append(x_train_abnormal)
            y_train.append(y_train_abnormal)
            x_valid.append(x_valid_abnormal)
            y_valid.append(y_valid_abnormal)
            y_train_true.append(y_train_abnormal_true)
            y_valid_true.append(y_valid_abnormal_true)
    return root, x_train, y_train, x_valid, y_valid, y_train_true, y_valid_true

def extract_name(data_path, sub, ab_num=213, nor_num=315):
    for root, dirs, files in os.walk(data_path):
        # 加载label文件
        csv_file = [file for file in files if file.endswith('.csv')]
        csv_data = load_csv(os.path.join(root, csv_file[0]))
        # ab_num, nor_num = 213, 315
        k_abnor_train, k_nor_train = np.arange(1,ab_num+1), np.arange(1,nor_num+1)
        x_train, y_train, y_train_true = [], [], []

        x_train_abnormal, y_train_abnormal, y_train_abnormal_true = _extract_data_by_number(csv_data, k_abnor_train, "abnormal", 'train', sub)
        x_train_normal, y_train_normal, y_train_normal_true = _extract_data_by_number(csv_data, k_nor_train, "normal", 'train', sub)
        # 顺序必须对应(依次是：训练异常x，训练异常y，训练真实y；验证异常x，验证异常y，验证真实y
        x_train_abnormal.extend(x_train_normal)
        y_train_abnormal = np.append(y_train_abnormal, y_train_normal)
        y_train_abnormal_true = np.append(y_train_abnormal_true, y_train_normal_true)
        # x_train = x_train_abnormal
        # y_train = y_train_abnormal
        # y_train_true = y_train_abnormal_true
    return root, x_train_abnormal, y_train_abnormal, y_train_abnormal_true

if __name__ == "__main__":
    pass
    # generate_scaler()
    # pickle.dump(2, open('scaler.pkl', 'wb'))
    # train = False
    # if train:
    #     # train
    #     path = 'D:/Dataset/PCG_project/My_data/24+34/train'
    #     to_path = 'D:/Dataset/PCG_project/My_data/24+34/train/_all_train_data.csv'
    #     abnor_num, nor_num = 214, 309
    # else:
    #     # test
    #     path = 'D:/Dataset/PCG_project/My_data/24+34/test'
    #     to_path = 'D:/Dataset/PCG_project/My_data/24+34/test/_all_test_data.csv'
    #     abnor_num, nor_num = 24, 34
    # write_data_to_csv(path, to_path, "test", abnor_num, nor_num)

