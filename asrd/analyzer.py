from dataclasses import dataclass
from typing import List

from asrd.models import FullIsoterm, Bet, DeBoer, GarkinsYura, \
    TechnicalCarbon, Hasley


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

    def get_volume(self, sample):
        return round(float(self.S_of_pick) * float(self.grad_koeff) / float(
            sample.mass), 4)


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

    def parse(self, path):
        with open(path, 'r', encoding='windows-1251') as file:
            content = file.read().strip()

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

    def get_options_for_graphs(self, index):
        sample: Sample = self.samples[int(index)]

        models = [
            FullIsoterm(sample, title='Изотерма Адсорбции', x_axis_name='P/P₀', y_axis_name='V, мл'),
            Bet(sample, title='БЭТ', x_axis_name='h=P/P₀', y_axis_name='f=h/V(1-h), г/мл'),
            DeBoer(sample, title='Модель Де-Бура', x_axis_name='t, нм', y_axis_name='f=h/V(1-h), г/мл'),
            Hasley(sample, title='Модель Хэсли', x_axis_name='t, нм', y_axis_name='f=h/V(1-h), г/мл'),
            GarkinsYura(sample, title='Модель Гаркинс-Юра', x_axis_name='t, нм', y_axis_name='f=h/V(1-h), г/мл'),
            TechnicalCarbon(sample, title='Модель технического углерода', x_axis_name='t, нм', y_axis_name='f=h/V(1-h), г/мл'),
        ]

        for model in models:
            model.calculate_params()

        return [model.render() for model in models]
