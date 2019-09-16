
f = open("./one", 'r',encoding="utf-8")
fc = open("./two", 'r',encoding="utf-8")
bc = open("./새파일.txt", 'a',encoding="utf-8")
i=0
cd=0
linec=''
while True:
    line = f.readline()
    if not line:
        break
    text1 = int(len(line)) - 1
    # print(line[0:text1])
    b = 0
    c=0
    dc=0
    fc = open("./two", 'r', encoding="utf-8")
    while c<=21686:
        c+=1
        line2 = fc.readline()
        if line == '':
            dc+=1
            break

        if line2[0:-2]==line[0:-1] and len(line2[0:-2])==len(line[0:-1]):
            i += 1
            linec = line2[0:-1]
            break

    bc.write(linec+'\n')
    cd+=1
    print(linec)
    print(cd)
    fc.close()
print(i)
print('dc %d',dc)
bc.close()
f.close()
fc.close()


