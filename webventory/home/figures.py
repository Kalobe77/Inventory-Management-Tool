import random
import sys
import matplotlib.pyplot as plt
import os
def graph(x, y, username):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel="Date")
    fig.autofmt_xdate()
    user_path = os.path.join(os.path.dirname(__file__),"static","home", "temp", f'{username}')
    if not os.path.exists(user_path):
        os.mkdir(user_path)
    os.chdir(user_path)
    filename = f'graph_{random.randint(0,sys.maxsize)}.png'
    fig.savefig(filename, format="png")
    return filename