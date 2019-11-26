import numpy as np
from pathlib import Path
import csv

def loadData(DATA_FOLDER = Path("C:/VCF/Iowa_Analyzer/data")):
    """
    Load data from the .csv Data folder
    :param DATA_FOLDER: pathlib.Path(absolute path)
    :return: (SubjectList, DataList)
    """
    print(">> data folder at " + str(DATA_FOLDER))

    # Get num file
    numFile = len([i for i in DATA_FOLDER.glob('*')])

    # Go through csv files and populate data
    """
    SubjectList : name of the csv file
    DataList : subject x trial x indices
    indices : 
        +-------+------+--------+---------+------+-------+----+
        |   0   |  1   |   2    |    3    |  4   |   5   | 6  |
        +-------+------+--------+---------+------+-------+----+
        | Trial | deck | reward | penalty | gain | total | rt |
        +-------+------+--------+---------+------+-------+----+
    """
    SubjectList = np.array([],dtype='<U3')
    DataList = np.ndarray((0,100,7),dtype='int')
    try:
        for dataFile in DATA_FOLDER.iterdir():
            with open(dataFile, 'r', encoding = 'utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader, None) # skip the header
                data = np.ndarray((0,7),dtype='int')
                # Read the csv file
                for row in csvreader:
                    # reformat row
                    row = row[1:8]
                    row[1] = ord(row[1])
                    newrow = np.array(row,dtype='int')
                    data = np.vstack((data,newrow))
                # Save data
                data = np.reshape(data,(1,100,7))
                SubjectList = np.append(SubjectList,dataFile.stem)
                DataList = np.concatenate((DataList,data),axis=0)
    except:
        print("ERROR : File loading error")
    return (SubjectList,DataList)