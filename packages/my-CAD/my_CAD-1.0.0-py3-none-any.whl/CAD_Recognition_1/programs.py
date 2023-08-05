#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
# import codecs
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())  # 这一句让中文能够写到txt文件中
import yaml
import io
import numpy as np
from release_test.CAD_Recognition.data_load import  load_data, _load_data, _data_normalization, data_normalization, _k_folds
from release_test.CAD_Recognition.features import dataset_getmfcc
import os
import tensorflow as tf
from keras import backend as KTF
# import keras.backend.tensorflow_backend as KTF
import keras
from keras import regularizers, initializers
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D, \
    BatchNormalization, LSTM, Reshape, Conv1D, AveragePooling1D, pooling
from keras.layers.pooling import GlobalAveragePooling1D
from keras.optimizers import RMSprop, Adam
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint
from keras.utils import multi_gpu_model
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import time
import math
from tensorflow.contrib.opt import AdamWOptimizer
import warnings
import pickle

def prob_cal(prediction, class_, index, ratio):
    # 取正常对应的输出段的输出概率，然后求均值。
    class_ = 0 if class_ == 0 else 1
    prob_scope = prediction[index * ratio: (index + 1) * ratio]
    # pred_scope = pred[i * ratio: (i + 1) * ratio]  #保留按照索引取正常或者异常的片段的概率
    # prob_index = np.where(pred_scope == 0)
    prob = np.mean(prob_scope[:, class_]) * 100
    prob = 99.99 if prob == 100 else prob
    return prob

def computing_resource(_config):
    """
    计算资源分配
    :param _config: yaml配置文件
    """
    # export CUDA_VISIBLE_DEVICES = n
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=_config["gpu_fraction"])
    config = tf.ConfigProto(intra_op_parallelism_threads=_config["threads_num"],
                            device_count={'CPU': _config["CPU_num"], 'GPU': _config["GPU_num"]},
                            allow_soft_placement=True,
                            gpu_options=gpu_options
                            )
    session = tf.Session(config=config)
    KTF.set_session(session)

