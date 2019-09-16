import pandas as pd
from sklearn import svm,metrics
from itertools import combinations
import numpy as np
import operator

from sklearn.model_selection import train_test_split
# from sklearn.metrics import confusion_matrix



csv = pd.read_csv('sanbul4.csv',encoding='cp949', sep=',',header=0)
csv.columns = csv.columns.str.replace(' ','_')
# csv.loc[csv['피해면적_합계'] < 0.5, '피해면적'] =1
# csv.loc[csv['피해면적_합계'] >= 0.5, '피해면적'] =2
# csv.loc[csv['피해면적_합계'] >= 1, '피해면적'] =3
# csv.loc[csv['피해면적_합계'] >= 2, '피해면적'] =4
# csv.loc[csv['피해면적_합계'] >= 3, '피해면적'] =5
# csv.loc[csv['피해면적_합계'] >= 5, '피해면적'] =6
# csv.loc[csv['피해면적_합계'] >= 7, '피해면적'] =7
# csv.loc[csv['피해면적_합계'] >= 13, '피해면적'] =8
# csv.loc[csv['피해면적_합계'] >= 50, '피해면적'] =9
# csv.loc[csv['피해면적_합계'] >= 200, '피해면적'] =10

csv.loc[csv['피해면적_합계'] <= 1, '피해면적'] =csv['피해면적_합계']

csv.loc[csv['발생원인_구분'] == '건', '발생원인'] =1
csv.loc[csv['발생원인_구분'] == '기', '발생원인'] =2
csv.loc[csv['발생원인_구분'] == '논', '발생원인'] =3
csv.loc[csv['발생원인_구분'] == '담', '발생원인'] =4
csv.loc[csv['발생원인_구분'] == '성', '발생원인'] =5
csv.loc[csv['발생원인_구분'] == '쓰', '발생원인'] =6
csv.loc[csv['발생원인_구분'] == '어', '발생원인'] =7
csv.loc[csv['발생원인_구분'] == '입', '발생원인'] =8



csv=csv.dropna(how='any')
formula=['발생일시_년','발생일시_월','발생원인','발생일시_일','습도','풍향','풍속','기온']
csv_label = csv['피해면적']
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
for num in range(1,len(formula)):
    combi_list = list(combinations(formula,num))
    for tup in combi_list:

        wine_df = pd.DataFrame(csv)
        xor_dat=csv[list(tup)]
        train_data, test_data, train_label, test_label = train_test_split(xor_dat, csv_label, shuffle=None)

        clf = svm.SVC(gamma='auto')
        clf.fit(train_data, train_label)
        pre = clf.predict(test_data)
        ac_score = metrics.accuracy_score(test_label, pre)

        match_count0 = 0
        match_count=0
        match_count1 = 0
        match_count2 = 0


        print('\n>> ',tup)
        print('>> 정답률: %.2f %%'%(ac_score*100))
        # mat = confusion_matrix(test_label, pre)
        # print("matrix:", mat)
        match_dic1[tup]=(ac_score*100)

        # match_dic['%s' % list_data] = '.2f %%%' % (
        #             match_count / len(y_predicted_rounded) * 100)
        # match_dic2['%s' %list_data] = '%.2f %%' % (
        #             match_count1 / len(y_predicted_rounded) * 100)
        # match_dic3['%s' % list_data] = '%.2f %%' % (
        #             match_count2 / len(y_predicted_rounded) * 100)



# 최대값 찾기
match_dic1 = sorted(match_dic1.items(), key=operator.itemgetter(1),reverse=True)

# print(match_dic)+
print('총 조합 갯수: %d'%len(match_dic1))
print("metrics MAX 조합:",match_dic1[0])

