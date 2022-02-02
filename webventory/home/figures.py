import random
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter
from typing import List, Union
from datetime import date
import os


def graph(x: List[date], y: List[Union[float, int]], username: str, is_price_graph: bool) -> str:
    """
    graph returns insights graphs for inventory management software

    Args:
        x (list): x-axis (ususally date)
        y (list): y-axis (price,quantity)
        username (str): username of user trying to access insights.
        is_price_graph (bool): true if graph being passed is price graph

    Returns:
        str: filename
    """
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel="Date")
    if is_price_graph:
        ax.yaxis.set_major_formatter(StrMethodFormatter('${x:.2f}'))
        ax.set(ylabel="Price")
    else:
        ax.set(ylabel="Quantity")
    fig.autofmt_xdate()
    user_path = os.path.join(os.path.dirname(
        __file__), "static", "home", "temp", f'{username}')
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    os.chdir(user_path)
    filename: str = f'graph_{random.randint(0,sys.maxsize)}.png'
    fig.savefig(filename, format="png")
    return filename
