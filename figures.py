import matplotlib.pyplot as plt


def graph(x, y):
    fig, ax = plt.subplots()
    ax.plot([x], [y])
    return fig
