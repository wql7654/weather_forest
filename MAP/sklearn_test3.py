import pandas as pd
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
csv = pd.read_csv('andong2.csv',encoding='cp949', sep=',',header=0)
csv.columns = csv.columns.str.replace(' ','_')
csv=csv.dropna(how='any')

print(csv)
csv_data = csv[[ '기온', '습도', '풍향','풍속']]
csv_label = csv['산불']

train_data, test_data, train_label, test_label = train_test_split(csv_data, csv_label, shuffle=None)
clf = svm.SVC(gamma='auto')
clf.fit(train_data, train_label)
pre = clf.predict(test_data)
ac_score = metrics.accuracy_score(test_label, pre)
mat=confusion_matrix(test_label, pre)


print('전체 데이터 수: %d' %len(csv_data))
print('학습 전용 데이터 수: %d' %len(train_data))
print('테스트 데이터 수: %d' %(len(test_data)))
print('정답률: ', ac_score*100, '%')
print(mat)