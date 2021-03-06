import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(color_codes=True)


def read_data(path):
    cols = [
        "Target", "start time", "finish_time", "P/P0", "P/P0_1", "?",
        "peak_start", "peak_finish", "pick_max", "??", "0", "pick_amplitude",
        "S_of_pick", "grad_koeff", "idk", "idk1", "idk2", "№_1", "1", "1_1",
        "NaN", "0_1"
    ]

    path = path.replace('/', '//')
    submissions_data = pd.read_csv(path, encoding='windows-1251', header=None)
    submissions_data.columns = cols

    indexes_of_expirements = np.where(submissions_data['Target'] == "SAMPLE")
    # a = submissions_data.index[-1] + 1
    # indexes = np.hstack((indexes_of_expirements[0], a))

    samples = submissions_data.loc[indexes_of_expirements]
    samples.columns = ["type", "create_time", "sample_name", "operator", "?",
                       "??", "mass", "vlazhnost'", "atmosphere_pressure",
                       "atmosphere_pressure_1", "graduation_name", "0",
                       "graduation_time", "??????", "summarnyy_raskhod", "idk",
                       "idk1", "T, K", "273.16K", "1_1", "density", "L/D"]
    # samples.index = [x for x in range(len(samples))]
    return np.array(samples.sample_name)


def plot_graph(index_of_sample, x, y):
    pass
    # current_index = indexes[index_of_sample] + 1:indexes[index_of_sample + 1]
    # data = submissions_data[current_index]
    # sns.set_style("ticks", {'xtick.color': '.0', 'ytick.color': '.0'})
    # g = sns.lmplot(
    #   x=x,
    #   y=y,
    #   data=data,
    #   hue='0_1',
    #   height=3,
    #   aspect=4,
    #   legend=0,
    #   fit_reg=False,
    #   scatter_kws={"s": 50}
    # )
    # plt.title(
    #   "Изотерма адсорбции",
    #   fontsize=18,
    #   bbox=dict(edgecolor='black', color='w'),
    #   horizontalalignment='center'
    # )
    # plt.ylabel(
    #   '$V, mm^{3}$',
    #   rotation=0,
    #   fontsize=14,
    #   verticalalignment='top',
    #   horizontalalignment='right'
    # )
    # plt.xlabel('$p/p_{0}$', fontsize=16)
    # plt.xticks(np.arange(0, 1.1, step=0.1), fontsize=13)
    # plt.yticks(fontsize=13)
    # plt.grid(
    #   True,
    #   which=u'major',
    #   color='black',
    #   linewidth=1.,
    #   linestyle='-'
    # )
    # path = os.getcwd() + "\\data\\" + x + y + ".jpg"
    # g.savefig(path)
    # return path
