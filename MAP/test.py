import urllib
import json
import requests
import urllib.request
import pandas as pd
import time
import datetime
from time import localtime, strftime
import numpy as np
import statsmodels.api as sm





df = pd.read_csv('./종단기상관측소.csv',encoding='cp949')
df.columns = df.columns.str.replace(' ','')

def get_Weather_xml():
    loca=""
    url="https://data.kma.go.kr/OPEN_API/AWSM/2016/09/XML/awsmdays_96.xml"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    data=response.read()
    print(data)

# get_Weather_xml()

def get_test():
    df2 = pd.read_csv('./sanbul2.csv', encoding='cp949')
    df2.columns = df2.columns.str.replace(' ', '')
    print(df2.columns)

# get_test()

def time_test():
    c=datetime.date(2018,11,22)
    bc=time.localtime()
    d=df['시작일'][1]

    dt1 = datetime.datetime(2018,11,22, 0)
    dt2 = datetime.datetime(2019,2,23, 0)
    date.today()



    print(c)
    print(d)
    print(bc)
    print(dt1-dt2)

# time_test()

def t_test():
    # Read the data set into a pandas DataFrame
    churn = pd.read_csv('hong2.csv', sep=',', header=0,encoding='cp949')

    churn.columns = [heading.lower() for heading in \
                     churn.columns.str.replace(' ', '_').str.replace("\'", "").str.strip('?')]

    # churn.loc[churn['피해면적_합계'] < 0.5, '피해면적'] = 1
    # churn.loc[churn['피해면적_합계'] >= 0.5, '피해면적'] = 2
    # churn.loc[churn['피해면적_합계'] >= 1, '피해면적'] = 3
    # churn.loc[churn['피해면적_합계'] >= 2, '피해면적'] = 4
    # churn.loc[churn['피해면적_합계'] >= 3, '피해면적'] = 5
    # churn.loc[churn['피해면적_합계'] >= 5, '피해면적'] = 6
    # churn.loc[churn['피해면적_합계'] >= 7, '피해면적'] = 7
    # churn.loc[churn['피해면적_합계'] >= 13, '피해면적'] = 8
    # churn.loc[churn['피해면적_합계'] >= 50, '피해면적'] = 9
    # churn.loc[churn['피해면적_합계'] >= 200, '피해면적'] = 10
    # churn['churn01'] = np.where(churn['churn'] == 'True.', 1., 0.)
    # churn['total_charges'] = churn['day_charge'] + churn['eve_charge'] + \
    #                          churn['night_charge'] + churn['intl_charge']

    dependent_variable = churn['산불']
    independent_variables = churn[['기온','습도','풍속','풍향']]
    independent_variables_with_constant = sm.add_constant(independent_variables, prepend=True)
    logit_model = sm.Logit(dependent_variable, independent_variables_with_constant).fit()

    print(logit_model.summary())  # error 발생
    # print("\nQuantities you can extract from the result:\n%s" % dir(logit_model))
    print("\nCoefficients:\n%s" % logit_model.params)
    print("\nCoefficient Std Errors:\n%s" % logit_model.bse)


t_test()

def test2():

    # Read the data set into a pandas DataFrame
    churn = pd.read_csv('churn.csv', sep=',', header=0)

    churn.columns = [heading.lower() for heading in \
                     churn.columns.str.replace(' ', '_').str.replace("\'", "").str.strip('?')]

    churn['churn01'] = np.where(churn['churn'] == 'True.', 1., 0.)
    churn['total_charges'] = churn['day_charge'] + churn['eve_charge'] + \
                             churn['night_charge'] + churn['intl_charge']

    dependent_variable = churn['churn01']
    independent_variables = churn[['account_length', 'custserv_calls', 'total_charges']]
    independent_variables_with_constant = sm.add_constant(independent_variables, prepend=True)
    logit_model = sm.Logit(dependent_variable, independent_variables_with_constant).fit()

    print(logit_model.summary())  # error 발생
    # print("\nQuantities you can extract from the result:\n%s" % dir(logit_model))
    print("\nCoefficients:\n%s" % logit_model.params)
    print("\nCoefficient Std Errors:\n%s" % logit_model.bse)

# test2()