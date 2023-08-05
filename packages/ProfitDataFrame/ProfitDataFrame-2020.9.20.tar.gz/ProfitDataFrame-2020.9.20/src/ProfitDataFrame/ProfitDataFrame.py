#!/usr/bin/env python
# coding: utf-8
#author : Zhang Chuanpeng 张传鹏 
#nickname :Zhang Xuanjin 张玄瑾 / yz7zzxj001
#updated in  2020年9月15日
#2020/5/26 profit q_info to suit whose index does not begins with 0
#2020/5/27 fixing the5th which it goes well on my pc ,but mistake on others
#2020/9/15 add 3 fuctions: gap_statistic finds best K in kmeans
#          dup_corr show the corr between duplications 
#          sta_describe show the kde and joinplot of numberic and bar of object
#          增加了三个函数：区间间隔统计法寻找最优K值，重复值相关性探究每列重复值之间得相关性，以及数据分布描述

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns



class Profitdataframe(pd.DataFrame):
    '''
    it's a package for myself to do somethings in ELT automatically。
    此包构建的目的是为了在EDA过程中自动化处理一些问题
    目前写了几个方法：
    q_info 方法是对原df.info()的重构。返回一个DataFrame,包含原表的列名、各列总计数目、非空、空、空率、字段类型、前五预览
    q_view 方法将原本pd.plotting.scatter_matrix(df) 缩写,即查看各列间的相关性
    q_tips 方法塞入了一些常用的命令，方便复制修改
    '''
    
    def q_info(self):
        '''
        it's a functhon which make a info with null_percent infos and traditional df.info()
        '''
        ind = self.index
        col = self.columns
        ind_len = len(ind)
        col_len = len(col)
        df = pd.DataFrame(columns = ['total_count',
                                     'non_null_count',
                                     'null_count',
                                     'null_percent',
                                     'ddtype',
                                     '5th_view',])
        for i in col:
            #the5th = ','.join([str(self[i][self.index[j]]) for j in range(5)])
            value = {'total_count':ind_len,
                     'non_null_count':self[i].count(),
                     'null_count':self[i].isnull().sum(),
                     'null_percent':self[i].isnull().sum()/ind_len,
                     'ddtype':self[i].dtype
                     #'5th_view':the5th
                    }
            temp = pd.Series(value,name = i)
            df.loc[i] =temp
        return df

    def q_view(self):
        pd.plotting.scatter_matrix(self)

    def sta_describe(self,y_colname=None): 
        for i in self.columns:
            if self[i].dtype != 'object': 
                plt.figure(figsize = (10,6))
                sns.kdeplot(self[i],legend = True)
                if y_colname:
                    plt.figure(figsize = (10,6))
                    sns.joinplot(i,y_colname,data=self,kind='reg')
            else:
                plt.figure(figsize = (10,6))
                sns.barplot(self[i])
        
    def q_tips(self,code = 0):
        if code == 0:
            print(r'code menu is online','code=0 means find this menu',
                 r'code = 1 means find shell for active-out',
                 r'code = 2 means find shell for wrongs in plot',
                 r'code = 3 find what in this model'
                 ,sep = '\n')
        if code == 1 :
            print(r"from IPython.core.interactiveshell import InteractiveShell",
                  r"InteractiveShell.ast_node_interactivity = 'all'"
                 ,sep = '\n')
        if code == 2 :
            print(r"# 解决坐标轴刻度负号乱码 plt.rcParams['axes.unicode_minus'] = False",
                  r"# 解决中文乱码问题(上) plt.rcParams['font.sans-serif'] = ['Simhei']",
                  r"解决中文乱码问题(下) plt.rcParams[‘font.family’] = 'Arial Unicode MS'"
                  r"sns.set_style('whitegrid',{'font.sans-serif':['simhei','Arial']})"
            ,sep = '/n')
        if code == 3:
            print(r".q_info() show the infos of dataframe",
                r".q_view() show the scatter_matrix of dataframe",
                r".q_tips(code = 0) show the menu of this module",
                r"gap_statistic(X,B = 10,K=range(1,11)) find the best K by gap_statistic in KMeanns",
                r"dup_corr(X,nodatetime) show the corr of duplications in X . nodatetime means datatimeindex not in dups",
                r".sta_describe(y_colname=None) show the kde and joinplot of numberic and bar of object"
                ,sep = '\r\n')


def short_pair_wise_D(each_cluster):
    mu = each_cluster.mean(axis=0)
    Dk = sum(sum((each_cluster-mu)**2))*2.0*each_cluster.shape[0]
    return Dk

def compute_Wk(data,classfication_result):
    Wk=0
    label_set = set(classfication_result)
    for label in label_set:
        each_cluster = data[classfication_result==label,:]
        Wk += short_pair_wise_D(each_cluster)/(2.0*each_cluster.shape[0])
    return Wk

def gap_statistic(X,B=10,K= range(1,11),N_init=10):
    """使用区间间隔统计方法寻找最优K值得主函数"""
    X = np.array(X)
    shapes = X.shape
    tops = X.max(axis = 0)
    bots = X.min(axis = 0)
    dists = np.matrix(np.diag(tops - bots))
    rands = np.random.random_sample(size = (B,shapes[0],shapes[1]))
    for i in range(B):
        rands[i,:,:] = rands[i,:,:]*dists+bots
    
    gaps = np.zeros(len(K))
    Wks = np.zeros(len(K))
    Wkbs = np.zeros((len(K),B))
    
    for idxk,k in enumerate(K):
        k_means = KMeans(n_clusters = k)
        k_means.fit(X)
        classification_result = k_means.labels_
        Wks[idxk] = compute_Wk(X,classification_result)
        
        for i in range(B):
            Xb = rands[1,:,:]
            k_means.fit(Xb)
            classification_result_b = k_means.labels_
            Wkbs[idxk,i] = compute_Wk(Xb,classification_result_b)
    
    gaps =(np.log(Wkbs)).mean(axis=1)-np.log(Wks)
    sd_ks = np.std(np.log(Wkbs),axis=1)
    sk = sd_ks * np.sqrt(1+1.0/B)
    
    gapDiff = gaps[:-1] - gaps[1:] + sk[1:]
    plt.bar(np.arange(len(gapDiff))+1,gapDiff)
    plt.xlabel('k')
    plt.ylabel('gapdiff')
    plt.show()

def dup_corr(x,nodatetime = True):
    """注意，这里只判断dtype为object的重复值情况，因为如int/period/float重复值是没啥意义的"""
    tempdf = pd.DataFrame()
    for i in x.columns:
        if nodatetime:
            if x.loc[:,i].dtype == 'object':
                tempdf[i] = x.loc[:,i].duplicated()
        else:
            if (x.loc[:,i].dtype == 'object') or (x.loc[:,i].dtype == 'DatetimeIndex'):
                tempdf[i] = x.loc[:,i].duplicated()
    plt.figure(figsize =(10,10))
    sns.heatmap(tempdf.corr(),annot = True)






