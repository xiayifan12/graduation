import matplotlib.pyplot as plt


def showGraphWithIters(error_list):
    plt.plot(error_list)
    plt.title('Error in sample')
    plt.xlabel('iters')
    plt.ylabel('error')
    plt.ylim(0, 0.5)
    plt.show()
