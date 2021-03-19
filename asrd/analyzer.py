from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


sns.set_theme(color_codes=True)


@dataclass
class SamplePoint:
    start_time: str
    finish_time: str
    p_p0: float  # P / P0
    p_p1: float  # P / P0_1
    peak_start: int
    peak_finish: int
    pick_max: int
    pick_amplitude: float
    S_of_pick: float
    grad_koeff: float
    adsorb_or_desorb: int
    volume: float = None


@dataclass
class Sample:
    create_time: str
    sample_name: str
    operator: str
    mass: float
    vlazhnost: float
    atmosphere_pressure: float
    atmosphere_pressure_1: float
    graduation_name: int
    graduation_time: str
    summarnyy_raskhod: float
    idk: float
    idk1: float
    temperature: float  # "T, K"
    density: float
    l_to_d: float  # "L/D"

    points: List[SamplePoint]


class Analyzer:
    samples: List[Sample]

    def parse(self, app, path):
        with open(path, 'r', encoding='windows-1251') as file:
            content = file.read().strip()
        app.config['GRAPH_FOLDER'] = os.path.splitext(os.path.basename(path))[0]

        self.samples = []

        for line in content.split('\n'):
            columns = line.split(',')

            if columns[0] == 'SAMPLE':
                current_sample = Sample(
                    create_time=columns[1],
                    sample_name=columns[2],
                    operator=columns[3],
                    mass=float(columns[6]),
                    vlazhnost=float(columns[7]),
                    atmosphere_pressure=float(columns[8]),
                    atmosphere_pressure_1=float(columns[9]),
                    graduation_name=int(columns[11]),
                    graduation_time=columns[12],
                    summarnyy_raskhod=float(columns[14]),
                    idk=float(columns[15]),
                    idk1=float(columns[16]),
                    temperature=float(columns[17]),
                    density=float(columns[20]),
                    l_to_d=float(columns[21]),
                    points=[]
                )

                self.samples.append(current_sample)

            elif columns[0] == 'POINT':
                current_point = SamplePoint(
                    start_time=columns[1],
                    finish_time=columns[2],
                    p_p0=float(columns[3]),
                    p_p1=float(columns[4]),
                    peak_start=int(columns[6]),
                    peak_finish=int(columns[7]),
                    pick_max=int(columns[8]),
                    pick_amplitude=float(columns[11]),
                    S_of_pick=float(columns[12]),
                    grad_koeff=float(columns[13]),
                    adsorb_or_desorb=int(columns[21])
                )

                self.samples[-1].points.append(current_point)
            else:
                raise Exception(f'{columns[0]} not found')

    def get_samples_names(self):
        return [sample.sample_name for sample in self.samples]

    def models_calculation(self, sample_index):
        sample = self.samples[sample_index]
        for point in sample.points:
            volume = float(point.S_of_pick) * float(point.grad_koeff) / \
                     float(sample.mass)
            point.volume = volume
            #print(point.S_of_pick)

    def plot_graph(self, app, index):
        sample = self.samples[index]
        x = [point.p_p1 for point in sample.points]
        y = [point.volume for point in sample.points]
        hue = [point.adsorb_or_desorb for point in sample.points]
        data = {'P/P0_1': x,
                'V': y,
                'adsorb_or_desorb': hue}
        graph_points = pd.DataFrame(data)
        print(graph_points)
        sns.set_style("ticks", {'xtick.color': '.0', 'ytick.color': '.0'})
        g = sns.lmplot(
                       x='P/P0_1',
                       y='V',
                       data=graph_points,
                       hue='adsorb_or_desorb',
                       height=3,
                       aspect=4,
                       legend=0,
                       fit_reg=False,
                       scatter_kws={"s": 50}
                       )
        plt.title("Изотерма адсорбции", fontsize=18,
                  bbox=dict(edgecolor='black'),
                  horizontalalignment='center')
        plt.ylabel('$V, mm^{3}$', rotation=0, fontsize=14,
                   verticalalignment='top', horizontalalignment='right')
        plt.xlabel('$p/p_{0}$', fontsize=16)
        plt.xticks(np.arange(0, 1.1, step=0.1), fontsize=13)
        plt.yticks(fontsize=13)
        plt.grid(True, which=u'major', color='black', linewidth=1.,
                 linestyle='-')
        if not os.path.isdir(app.config['GRAPH_FOLDER']):
            os.mkdir(app.config['GRAPH_FOLDER'])
        path = os.path.join(app.config['UPLOAD_FOLDER'],
                            app.config['GRAPH_FOLDER'] + '/' + str(index)
                            + '.jpg')
        g.savefig(path)
        return app.config['GRAPH_FOLDER'] + '/' + str(index) + '.jpg'
