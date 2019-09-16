import pandas as pd
from sklearn import svm,metrics
from itertools import combinations
import operator
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt



csv = pd.read_csv('hwasung2.csv',encoding='cp949', sep=',',header=0)
csv.columns = csv.columns.str.replace(' ','_')



csv=csv.dropna(how='any')
formula=['습도','풍향','풍속','기온']
csv_label = csv['산불']
match_dic0={}

match_dic1={}
match_dic={}
match_dic2={}
match_dic3={}
# print(wine)
err_cnt0=0.0
err_cnt=0.05
err_cnt2=0.1
err_cnt3=0.2
for num in range(4,len(formula)+1):
    combi_list = list(combinations(formula,num))
    for tup in combi_list:

        wine_df = pd.DataFrame(csv)
        xor_dat=csv[list(tup)]
        X_train, X_test, y_train, y_test = train_test_split(xor_dat, csv_label, shuffle=None)
        forest = RandomForestClassifier(n_estimators=100, random_state=0)
        forest.fit(X_train, y_train)
        print("훈련 세트 정확도 : {:.3f}".format(forest.score(X_train, y_train)))
        print("테스트 세트 정확도 : {:.3f}".format(forest.score(X_test, y_test)))
        # 특성 중요도
        print("특성 중요도 : \n{}".format(forest.feature_importances_))

        match_dic1[tup] = (forest.score(X_test, y_test) * 100)


        # match_dic['%s' % list_data] = '.2f %%%' % (
        #             match_count / len(y_predicted_rounded) * 100)
        # match_dic2['%s' %list_data] = '%.2f %%' % (
        #             match_count1 / len(y_predicted_rounded) * 100)
        # match_dic3['%s' % list_data] = '%.2f %%' % (
        #             match_count2 / len(y_predicted_rounded) * 100)



# 최대값 찾기
# match_dic1 = sorted(match_dic1.items(), key=operator.itemgetter(1),reverse=True)

# print(match_dic)+
# print('총 조합 갯수: %d'%len(match_dic1))
print("metrics MAX 조합:",match_dic1)
