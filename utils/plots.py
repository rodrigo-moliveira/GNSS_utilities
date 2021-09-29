import matplotlib.pyplot as plt

i = 1


def new_plot(x, y, title="", new_figure=True, label=""):
    global i

    if new_figure:
        i += 1
    fig = plt.figure(i)

    plt.title(title)

    if len(label) > 0:
        plt.plot(x, y, label=label)
        plt.legend()
    else:
        plt.plot(x, y)


def new_plot_series(data, title=""):
    global i

    fig = plt.figure(i)
    i += 1

    plt.title(title)
    plt.plot(data)


def show():
    plt.show()


