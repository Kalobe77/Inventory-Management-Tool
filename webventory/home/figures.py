import random
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter,StrMethodFormatter
import os
def graph(x:list, y:list, username:str, is_price_graph):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel="Date")
    if is_price_graph:
        ax.yaxis.set_major_formatter(StrMethodFormatter('${x:.2f}'))
        ax.set(ylabel="Price")
    else:
        ax.set(ylabel="Quantity")
    fig.autofmt_xdate()
    user_path = os.path.join(os.path.dirname(__file__),"static","home", "temp", f'{username}')
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    os.chdir(user_path)
    filename = f'graph_{random.randint(0,sys.maxsize)}.png'
    fig.savefig(filename, format="png")
    return filename