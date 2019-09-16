

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split

import tensorflow as tf
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
# print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


csv = pd.read_csv('sanbul4.csv',encoding='cp949', sep=',',header=0)
csv.columns = csv.columns.str.replace(' ','_')
csv.loc[csv['피해면적_합계'] < 0.5, '피해면적'] =1
csv.loc[csv['피해면적_합계'] >= 0.5, '피해면적'] =2
csv.loc[csv['피해면적_합계'] >= 1, '피해면적'] =3
csv.loc[csv['피해면적_합계'] >= 2, '피해면적'] =4
csv.loc[csv['피해면적_합계'] >= 3, '피해면적'] =5
csv.loc[csv['피해면적_합계'] >= 5, '피해면적'] =6
csv.loc[csv['피해면적_합계'] >= 7, '피해면적'] =7
csv.loc[csv['피해면적_합계'] >= 13, '피해면적'] =8
csv.loc[csv['피해면적_합계'] >= 50, '피해면적'] =9
csv.loc[csv['피해면적_합계'] >= 200, '피해면적'] =10

csv.loc[csv['발생원인_구분'] == '건', '발생원인'] =1
csv.loc[csv['발생원인_구분'] == '기', '발생원인'] =2
csv.loc[csv['발생원인_구분'] == '논', '발생원인'] =3
csv.loc[csv['발생원인_구분'] == '담', '발생원인'] =4
csv.loc[csv['발생원인_구분'] == '성', '발생원인'] =5
csv.loc[csv['발생원인_구분'] == '쓰', '발생원인'] =6
csv.loc[csv['발생원인_구분'] == '어', '발생원인'] =7
csv.loc[csv['발생원인_구분'] == '입', '발생원인'] =8

csv=csv.dropna(how='any')
# iris = pd.read_csv('./Iris2.csv', index_col = 0)
formula=['발생일시_년','발생일시_월','발생원인','발생일시_일','습도','풍향','풍속','기온']
# iris["Species"] = iris["Species"].map({"Iris-setosa":0,"Iris-virginica":1,"Iris-versicolor":2})
# csv.iloc[:,1:4] = csv.iloc[:,1:4].astype(np.float32)
csv[formula] = csv[formula].astype(np.float32)
X_train, X_test, y_train, y_test = train_test_split(csv[formula], csv["발생원인"], test_size=0.33, random_state=42)

columns = csv[formula]

feature_columns = [tf.contrib.layers.real_valued_column(k) for k in columns]

def input_fn(df,labels):
    feature_cols = {k:tf.constant(df[k].values,shape = [df[k].size,1]) for k in columns}
    label = tf.constant(labels.values, shape = [labels.size,1])
    return feature_cols,label

classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,hidden_units=[10,20,10],n_classes = 3)
cross=classifier.fit(input_fn=lambda: input_fn(X_train,y_train),steps = 1000)
print(cross)
ev = classifier.evaluate(input_fn=lambda: input_fn(X_test,y_test),steps=1)
print(ev)