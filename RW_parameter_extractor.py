# Load packages
import csv
import numpy as np
from loadData import loadData
from multiprocessing import Pool
from matplotlib import pyplot as plt
import matplotlib
matplotlib.rcParams["font.family"] = 'Malgun Gothic'

def RW_param_evaluator(alpha, it, choice, result):
    """
    Calculate log likelihood for the given alpha and inverse temperature value
    :param alpha: alpha. learning rate
    :param it: inverse temperature
    :param choice: 1D vector (0:A, 1:B, 2:C, 3:D)
    :param result: 1D int vector for outcome value
    :return: tuple(alpha, it)
    """
    # for the computational efficiency, make result to a small number
    result = result / 100

    #Initialize
    loglikelihood = 0
    isVisited = np.array([False, False, False, False])
    Q = np.array([0,0,0,0])

    #Run through trials
    for trial in range(len(choice)):
        eQ = np.exp(Q * it)
        prob = eQ / np.sum(eQ)
        selectedOption = choice[trial]

        #Evaluation
        loglikelihood = loglikelihood + np.log(prob[selectedOption])

        #Recalculate Q value
        if trial == 0: # propagate Q value to all options
            Q = np.repeat(result[trial],4)
            isVisited[selectedOption] = True
        else:
            if (isVisited[selectedOption]):
                Q[selectedOption] += alpha * (result[trial] - Q[selectedOption])
            else:
                Q[selectedOption] = result[trial]
                isVisited[selectedOption] = True
    return loglikelihood

if __name__ == '__main__':
    #Set hyperharameter range
    x_arr = np.arange(0.01, 2, 0.01)  # alpha
    y_arr = np.arange(0.01, 2, 0.01)  # inverse temperature

    #Load Data
    SubjectList, DataList = loadData()

    #Output Array
    output_score = np.zeros((len(SubjectList),len(x_arr), len(y_arr))) # subject x X x Y
    output_param = np.zeros((len(SubjectList),4)) # subject x index alpha, index it, alpha,it

    #Run through subject
    for subject in range(DataList.shape[0]):
        result = DataList[subject, :, 4]
        choice = DataList[subject, :, 1] - ord('A')
        score = list()
        param_grid = list()
        for x in x_arr:
            # Make parameter grid to give to pool
            for y in y_arr:
                param_grid.append((x, y, choice, result))
        # multiprocessing
        with Pool() as p:
            result_list = p.starmap(RW_param_evaluator, param_grid)
            score.append(result_list)

        #save score
        score = np.asarray(score)
        output_score[subject,:,:] = score.reshape((len(x_arr), len(y_arr)))

        #Find the hyperparameter
        ind = np.unravel_index(np.argmax(np.array(score)), (199,199))
        output_param[subject, :] = np.array([ind[0], ind[1], x_arr[ind[0]],y_arr[ind[1]]])

        print("Done")
        #Print result
        print("Participants #" + str(subject) + " " + SubjectList[subject])
        print("alpha : " + str(x_arr[ind[0]]))
        print("inverse temperature : " + str(y_arr[ind[1]]))

        #Save to csv
        with open('RW_result.csv','a', newline='') as csvfile:
            cw = csv.writer(csvfile, delimiter =',')
            cw.writerow([SubjectList[subject],x_arr[ind[0]], y_arr[ind[1]]])

    #Draw plot
    fig = plt.figure()
    ax = fig.subplots(1,2)

    # main line
    ax[0].set_title('learning rate')
    ax[0].plot(np.arange(len(SubjectList)), np.sort(output_param[:,2]), 'o-')
    ax[0].set_xticks(np.arange(len(SubjectList)))
    ax[0].set_xticklabels(SubjectList[np.argsort(output_param[:,2])], rotation=90)
    ax[0].set_xlabel('Name')
    ax[0].set_ylim(0,2)
    # base line
    ax[0].plot([0, len(SubjectList)-1], [1, 1], 'r--')

    # main line
    ax[1].set_title('inverse temperature')
    ax[1].plot(np.arange(len(SubjectList)), np.sort(output_param[:,3]), 'o-')
    ax[1].set_xticks(np.arange(len(SubjectList)))
    ax[1].set_xticklabels(SubjectList[np.argsort(output_param[:,3])], rotation=90)
    ax[1].set_xlabel('Name')
    ax[1].set_ylim(0, 2)
    fig.show()
