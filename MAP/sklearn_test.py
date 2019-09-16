import pandas as pd
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
csv = pd.read_csv('sanbul2.csv',encoding='cp949', sep=',',header=0)
csv.columns = csv.columns.str.replace(' ','_')

csv.loc[csv['피해면적_합계'] >= 3, '피해면적'] =1
csv.loc[csv['피해면적_합계'] >= 5, '피해면적'] =2
csv.loc[csv['피해면적_합계'] >= 7, '피해면적'] =3
csv.loc[csv['피해면적_합계'] >= 13, '피해면적'] =4
csv.loc[csv['피해면적_합계'] >= 50, '피해면적'] =5
csv.loc[csv['피해면적_합계'] >= 200, '피해면적'] =6

csv.loc[csv['발생원인_구분'] == '건', '발생원인'] =1
csv.loc[csv['발생원인_구분'] == '기', '발생원인'] =2
csv.loc[csv['발생원인_구분'] == '논', '발생원인'] =3
csv.loc[csv['발생원인_구분'] == '담', '발생원인'] =4
csv.loc[csv['발생원인_구분'] == '성', '발생원인'] =5
csv.loc[csv['발생원인_구분'] == '쓰', '발생원인'] =6
csv.loc[csv['발생원인_구분'] == '어', '발생원인'] =7
csv.loc[csv['발생원인_구분'] == '입', '발생원인'] =8

print(csv['피해면적'])

csv_data = csv[[ '발생일시_일','기온', '습도', '풍향','발생원인']]
csv_label = csv['피해면적']
for index in range(len(pre)):
    train_data, test_data, train_label, test_label = train_test_split(csv_data, csv_label, shuffle=None)
    clf = svm.SVC(gamma='auto')
    clf.fit(train_data, train_label)
    pre = clf.predict(test_data)
    ac_score = metrics.accuracy_score(test_label, pre)


print('전체 데이터 수: %d' %len(csv_data))
print('학습 전용 데이터 수: %d' %len(train_data))
print('테스트 데이터 수: %d' %(len(test_data)))
print('정답률: ', ac_score*100, '%')