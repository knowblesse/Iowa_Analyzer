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
from loadData import loadData
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.family"] = 'Malgun Gothic'

#
SubjectList, DataList = loadData()
numFile = len(SubjectList)

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
ax2.set_xticklabels(SubjectList[np.argsort(OUTPUT[:,3])],rotation=90)
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