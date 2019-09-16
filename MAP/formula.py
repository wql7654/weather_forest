import pandas as pd
from statsmodels.formula.api import ols,glm
import operator
from itertools import combinations
from datetime import datetime
import time

start = datetime.fromtimestamp(time.time())
print("7.2.7 예측하기")

wine = pd.read_csv('sanbul4.csv',encoding='cp949', sep=',',header=0)
wine.columns = wine.columns.str.replace(' ','_')

wine.loc[wine['피해면적_합계'] < 0.5, '피해면적'] =1
wine.loc[wine['피해면적_합계'] >= 0.5, '피해면적'] =2
wine.loc[wine['피해면적_합계'] >= 1, '피해면적'] =3
wine.loc[wine['피해면적_합계'] >= 2, '피해면적'] =4

# wine.loc[wine['피해면적_합계'] < 0.5, '피해면적'] =1
# wine.loc[wine['피해면적_합계'] >= 0.5, '피해면적'] =2
# wine.loc[wine['피해면적_합계'] >= 1, '피해면적'] =3
# wine.loc[wine['피해면적_합계'] >= 2, '피해면적'] =4
# wine.loc[wine['피해면적_합계'] >= 3, '피해면적'] =5
# wine.loc[wine['피해면적_합계'] >= 5, '피해면적'] =6
# wine.loc[wine['피해면적_합계'] >= 7, '피해면적'] =7
# wine.loc[wine['피해면적_합계'] >= 13, '피해면적'] =8
# wine.loc[wine['피해면적_합계'] >= 50, '피해면적'] =9
# wine.loc[wine['피해면적_합계'] >= 200, '피해면적'] =10

wine.loc[wine['발생원인_구분'] == '건', '발생원인'] =1
wine.loc[wine['발생원인_구분'] == '기', '발생원인'] =2
wine.loc[wine['발생원인_구분'] == '논', '발생원인'] =3
wine.loc[wine['발생원인_구분'] == '담', '발생원인'] =4
wine.loc[wine['발생원인_구분'] == '성', '발생원인'] =5
wine.loc[wine['발생원인_구분'] == '쓰', '발생원인'] =6
wine.loc[wine['발생원인_구분'] == '어', '발생원인'] =7
wine.loc[wine['발생원인_구분'] == '입', '발생원인'] =8

colums_list=['발생일시_년','발생일시_월','발생원인','발생일시_일','습도','풍향','풍속','기온']


match_dic={}
# colums_list = ['alcohol','chlorides','citric_acid','density','fixed_acidity','free_sulfur_dioxide','pH',
#                'residual_sugar','sulphates','total_sulfur_dioxide','volatile_acidity']
wine=wine.dropna(how='any')
for num in range(1,12):
    combi_list = list(combinations(colums_list,num))
    for tup in combi_list:
        my_formula = '피해면적 ~ '
        for data in tup:
            my_formula+='%s + '%data
        my_formula = my_formula.strip().rstrip('+')
        lm = ols(my_formula, data=wine).fit()
        dependent_variable = wine['피해면적']
        independent_variables = wine[list(tup)] # formula 에 들어간 columns만 골라서 고정 변수로 줌
        y_predicted = lm.predict(independent_variables)
        y_predicted_rounded = [round(score) for score in y_predicted]
        match_count=0
        for index in range(len(y_predicted_rounded)):
            if y_predicted_rounded[index] == dependent_variable.values[index]:
                match_count+=1
        print('\n>> '+my_formula.replace('피해면적 ~ ',''))
        print('>> match count=',match_count)
        print('>> 정답률: %.2f %%'%(match_count/len(y_predicted_rounded)*100))
        match_dic['%s'%my_formula.replace('피해면적 ~ ','')] = '%.2f %%'%(match_count/len(y_predicted_rounded)*100)


# 최대값 찾기
match_dic = sorted(match_dic.items(), key=operator.itemgetter(1),reverse=True)
# print(match_dic)
print('\n \n총 조합 갯수: %d'%len(match_dic))
print("MAX 조합:",match_dic[0])