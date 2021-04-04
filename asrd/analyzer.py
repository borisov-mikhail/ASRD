import os

import asrd.config as conf
from asrd import db
from asrd.database import Sample, SamplePoint
from asrd.models import FullIsoterm, Bet, DeBoer, GarkinsYura, \
    TechnicalCarbon, Hasley


class Analyzer:
    def parse(self, guid):
        path = os.path.join(conf.UPLOAD_PATH, guid)
        with open(path, 'r', encoding='windows-1251') as file:
            content = file.read().strip()

        for line in content.split('\n'):
            columns = line.split(',')

            if columns[0] == 'SAMPLE':
                current_sample = Sample(
                    filename=guid,
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

                )
                db.session.add(current_sample)
                db.session.commit()

            elif columns[0] == 'POINT':
                current_point = SamplePoint(
                    sample_id=int(
                        db.session.query(Sample).order_by(Sample.id)[-1].id),
                    start_time=columns[1],
                    finish_time=columns[2],
                    p_p0=float(columns[4]),
                    peak_start=int(columns[6]),
                    peak_finish=int(columns[7]),
                    pick_max=int(columns[8]),
                    pick_amplitude=float(columns[11]),
                    S_of_pick=float(columns[12]),
                    grad_koeff=float(columns[13]),
                    adsorb_or_desorb=int(columns[21])
                )
                db.session.add(current_point)
                db.session.commit()

            else:
                raise Exception(f'{columns[0]} not found')

    def get_samples_names(self, guid):
        return [sample.sample_name for sample in
                Sample.query.filter_by(filename=guid).all()]

    def get_options_for_graphs(self, index):
        sample: Sample = self.samples[int(index)]

        models = [
            FullIsoterm(sample, title='Изотерма Адсорбции', x_axis_name='P/P₀',
                        y_axis_name='V, мл/г'),
            Bet(sample, title='БЭТ', x_axis_name='h=P/P₀',
                y_axis_name='f=h/V(1-h), г/мл'),
            DeBoer(sample, title='Модель Де-Бура', x_axis_name='t, нм',
                   y_axis_name='V, мл/г'),
            Hasley(sample, title='Модель Хэсли', x_axis_name='t, нм',
                   y_axis_name='V, мл/г'),
            GarkinsYura(sample, title='Модель Гаркинс-Юра',
                        x_axis_name='t, нм', y_axis_name='V, мл/г'),
            TechnicalCarbon(sample, title='Модель технического углерода',
                            x_axis_name='t, нм', y_axis_name='V, мл/г'),
        ]

        for model in models:
            model.calculate_params()

        return [model.render() for model in models]
