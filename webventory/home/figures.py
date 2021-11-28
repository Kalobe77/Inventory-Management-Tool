import random
import sys
import matplotlib.pyplot as plt
import os
def graph(x, y):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel="Date")
    fig.autofmt_xdate()
    path = os.path.join(os.path.dirname(__file__),"static","home", "temp")
    os.chdir(path)

    filename = f'graph{random.randint(0,sys.maxsize)}.png'
    fig.savefig(filename, format="png")
    return filename