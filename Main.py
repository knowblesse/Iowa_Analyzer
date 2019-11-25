"""
    ----------------------------------------------------------------
    Iowa_Analyzer main.py
    @Knowblesse 2019
    Date : 19NOV24
    ----------------------------------------------------------------
    Analysis and plotting script for
    2019 Autumn Sim Yeon presentation.
    ----------------------------------------------------------------
"""
# Load packages
import csv
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.family"] = 'Malgun Gothic'

# Fixed Parameters
DATA_FOLDER = Path("C:/VCF/Iowa_Analyzer/data")
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

# Generate single statistic variables from the data
"""
OUTPUT : 
+-------------+------------------------+
|      0      |          1-4           |
+-------------+------------------------+
| Final Score | numA, numB, numC, numD |
+-------------+------------------------+
"""
OUTPUT = np.zeros((numFile,6)) # final score | numA numB numC numD | prob 'C'
for i in np.arange(numFile):
    tempArr = DataList[i,:,:]
    OUTPUT[i,0] = tempArr[-1,5] # total score
    OUTPUT[i,1:5]  = np.array([sum(tempArr[:,1] == ord('A')),
                               sum(tempArr[:,1] == ord('B')),
                               sum(tempArr[:,1] == ord('C')),
                               sum(tempArr[:,1] == ord('D'))])
    OUTPUT[i,5] = np.mean(tempArr[:,5])

################################
#           PLOT     1         #
################################
# Total Score
fig1 = plt.figure(1)
ax1 = fig1.subplots(1,1)
ax1.set_title('Total Score')

# main line
ax1.plot(np.arange(numFile),np.sort(OUTPUT[:,0]),'o-')
ax1.set_xticks(np.arange(numFile))
ax1.set_xticklabels(SubjectList[np.argsort(OUTPUT[:,0])],rotation=90)
ax1.set_xlabel('Name')
ax1.set_ylabel('Total Score')
# base line
ax1.plot([0,numFile-1],[2000,2000],'r--')

fig1.show()

################################
#           PLOT     2         #
################################
# Choice Ratio
fig2 = plt.figure(2)
ax2 = fig2.subplots(1,1)
ax2.set_title('Best Choice Ratio')

# main line
ax2.plot(np.arange(numFile),np.sort(OUTPUT[:,3])/100,'o-')
ax2.set_xticks(np.arange(numFile))
ax2.set_xticklabels(SubjectList[np.argsort(OUTPUT[:,0])],rotation=90)
ax2.set_xlabel('Name')
ax2.set_ylabel('Ratio')
# base line
ax2.plot([0,numFile-1],[0.25,0.25],'r--')

fig2.show()

################################
#           PLOT     3         #
################################
# Choice trend change
fig3 = plt.figure(3)
ax3 = fig3.subplots(2,3)
ax3[0,0].set_title('Option : A')
ax3[0,1].set_title('Option : B')
ax3[1,0].set_title('Option : C')
ax3[1,1].set_title('Option : D')
ax3[0,2].set_title('Option : A&B')
ax3[1,2].set_title('Option : C&D')

# Populate data
ax3[0,0].plot(np.sum(np.sum(DataList[:,:,1] == ord('A'),axis=0).reshape(10,10),axis=1)/(10*numFile))
ax3[0,1].plot(np.sum(np.sum(DataList[:,:,1] == ord('B'),axis=0).reshape(10,10),axis=1)/(10*numFile))
ax3[1,0].plot(np.sum(np.sum(DataList[:,:,1] == ord('C'),axis=0).reshape(10,10),axis=1)/(10*numFile))
ax3[1,1].plot(np.sum(np.sum(DataList[:,:,1] == ord('D'),axis=0).reshape(10,10),axis=1)/(10*numFile))

ax3[0,2].plot(np.sum(np.sum(DataList[:,:,1] <= ord('B'),axis=0).reshape(10,10),axis=1)/(10*numFile))
ax3[1,2].plot(np.sum(np.sum(DataList[:,:,1] >= ord('C'),axis=0).reshape(10,10),axis=1)/(10*numFile))

for i in range(2):
    for j in range(3):
        ax3[i,j].set_xlabel('Trials(*0.1)')
        ax3[i,j].set_ylabel('Ratio')
        ax3[i,j].set_ylim(0,1)

fig3.show()