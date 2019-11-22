# Fixed Parameters
DATA_FOLDER = "C:"
CORRECT_ANSWER = "C"

# Load packages
import csv
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

# Load data
# try:
dataFolder = Path().absolute().joinpath('data')
print(">> data folder at " + str(dataFolder))

# Get num file
numFile = len([i for i in dataFolder.glob('*')])

# Go through csv files and populate data
SubjectList = np.array([],dtype='<U3')
DataList = np.ndarray((0,100,8),dtype='int')
try:
    for dataFile in dataFolder.iterdir():
        with open(str(dataFile)) as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader, None) # skip the header
            data = np.ndarray((0,8),dtype='int')
            # Read the csv file
            for row in csvreader:
                # reformat row
                row = row[1:9]
                row[1] = ord(row[1])
                newrow = np.array(row,dtype='int')
                data = np.vstack((data,newrow))
            # Save data
            data = np.reshape(data,(1,100,8))
            SubjectList = np.append(SubjectList,dataFile.stem)
            DatList = np.concatenate((DataList,data),axis=0)
except:
    print("###ERROR : File loading error###")

# Load data file and store it into one big array



# Analysis 1
## Total Outcome


