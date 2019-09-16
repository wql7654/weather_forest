#랜덤포레스트를 이용하여 산불면적 예측

import pandas as pd
from itertools import combinations
import operator
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

#pip install pandas
#pip install operator
#pip install sklearn

csv = pd.read_csv('sanbul4.csv',encoding='cp949', sep=',',header=0) #판다스로 csv파일을 불러옴
csv.columns = csv.columns.str.replace(' ','_')

csv.loc[csv['피해면적_합계'] < 0.5, '피해면적'] =1 #화재의 면적범위가 넓어서 10개로 나누어줌
csv.loc[csv['피해면적_합계'] >= 0.5, '피해면적'] =2
csv.loc[csv['피해면적_합계'] >= 1, '피해면적'] =3
csv.loc[csv['피해면적_합계'] >= 2, '피해면적'] =4
csv.loc[csv['피해면적_합계'] >= 3, '피해면적'] =5
csv.loc[csv['피해면적_합계'] >= 5, '피해면적'] =6
csv.loc[csv['피해면적_합계'] >= 7, '피해면적'] =7
csv.loc[csv['피해면적_합계'] >= 13, '피해면적'] =8
csv.loc[csv['피해면적_합계'] >= 50, '피해면적'] =9
csv.loc[csv['피해면적_합계'] >= 200, '피해면적'] =10

csv.loc[csv['발생원인_구분'] == '건', '발생원인'] =1 #문자로 되어있는 데이터를 수치로 변경
csv.loc[csv['발생원인_구분'] == '기', '발생원인'] =2
csv.loc[csv['발생원인_구분'] == '논', '발생원인'] =3
csv.loc[csv['발생원인_구분'] == '담', '발생원인'] =4
csv.loc[csv['발생원인_구분'] == '성', '발생원인'] =5
csv.loc[csv['발생원인_구분'] == '쓰', '발생원인'] =6
csv.loc[csv['발생원인_구분'] == '어', '발생원인'] =7
csv.loc[csv['발생원인_구분'] == '입', '발생원인'] =8



csv=csv.dropna(how='any') #빈 데이터 삭제

formula=['발생일시_년','발생일시_월','발생원인','발생일시_일','습도','풍향','풍속','기온'] # 학습할 데이터
csv_label = csv['피해면적'] #예측할 데이터
match_dic1={}
for num in range(1,len(formula)):
    combi_list = list(combinations(formula,num))
    for tup in combi_list:
        xor_dat=csv[list(tup)]
        X_train, X_test, y_train, y_test = train_test_split(xor_dat, csv_label, shuffle=None) #데이터를 7:3으로 나누어줌
        forest = RandomForestClassifier(n_estimators=100, random_state=0) #랜덤포레스트 (이진트리 100개사용)
        forest.fit(X_train, y_train) #데이터 학습
        print("훈련 세트 정확도 : {:.3f}".format(forest.score(X_train, y_train)))
        print("테스트 세트 정확도 : {:.3f}".format(forest.score(X_test, y_test)))
        print("특성 중요도 : \n{}".format(forest.feature_importances_))

        match_dic1[tup] = (forest.score(X_test, y_test) * 100)



match_dic1 = sorted(match_dic1.items(), key=operator.itemgetter(1),reverse=True) # 가장높은 확률 찾기


print('총 조합 갯수: %d'%len(match_dic1))
print("metrics MAX 조합:",match_dic1[0]) #얘측률