def plot_history(history):
    print(history.history.keys())
    plt.clf()
    plt.title(u'Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.legend(['training', 'valivation'], loc='upper left')
    plt.show()

    plt.title(u'Loss')
    plt.ylim(0, 3)
    plt.ylabel('Model loss')
    plt.xlabel('Epoch')
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.legend(['training', 'valivation'], loc='upper left')
    plt.show()

def pcg_metrics_cal(labels, prediction, mode, y_true, isprint=False, patient=False):
    #分条数据，比例为5:1
    # 1.分条数据，比例为3；分患者数据，比例为9
    section = 5
    ratio = section*3 if patient else section
    # 2.获得数据标签；获得患者标签
    true_index = np.arange(0, labels.shape[0], ratio)
    data_patient_label = labels.argmax(axis=1)[true_index]

    # 3.统计每条3份数据的的类别占比，获得预测标签；统计整个患者的(section*3)段数据的的类别占比，获得预测标签
    pred = prediction.argmax(axis=1)
    data_pred =  np.zeros(( int(pred.shape[0]/ratio) ))
    normal_num = np.zeros(( int(pred.shape[0]/ratio) ))  #正常的条数
    # 每条数据或者每个患者的正常数据条数
    for i in range(int(pred.shape[0]/ratio)):
        pred_scope = pred[i*ratio : (i+1)*ratio]
        normal_num[i] = np.sum(pred_scope == 0)   #计算pred_scope中的0的个数
        data_pred[i] = 0 if normal_num[i]>=math.ceil(ratio/2) else 1
    # 4.计算指标
    matrix = confusion_matrix(data_patient_label, data_pred, labels=[0,1])  #这里的标签需要更改
    TP, FN, FP, TN = matrix[0,0], matrix[0,1], matrix[1,0], matrix[1,1]
    Accuracy = (TP + TN) / np.sum(matrix) * 100
    Sensitivity = (TP / (TP + FN)) * 100            #敏感性
    Specificity = (TN / (TN + FP)) * 100            #特异性
    Precision = (TP / (TP + FP)) * 100              #查准率(准确率)
    Recall = (TP / (TP + FN)) * 100                 #查全率(召回率)
    G_mean = np.sqrt(Sensitivity * Specificity)     #几何平均分(敏感性,特异性赋予了相同权重，后面可以改为更侧重敏感性)
    F1 = 2 * (Precision * Recall)/(Precision + Recall)
    with open("log.txt", "a") as f:
        print(mode+"===>\n"+"matrix:\n{:}\nAccuracy:{:.3f}%\nSensitivity:{:.3f}%\n"
            "Specificity:{:.3f}%\nPrecision:{:.3f}%\nRecall:{:.3f}%\nG_mean:{:.3f}\nF1:{:.3f}".
          format(matrix,Accuracy,Sensitivity, Specificity, Precision, Recall, G_mean, F1),file=f)
    print("\033[32m"+ mode +"=========>\n"+ "matrix:\n{:}\nAccuracy:{:.3f}%\nSensitivity:{:.3f}%\n"
          "Specificity:{:.3f}%\nPrecision:{:.3f}%\nRecall:{:.3f}%\nG_mean:{:.3f}\nF1:{:.3f}\033[0m".
        format(matrix, Accuracy, Sensitivity, Specificity, Precision, Recall, G_mean, F1))
    # 5.转换为三分类，并输出结果
    # 5.1患者判断
    if patient:
        threshold = [2,5]  #2,5
        if isprint:  #改为3分类
            status_list = ['正常', '轻风险', '异常'] #状态
            pred_triple_class = np.zeros(( y_true.shape[0] ))  #真实类别
            #动态记录阈值
            mild_threshold, normal_threshold, normal_prob, mild_prob, severe_prob = np.zeros(1), np.zeros(1), np.zeros(1), np.zeros(1), np.zeros(1)
            #判断该患者是：正常，轻风险，异常(基于二分的结果，正常不进入轻风险和异常判断)
            for i in range(data_pred.shape[0]):
                if data_pred[i] == 0:
                    pred_triple_class[i] = 0   #正常直接判断为正常,相信二分类器
                else:
                    if normal_num[i]<threshold[0]:
                        pred_triple_class[i] = 2
                    elif (normal_num[i] >= threshold[0]) & (normal_num[i] <= threshold[1]):
                        pred_triple_class[i] = 1
                    elif normal_num[i] > threshold[1]:
                        if data_pred[i] == 1:
                            pred_triple_class[i] = 2  #二分若为异常，则不允许判为正常(实际上此处可以对判断正常的概率有一定提升，但是为了安全起见，相信二分类器)
                        else:
                            pred_triple_class[i] = 0
                pred_status = status_list[int(pred_triple_class[i])]
                true_status = status_list[int(y_true[i])]
                if pred_status == true_status == '正常':
                    #取正常对应的输出段的输出概率，然后求均值。
                    prob = prob_cal(prediction, pred_triple_class[i], i, ratio)
                    print("\033[32m患者{}识别结果为:{:s},真实结果为:{:s},正常概率为:{:.2f}%\033[0m".
                          format(i+1, pred_status, true_status, prob))
                elif pred_status == true_status == '异常':
                    prob = prob_cal(prediction, pred_triple_class[i], i, ratio)
                    normal_prob = np.append(normal_prob, prob)
                    print("\033[34m患者{}识别结果为:{:s},真实结果为:{:s},异常概率为:{:.2f}%\033[0m".
                          format(i+1, pred_status, true_status, prob))
                elif (pred_status=='轻风险') & (true_status=='轻风险'):
                    prob = prob_cal(prediction, pred_triple_class[i], i, ratio)
                    normal_prob = np.append(normal_prob, prob)
                    print("\033[34m患者{}识别结果为:{:s},真实结果为:{:s},轻风险概率为:{:.2f}%\033[0m".
                          format(i+1, pred_status, true_status, prob))
                else:
                    prob = prob_cal(prediction, pred_triple_class[i], i, ratio)
                    print("\033[31m患者{}识别结果为:{:s},真实结果为:{:s},异常概率为:{:.2f}\033[0m".
                          format(i+1, pred_status, true_status, prob))
                if true_status=='正常':
                    normal_threshold = np.append(normal_threshold, normal_num[i])
                    normal_prob = np.append(normal_prob, prob)
                elif true_status=='轻风险':
                    mild_threshold = np.append(mild_threshold, normal_num[i])
                    mild_prob = np.append(mild_prob, prob)
                elif true_status=="异常":
                    severe_prob = np.append(severe_prob, prob)

            normal_threshold = np.delete(normal_threshold, 0)
            mild_threshold = np.delete(mild_threshold,0)
            normal_prob = np.delete(normal_prob, 0)
            mild_prob = np.delete(mild_prob, 0)
            severe_prob = np.delete(severe_prob, 0)
            triple_matrix = confusion_matrix(y_true, pred_triple_class, labels=[0,1,2])
            print("患者3分类矩阵:matrix:\n{:}".format(triple_matrix))
            print("patient_classification_report:\n{}".format(classification_report(pred_triple_class, y_true,labels=[0,1,2],target_names=["normal","mild","abnormal"])))
            return mild_threshold, normal_threshold, normal_prob, mild_prob, severe_prob, data_pred
    # 5.2数据判断，判断数据是：正常，异常
    else:
        if isprint:
            status_list = ['正常', '异常']
            for i in range(data_pred.shape[0]):
                pred_status = status_list[int(data_pred[i])]
                true_status = status_list[int(data_patient_label[i])]
                if pred_status == true_status == '正常':
                    print("\033[32m数据{}识别结果为:{:s},真实结果为:{:s}\033[0m".format(i+1, pred_status, true_status))
                elif pred_status == true_status == '异常':
                    print("\033[34m数据{}识别结果为:{:s},真实结果为:{:s}\033[0m".format(i+1, pred_status, true_status))
                else:
                    print("\033[31m数据{}识别结果为:{:s},真实结果为:{:s}\033[0m".format(i+1, pred_status, true_status))
    return np.array([Accuracy, Sensitivity, Specificity, Precision, Recall, G_mean, F1]).reshape((1,7))

def ecg_metrics_cal(labels, prediction, mode, y_true, isprint=False, patient=False):
    # 分条数据，比例为5:1
    # 1.分条数据，比例为3；分v患者数据，比例为9
    section = 5
    ratio = section * 3 if patient else section
    # 2.获得数据标签；获得患者标签
    true_index = np.arange(0, labels.shape[0], ratio)
    data_patient_label = labels.argmax(axis=1)[true_index]

    # 3.统计每条3份数据的的类别占比，获得预测标签；统计整个患者的(section*3)段数据的的类别占比，获得预测标签
    pred = prediction.argmax(axis=1)
    data_pred = np.zeros((int(pred.shape[0] / ratio)))
    normal_num = np.zeros((int(pred.shape[0] / ratio)))  # 正常的条数
    # 每条数据或者每个患者的正常数据条数
    for i in range(int(pred.shape[0] / ratio)):
        pred_scope = pred[i * ratio: (i + 1) * ratio]
        normal_num[i] = np.sum(pred_scope == 0)  # 计算pred_scope中的0的个数
        data_pred[i] = 0 if normal_num[i] >= math.ceil(ratio / 2) else 1
    # 4.计算指标
    matrix = confusion_matrix(data_patient_label, data_pred, labels=[0, 1])  # 这里的标签需要更改
    TP, FN, FP, TN = matrix[0, 0], matrix[0, 1], matrix[1, 0], matrix[1, 1]
    Accuracy = (TP + TN) / np.sum(matrix) * 100
    Sensitivity = (TP / (TP + FN)) * 100  # 敏感性
    Specificity = (TN / (TN + FP)) * 100  # 特异性
    Precision = (TP / (TP + FP)) * 100  # 查准率(准确率)
    Recall = (TP / (TP + FN)) * 100  # 查全率(召回率)
    G_mean = np.sqrt(Sensitivity * Specificity)  # 几何平均分(敏感性,特异性赋予了相同权重，后面可以改为更侧重敏感性)
    F1 = 2 * (Precision * Recall) / (Precision + Recall)
    with open("log.txt", "a") as f:
        print(mode + "===>\n" + "matrix:\n{:}\nAccuracy:{:.3f}%\nSensitivity:{:.3f}%\n"
                                "Specificity:{:.3f}%\nPrecision:{:.3f}%\nRecall:{:.3f}%\nG_mean:{:.3f}\nF1:{:.3f}".
              format(matrix, Accuracy, Sensitivity, Specificity, Precision, Recall, G_mean, F1), file=f)
    print("\033[32m" + mode + "=========>\n" + "matrix:\n{:}\nAccuracy:{:.3f}%\nSensitivity:{:.3f}%\n"
                                               "Specificity:{:.3f}%\nPrecision:{:.3f}%\nRecall:{:.3f}%\nG_mean:{:.3f}\nF1:{:.3f}\033[0m".
          format(matrix, Accuracy, Sensitivity, Specificity, Precision, Recall, G_mean, F1))
    # 5.转换为三分类，并输出结果
    # 5.1患者判断
    if patient:
        threshold = [2, 5]  # 2,5
        if isprint:  # 改为3分类
            status_list = ['正常', '轻风险', '异常']  # 状态
            pred_triple_class = np.zeros((y_true.shape[0]))  # 真实类别
            # 动态记录阈值
            mild_threshold, normal_threshold, normal_prob, mild_prob, severe_prob =\
                np.zeros(1), np.zeros(1), np.zeros(1), np.zeros(1), np.zeros(1)
            # 判断该患者是：正常，轻风险，异常(基于二分的结果，正常不进入轻风险和异常判断)
            for i in range(data_pred.shape[0]):
                if data_pred[i] == 0:
                    pred_triple_class[i] = 0  # 正常直接判断为正常,相信二分类器
                else:
                    if normal_num[i] < threshold[0]:
                        pred_triple_class[i] = 2
                    elif (normal_num[i] >= threshold[0]) & (normal_num[i] <= threshold[1]):
                        pred_triple_class[i] = 1
                    elif normal_num[i] > threshold[1]:
                        if data_pred[i] == 1:
                            pred_triple_class[i] = 2  # 二分若为异常，则不允许判为正常(实际上此处可以对判断正常的概率有一定提升，但是为了安全起见，相信二分类器)
                        else:
                            pred_triple_class[i] = 0
                pred_status = status_list[int(pred_triple_class[i])]
                true_status = status_list[int(y_true[i])]
                if pred_status == true_status == '正常':
                    # 取正常对应的输出段的输出概率，然后求均值。
                    prob = prob_cal(prediction, pred_triple_class[i], i, ratio)
                    print("\033[32m患者{}识别结果为:{:s},真实结果为:{:s},正常概率为:{:.2f}%\033[0m".
                          format(i + 1, pred_status, true_status, prob))
                elif pred_status == true_status == '异常':
                    prob = prob_cal(prediction, pred_triple_class[i], i, ratio)
                    normal_prob = np.append(normal_prob, prob)
                    print("\033[34m患者{}识别结果为:{:s},真实结果为:{:s},异常概率为:{:.2f}%\033[0m".
                          format(i + 1, pred_status, true_status, prob))
                elif (pred_status == '轻风险') & (true_status == '轻风险'):
                    prob = prob_cal(prediction, pred_triple_class[i], i, ratio)
                    normal_prob = np.append(normal_prob, prob)
                    print("\033[34m患者{}识别结果为:{:s},真实结果为:{:s},轻风险概率为:{:.2f}%\033[0m".
                          format(i + 1, pred_status, true_status, prob))
                else:
                    prob = prob_cal(prediction, pred_triple_class[i], i, ratio)
                    print("\033[31m患者{}识别结果为:{:s},真实结果为:{:s},异常概率为:{:.2f}\033[0m".
                          format(i + 1, pred_status, true_status, prob))
                if true_status == '正常':
                    normal_threshold = np.append(normal_threshold, normal_num[i])
                    normal_prob = np.append(normal_prob, prob)
                elif true_status == '轻风险':
                    mild_threshold = np.append(mild_threshold, normal_num[i])
                    mild_prob = np.append(mild_prob, prob)
                elif true_status == "异常":
                    severe_prob = np.append(severe_prob, prob)
                ######################轻风险二分类效果查看
            print("\033[35m\n\n轻风险二分类效果查看:\033[0m")
            for i in range(data_pred.shape[0]):
                true_status = status_list[int(y_true[i])]
                if true_status == "轻风险":
                    if data_pred[i] == 0:
                        view_status = "正常"
                        print("\033[32m识别结果为:{:s},真实结果为:{:s}\033[0m".format( view_status, true_status))
                    else:
                        view_status = "异常"
                        print("\033[31m识别结果为:{:s},真实结果为:{:s}\033[0m".format( view_status, true_status))
                ######################轻风险二分类效果查看
            normal_threshold = np.delete(normal_threshold, 0)
            mild_threshold = np.delete(mild_threshold, 0)
            normal_prob = np.delete(normal_prob, 0)
            mild_prob = np.delete(mild_prob, 0)
            severe_prob = np.delete(severe_prob, 0)
            triple_matrix = confusion_matrix(y_true, pred_triple_class, labels=[0, 1, 2])
            print("患者3分类矩阵:matrix:\n{:}".format(triple_matrix))
            print("patient_classification_report:\n{}".format(
                classification_report(pred_triple_class, y_true, labels=[0, 1, 2],
                                      target_names=["normal", "mild", "abnormal"])))
            return mild_threshold, normal_threshold, normal_prob, mild_prob, severe_prob, data_pred
    # 5.2数据判断，判断数据是：正常，异常
    else:
        if isprint:
            status_list = ['正常', '异常']
            for i in range(data_pred.shape[0]):
                pred_status = status_list[int(data_pred[i])]
                true_status = status_list[int(data_patient_label[i])]
                if pred_status == true_status == '正常':
                    print("\033[32m数据{}识别结果为:{:s},真实结果为:{:s}\033[0m".format(i + 1, pred_status, true_status))
                elif pred_status == true_status == '异常':
                    print("\033[34m数据{}识别结果为:{:s},真实结果为:{:s}\033[0m".format(i + 1, pred_status, true_status))
                else:
                    print("\033[31m数据{}识别结果为:{:s},真实结果为:{:s}\033[0m".format(i + 1, pred_status, true_status))
    return np.array([Accuracy, Sensitivity, Specificity, Precision, Recall, G_mean, F1]).reshape((1, 7))

def sub1_model_test(root1, x_test_name, y_test_label, y_test_true_label, scaler, model_path=None):
    # 1.加载测试数据
    # f = io.open('_config.yaml', 'r', encoding="utf-8")
    # _config = yaml.load(f)
    print("进入PCG测试")
    x_test, y_test, sample_rate = load_data(root1, x_test_name, y_test_label, 5)
    # 2.提取mfcc特征
    x_test = dataset_getmfcc(x_test, sample_rate)
    # 3.特征归一化
    x_test, _ = data_normalization(scaler, raw_train=0, raw_test=x_test)
    x_test = x_test[:, :, :, np.newaxis] # 维度变换
    y_test = keras.utils.to_categorical(y_test, 2)  #独热编码
    # 4.加载模型
    if model_path!=None:
        model = load_model(model_path)
    # 5.前向预测
    y_pred = model.predict(x_test)
    print("\033[32m数据测试\033[0m")
    pcg_metrics_cal(y_test, y_pred, "test", y_test_true_label, isprint=False, patient=False)
    print("\033[32m患者测试\033[0m")
    mild_threshold, normal_threshold, normal_prob, mild_prob, severe_prob, double_results = \
        pcg_metrics_cal(y_test, y_pred, "test", y_test_true_label, isprint=True, patient=True)
    return double_results

def sub2_model_test(root2, x_test_name, y_test_label, y_test_true_label, scaler, model_path=None):
    # 1.加载测试数据
    # f = io.open('_config.yaml', 'r', encoding="utf-8")
    # _config = yaml.load(f)
    print("进入ECG测试")
    x_test, y_test, sample_rate = _load_data(root2, x_test_name, y_test_label, 5)
    # 2.特征归一化
    x_test = x_test.transpose()
    x_test, _ = _data_normalization(scaler, raw_train=0, raw_test=x_test)
    x_test = x_test[:, :, np.newaxis]  # 维度变换
    y_test = keras.utils.to_categorical(y_test, 2)  # 独热编码
    # 3.加载模型
    if model_path != None:
        model = load_model(model_path)
    # 4.前向预测
    y_pred = model.predict(x_test)
    print("\033[32m数据测试\033[0m")
    ecg_metrics_cal(y_test, y_pred, "test", y_test_true_label, isprint=False, patient=False)
    print("\033[32m患者测试\033[0m")
    mild_threshold, normal_threshold, normal_prob, mild_prob, severe_prob, double_class_results = \
        ecg_metrics_cal(y_test, y_pred, "test", y_test_true_label,isprint=True, patient=True)
    return double_class_results

def threshold_test(data_path, model_list, scaler1, scaler2):
    # 分别用不同的k_folds来取出轻风险不同标签的验证数据，但是患者是相同的，只是轻风险标签不同，将数据分别送入两个子分类器进行分类。
    # f = io.open('_config.yaml', 'r', encoding="utf-8")
    # _config = yaml.load(f)
    all_metrics = np.zeros((1, 7))
    matrix = np.zeros((3,3))
    '''model_list = [["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-0_val_loss-0.59_epoch-40_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_0val_loss-0.40_epoch-239_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-1_val_loss-0.38_epoch-06_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_1val_loss-0.30_epoch-35_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-2_val_loss-0.27_epoch-06_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_2val_loss-0.43_epoch-234_ECG_model.hdf5",],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-3_val_loss-0.52_epoch-07_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_3val_loss-0.48_epoch-243_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-4_val_loss-0.50_epoch-02_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_4val_loss-0.52_epoch-118_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-5_val_loss-0.34_epoch-08_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_5val_loss-0.37_epoch-181_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-6_val_loss-0.40_epoch-09_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_6val_loss-0.38_epoch-62_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-7_val_loss-0.26_epoch-04_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_7val_loss-0.29_epoch-327_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-8_val_loss-0.32_epoch-07_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_8val_loss-0.44_epoch-232_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-9_val_loss-0.53_epoch-02_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_9val_loss-0.48_epoch-34_ECG_model.hdf5"]]'''
    root_1, x_kf_train_1, y_kf_train_1, x_kf_valid_1, y_kf_valid_1, y_kf_true_train_1, y_kf_true_valid_1 = \
        _k_folds(data_path, 10, sub=1)
    root_2, x_kf_train_2, y_kf_train_2, x_kf_valid_2, y_kf_valid_2, y_kf_true_train_2, y_kf_true_valid_2 = \
        _k_folds(data_path, 10, sub=2)
    for i in range(0, 10):
        print("\033[31mFolds:{:d}===========================================>\033[0m".format(i + 1))
        sub_1_results = sub1_model_test(root_1, x_kf_valid_1[i], y_kf_valid_1[i], y_kf_true_valid_1[i], scaler1, model_list[0])
        sub_2_results = sub2_model_test(root_2, x_kf_valid_2[i], y_kf_valid_2[i], y_kf_true_valid_2[i], scaler2, model_list[1])
        this_martix = decision_fusion(y_kf_true_valid_1[i], sub_1_results, sub_2_results)
        matrix += this_martix
        if i == 1: break

    # 11.交叉验证训练指标计算
    '''all_metrics = np.delete(all_metrics, 0, axis=0)  # 删掉0行
    macro_metrics = np.mean(all_metrics, axis=0)
    macro_F1 = 2 * (macro_metrics[3] * macro_metrics[4]) / (macro_metrics[3] + macro_metrics[4])
    print("\033[32mmacro results:\nAccuracy:{:.3f}%\nSensitivity:{:.3f}%\nSpecificity:{:.3f}%\nPrecision:{:.3f}%\nRecall:{:.3f}%\nG_mean:{:.3f}\nF1:{:.3f}\033[0m".
        format(macro_metrics[0], macro_metrics[1], macro_metrics[2], macro_metrics[3], macro_metrics[4],
               macro_metrics[5], macro_F1))'''
    print("交叉验证所有矩阵之和:matrix:\n{:}".format(matrix))

def decision_fusion(y_true, sub_1_results, sub_2_results):
    final_results = np.zeros(1)
    for i in range(sub_1_results.shape[0]):
        #1.相同则不变
        if sub_1_results[i] == sub_2_results[i] == 0:
            final_results = np.append(final_results, 0)
        elif sub_1_results[i] == sub_2_results[i] == 1:
            final_results = np.append(final_results, 2)
        #2.PCG异常，ECG正常则判定为轻风险
        elif (sub_1_results[i]==1) and (sub_2_results[i]==0):
            final_results = np.append(final_results, 1)
        #3.PCG正常，ECG异常则相信PCG分类
        elif (sub_1_results[i]==0) and (sub_2_results[i]==1):
            final_results = np.append(final_results, 0)
    final_results = np.delete(final_results, 0)
    triple_matrix = confusion_matrix(y_true, final_results, labels=[0, 1, 2])
    print("融合患者3分类矩阵:matrix:\n{:}".format(triple_matrix))
    print("patient_classification_report:\n{}".format(classification_report(final_results, y_true,
        labels=[0, 1, 2], target_names=["normal", "mild", "abnormal"])))
    return triple_matrix

def dataset_test(data_path, model_list, scaler1, scaler2):
    print("进入测试")
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=UserWarning)
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        threshold_test(data_path, model_list, scaler1, scaler2)

