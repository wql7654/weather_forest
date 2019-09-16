import numpy as np
import pandas as pd
import turtle


df = pd.read_csv('./sanbul3.csv',encoding='cp949')
df.columns = df.columns.str.replace(' ','')
df2 = pd.read_csv('./종단기상관측소.csv',encoding='cp949')
# df2 = pd.read_csv('./종단기상관측소.csv',encoding='cp949')
df2.columns = df2.columns.str.replace(' ','')

bc = open("./새파일6.txt", 'a',encoding="utf-8")

# print(df['X-좌표']) # 290
print(df2['위도'][0]) # 4631

alldistance=[]
for i in range(0,4634):
    jijum={}
    for b in range(0,len(df2['위도'])):
        x1 = df['Y-좌표'][i]
        y1 = df['X-좌표'][i]
        x2 = df2['위도'][b]
        y2 = df2['경도'][b]
        z1 = df['발생일시_년'][i]
        z2 = df2['시작일'][b][0:4]

        if int(z1)<int(z2):
            pass
        else:
            distance = ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)) ** 0.5
            jijum[distance] = df2['지점'][b]
    bs=sorted(jijum.items(),key=lambda item:item[0],reverse=False)
    bc.write(str(bs[0][1])+'\n')

    # alldistance.append(b[0])
    print(i)
    # print(b[4630])


# print(df['발생장소_관서'][0])
print(alldistance)
x1,y1=df['X-좌표'][0],df['Y-좌표'][0]

x2,y2=df2['위도'][0],df2['경도'][0]
distance=((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))**0.5

print("두좌표거리",x1,y1,x2,y2)
bc.close()
# turtle.penup()
# turtle.goto(x1,y1)
# turtle.write("point")
# turtle.pendown()
#
# turtle.goto(x2,y2)
# turtle.write_docstringdict("point")
#