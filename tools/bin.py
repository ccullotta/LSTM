import pickle
def writeToBin(data, fileName):
    with open(fileName, 'wb') as f:
        pickle.dump(data, f)

def openBin(fileName):
    with open(fileName, 'rb') as Y:
        return pickle.load(Y)

def saveModel(data, fileName):
    with open(fileName, 'w') as j:
        j.write(data)