if __name__ == "__main__":
    '''model_list = [["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-0_val_loss-0.59_epoch-40_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_0val_loss-0.40_epoch-239_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-1_val_loss-0.38_epoch-06_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_1val_loss-0.30_epoch-35_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-2_val_loss-0.27_epoch-06_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_2val_loss-0.43_epoch-234_ECG_model.hdf5",],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-3_val_loss-0.52_epoch-07_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_3val_loss-0.48_epoch-243_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-4_val_loss-0.50_epoch-02_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_4val_loss-0.52_epoch-118_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-5_val_loss-0.34_epoch-08_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_5val_loss-0.37_epoch-181_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-6_val_loss-0.40_epoch-09_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_6val_loss-0.38_epoch-62_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-7_val_loss-0.26_epoch-04_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_7val_loss-0.29_epoch-327_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-8_val_loss-0.32_epoch-07_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_8val_loss-0.44_epoch-232_ECG_model.hdf5"],
                  ["E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-9_val_loss-0.53_epoch-02_PCG_model.hdf5","E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/release_test/Model/9.21/5_percentage/_folds_9val_loss-0.48_epoch-34_ECG_model.hdf5"]]'''
    # f = open("_config.yaml", 'r', encoding="utf-8")
    # _config = yaml.load(f)
    # computing_resource(_config)
    # model_fusion()

    '''scaler1 = pickle.load(open('E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/Model/scaler/scaler_8_30_triple.pkl', 'rb'))
    scaler2 = pickle.load(open('E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/Model/scaler/scaler_9_11_1,3_4.pkl', 'rb'))
    data_path = "D:/Dataset/PCG_project/My_data/zaoying/all_zaoying/1,3_4/train"
    model_list = [
        "E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/Model/9.21/9.21_5percentage_CL_All_CDG_Model/_folds-7_val_loss-0.26_epoch-04_PCG_model.hdf5",
        "E:/Postgraduate work/Literature/PCG/PCG_Projects/release_demo/Model/9.21/5_percentage/_folds_7val_loss-0.29_epoch-327_ECG_model.hdf5"]
    dataset_test(data_path, model_list, scaler1, scaler2)'''
