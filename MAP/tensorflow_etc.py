import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split

import tensorflow as tf
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
# print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.

iris = pd.read_csv('./Iris2.csv', index_col = 0)

iris["Species"] = iris["Species"].map({"Iris-setosa":0,"Iris-virginica":1,"Iris-versicolor":2})
iris.iloc[:,1:4] = iris.iloc[:,1:4].astype(np.float32)
X_train, X_test, y_train, y_test = train_test_split(iris.iloc[:,1:5], iris["Species"], test_size=0.33, random_state=42)
columns = iris.columns[1:5]
feature_columns = [tf.contrib.layers.real_valued_column(k) for k in columns]

def input_fn(df,labels):
    feature_cols = {k:tf.constant(df[k].values,shape = [df[k].size,1]) for k in columns}
    label = tf.constant(labels.values, shape = [labels.size,1])
    return feature_cols,label

classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,hidden_units=[10,20,10],n_classes = 3)
cross=classifier.fit(input_fn=lambda: input_fn(X_train,y_train),steps = 1000)

ev = classifier.evaluate(input_fn=lambda: input_fn(X_test,y_test),steps=1)
print(ev)
print(cross)