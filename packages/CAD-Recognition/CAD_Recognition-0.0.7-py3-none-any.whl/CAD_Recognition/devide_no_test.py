#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import os
from shutil import *
from collections import Counter

#部分测试集的版本

def rename(file_name, path, people_num, wav_num, mode, devide):
    assert (mode=="abnormal" or mode=="normal")
    # 当操作的文件不在当前目录时必须先进入目录
    os.chdir(path)
    suffix = os.path.splitext(file_name)[1]  # 获取后缀
    new_name = devide + '_' + mode + '_' + str(people_num) + '_' + str(wav_num) + suffix
    os.rename(file_name, new_name)
    return new_name

def copy_wav(raw_wav_path, save_wav_path, raw_data, people_num, mode, devide, same, last_name):
    #从原始数据中导出每个名字,并从原始数据目录下拷贝至新目录并重命名患者did、excel中数据名称、拷贝后的数据名称。
    waves = raw_data[1:-1]
    people_wav = waves.split(',')
    if not os.path.isdir(save_wav_path):
        os.makedirs(save_wav_path)
    #新目录
    new_data_dir = devide
    to_path = save_wav_path + "\\" + new_data_dir
    if not os.path.isdir(to_path):
        os.makedirs(to_path)
    # 不相同则重新计数,相同则取前一次最后的数据的编号
    if same:
        last_num = last_name.split("_") #分割数据名称，取已有数据条数
        wav_num = int(last_num[-1][0:-4])
    else:
        wav_num = 0
    #拷贝数据并改名称
    all_new_name = ''
    for eachfile in people_wav:
        wav_num += 1
        from_path = os.path.join(raw_wav_path, eachfile)  #从原路径下选出数据并拷贝
        copy2(from_path, to_path)
        new_name = rename(eachfile, to_path, people_num, wav_num, mode, devide)
        all_new_name = all_new_name + ',' + new_name
    return all_new_name[1:]

def label_check(data):
    #double check labels, normal is 0 and abnormal is 1
    label = data["total_result"]
    data.loc[data['total_result'] == 1, 'total_result'] = 0
    data.loc[data['total_result'] == 3, 'total_result'] = 1
    data.loc[data['total_result'] == 4, 'total_result'] = 2
    return data

def sort_data(wav_path, save_path, data, mode, devide):
    #对数据排序，拷贝，改名
    data = data[data[:,1].argsort()] #按照第2列姓名进行排序
    people_index = 0
    same_flag = False
    for i in range(data.shape[0]):
        if (i>0) & (data[i, 1]== data[i-1, 1]):  #同名
            same_flag = True
        else:
            people_index += 1
            same_flag = False
        data[i,0] = devide + '_' + mode + '_' + str(people_index)
        data[i, 15] = copy_wav(wav_path, save_path, data[i,15], people_index, mode, devide, same_flag, data[i-1,15])
    return data


def duplicates_count(data):
    #去掉数据中的重复患者，作为训练集的一部分，不允许出现在测试集
    dup_nor_index = 0
    dup_abnor_index = 0
    name = np.array(data["name"])
    count_name = dict(Counter(name))
    dup_name = [key for key, value in count_name.items() if value > 1]  # 只展示重复元素
    for i in range(len(dup_name)):
        dup_nor_index += np.where((data['name']==dup_name[i]) & (data['total_result']==0), 1, 0)
        dup_abnor_index += np.where((data['name']==dup_name[i]) & (data['total_result']==1), 1, 0)
    normal_num_count = {key: value for key, value in dict(Counter(dup_nor_index)).items() if value > 1}
    abnormal_num_count = {key: value for key, value in dict(Counter(dup_abnor_index)).items() if value > 1}
    # print("nor_count:{},abnor_count:{:}".format(normal_num_count, abnormal_num_count))  #统计重复的次数
    return dup_nor_index, dup_abnor_index


def sort_class(wav_path, save_path, data):
    # STEP1:将数据分为正常和异常
    # STEP2:对数据进行分类，排序，相同患者在一起，组成大训练集，进行交叉验证使用

    # STEP1
    data_array = np.array(data)
    # abnormal = data_array[np.where(data_array[:,13] == 1), np.where(data_array[:,13] == 2)]  #标签为1和2的都归为异常
    abnormal = data_array[np.where(data_array[:,13] == 1)]  #标签为1和2的都归为异常
    abnormal = np.append(abnormal, data_array[np.where(data_array[:,13] == 2)], axis=0)
    normal = data_array[np.where(data_array[:,13]== 0)]
    # STEP2
    train_abnormal = sort_data(wav_path, save_path, abnormal, "abnormal", "train")
    train_normal = sort_data(wav_path, save_path, normal, "normal", "train")
    #数据组成
    train_sorted_data = np.vstack((train_abnormal, train_normal))
    return train_sorted_data

def data_transform(csv_path, wav_path, save_path):
    train_out_path = save_path + "/train/_train_label.csv"  # 训练集label文件输出路径
    print("\033[32m正在处理数据...\033[0m")
    with open(csv_path, encoding="utf_8_sig") as files:
        my_usecols = list(range(0, 20))
        data = pd.read_csv(files, usecols=my_usecols, header=0, engine="python")
        c = (data['client_id'] == 10000) | (data['client_id']==10001)  #10000造影数据,10001体检中心数据
        data = data.loc[c , :]
        data = label_check(data)
        train_data = sort_class(wav_path, save_path, data)
        df_train = pd.DataFrame(data=train_data)
        df_train.to_csv(train_out_path, index=False, header=data.columns, encoding='utf_8_sig')
    print("\033[32m数据处理完毕!\033[0m")
    test_path = save_path + "/train"
    return test_path

if __name__ == "__main__":
    # ===>只需改前三个路径到相应位置,需要把原label文件改成utf8的csv格式读取  213,315
    csv_path = "D:/Dataset/PCG_project/My_data/raw_data/8_17/label/label_before_August.csv"  # 原label所在的路径
    wav_path = "D:/Dataset/PCG_project/My_data/raw_data/8_17/raw_wav"  # 原wav所在路径
    save_path = "D:/Dataset/PCG_project/My_data/zaoying/all_zaoying/release_test"  # 想保存到的数据的根路径
    data_transform(csv_path, wav_path, save_path)
