import numpy as np
import pandas as pd
import statsmodels.api as sm


churn = pd.read_csv('sanbul4.csv',encoding='cp949', sep=',',header=0)
churn.columns = churn.columns.str.replace(' ','_')

churn.loc[churn['피해면적_합계'] < 0.5, '피해면적'] =1
churn.loc[churn['피해면적_합계'] >= 0.5, '피해면적'] =2
churn.loc[churn['피해면적_합계'] >= 1, '피해면적'] =3
churn.loc[churn['피해면적_합계'] >= 2, '피해면적'] =4
churn.loc[churn['피해면적_합계'] >= 3, '피해면적'] =5
churn.loc[churn['피해면적_합계'] >= 5, '피해면적'] =6
churn.loc[churn['피해면적_합계'] >= 7, '피해면적'] =7
churn.loc[churn['피해면적_합계'] >= 13, '피해면적'] =8
churn.loc[churn['피해면적_합계'] >= 50, '피해면적'] =9
churn.loc[churn['피해면적_합계'] >= 200, '피해면적'] =10

churn.loc[churn['발생원인_구분'] == '건', '발생원인'] =1
churn.loc[churn['발생원인_구분'] == '기', '발생원인'] =2
churn.loc[churn['발생원인_구분'] == '논', '발생원인'] =3
churn.loc[churn['발생원인_구분'] == '담', '발생원인'] =4
churn.loc[churn['발생원인_구분'] == '성', '발생원인'] =5
churn.loc[churn['발생원인_구분'] == '쓰', '발생원인'] =6
churn.loc[churn['발생원인_구분'] == '어', '발생원인'] =7
churn.loc[churn['발생원인_구분'] == '입', '발생원인'] =8
# churn=churn.dropna(how='any')
churn = churn[pd.notnull(churn['발생일시_년'])]
churn = churn[pd.notnull(churn['발생일시_월'])]
churn = churn[pd.notnull(churn['발생원인'])]
churn = churn[pd.notnull(churn['발생일시_일'])]
churn = churn[pd.notnull(churn['습도'])]
churn = churn[pd.notnull(churn['풍향'])]
churn = churn[pd.notnull(churn['풍속'])]
churn = churn[pd.notnull(churn['기온'])]
churn = churn[pd.notnull(churn['피해면적'])]


colums_list=['발생일시_년','발생일시_월','발생원인','발생일시_일','습도','풍향','풍속','기온']




# churn = pd.read_csv('churn.csv', sep = ',', header = 0)
# churn.columns = [heading.lower() for heading in \
                 # churn.columns.str.replace(' ', '_').str.replace("\'", "").str.strip('?')]

# churn['churn01'] = np.where(churn['churn'] == 'True.', 1., 0.)
# churn['total_charges'] = churn['day_charge'] + churn['eve_charge'] + \
#                          churn['night_charge'] + churn['intl_charge']

dependent_variable = churn['피해면적']
independent_variables = churn[colums_list]
independent_constant = sm.add_constant(independent_variables.to_numpy(), prepend=True)
logit_model = sm.Logit(dependent_variable, independent_constant).fit()
# X = sm.add_constant(weekly[predictors].values)

new_observations=churn.loc[churn.index.isin(range(len(churn))), independent_variables.columns]
new_observations_constant=sm.add_constant(new_observations,prepend=True)
y_predicted = logit_model.predict(new_observations_constant)
y_predicted_rounded=[round(score,0) for score in y_predicted]
logistic_predicted_value_list=[]
false_on=0
all_on=0
for predict_value in y_predicted_rounded:
    if predict_value == 0.0:
        logistic_predicted_value_list.append(False)

    else:
        logistic_predicted_value_list.append(True)
for i in logistic_predicted_value_list:
    i=str(i) + '.'
    if i== churn['churn'][all_on]:
        false_on += 1
    all_on += 1

print("정답률 %.2f%%"%((false_on/all_on)*100))