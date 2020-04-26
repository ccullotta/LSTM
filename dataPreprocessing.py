import math
from tools.bin import*

def normalizeBtc(num, big, small):
    num = (num - small)/(big-small)
    # num = num/big
    # 1/(1+math.exp(-num))
    return num
def normalizeVol(num, big, small):
    num = num/big
    1/(1+math.exp(-num))
    return num



baseData = openBin("btcClosingData2")

data = [
    [
        [
            normalizeBtc(baseData[j][i], float(max(baseData[j][:])), float(min(baseData[j][:]))),
            # normalizeBtc(baseData[1][i+j], float(max(baseData[1][j:j+30])), float(min(baseData[1][j:j+30])))
            ] for i in range(60)
        ] for j in range(len(baseData)) 

        ]

print(data[0])
targei = []
for i in range(len(data)-1):
    if data[i][59] < data[i+1][0]:
        targei.append(1) 
    else:
        targei.append(0)

data = data[:(len(data) - 1)]
writeToBin(data, 'btcClosingData3')
writeToBin(targei, "btcTraining")

print(targei)