import csv
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt

def imshow_score(output_score, output_param, subject):
    fig = plt.figure()
    ax = fig.subplots(1,1)
    ax.imshow(output_score[subject,:,:], cmap=plt.get_cmap('jet'))
    ax.scatter(output_param[subject,1], output_param[subject,0],'w')
    ax.set_xlabel('alpha')
    ax.set_ylabel('inverse temperature')

    fig.show()

def parameterGraph(DATA_PATH=Path("C:/VCF/Iowa_Analyzer/RW_result.csv")):
    """
    Load result.csv and plot the graph
    :param DATA_PATH: path of the RW_result.csv
    """
    ParamList = np.empty((0,2))
    SubjectList = np.empty((0))
    try:
        with open(DATA_PATH, 'r') as csvfile:
            cr = csv.reader(csvfile,delimiter=',')
            # Read the csv file
            for row in cr:
                # reformat row
                SubjectList = np.append(SubjectList,row[0])
                ParamList = np.vstack((ParamList,np.array(row[1:3],dtype='double')))
    except:
        print("ERROR : File loading error")

    #Draw plot
    fig = plt.figure()
    ax = fig.subplots(1,2)

    # main line
    ax[0].set_title('learning rate')
    ax[0].plot(np.arange(len(SubjectList)), np.sort(ParamList[:,0]), 'o-')
    ax[0].set_xticks(np.arange(len(SubjectList)))
    ax[0].set_xticklabels(SubjectList[np.argsort(ParamList[:,0])], rotation=90)
    ax[0].set_xlabel('Name')
    ax[0].set_ylim(0,2)
    # base line
    ax[0].plot([0, len(SubjectList)-1], [1, 1], 'r--')

    # main line
    ax[1].set_title('inverse temperature')
    ax[1].plot(np.arange(len(SubjectList)), np.sort(ParamList[:,1]), 'o-')
    ax[1].set_xticks(np.arange(len(SubjectList)))
    ax[1].set_xticklabels(SubjectList[np.argsort(ParamList[:,1])], rotation=90)
    ax[1].set_xlabel('Name')
    ax[1].set_ylim(0, 2)
    fig.show()
