import csv
def writeToCSV(input, fileName):
    with open(fileName,'w',newline='') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        wr.writerows(input)
        return

def readCSVFile(fileName):
    stocks = []
    with open(fileName, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            stocks.append(row)
    return stocks  