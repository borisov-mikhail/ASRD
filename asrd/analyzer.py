from typing import List

from asrd import db
from asrd.database import MeasuringSet, Sample, SamplePoint
from asrd.models import FullIsoterm, Bet, DeBoer, HarkinsJura, \
    TechnicalCarbon, Hasley, BrookhoffDeBoer


class Analyzer:
    def parse(self, file) -> str:
        current_set = MeasuringSet(
            filename=file.filename,
        )
        db.session.add(current_set)
        db.session.commit()
        value = file.read().decode('windows-1251').strip()

        for line in value.split('\n'):
            columns = line.split(',')

            if columns[0] == 'SAMPLE':
                current_sample = Sample(
                    measuring_set_id=current_set.id,
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
                    sample_id=current_sample.id,
                    finish_time=columns[2],
                    start_time=columns[1],
                    p_p0=float(columns[4]),
                    peak_start=int(columns[6]),
                    peak_finish=int(columns[7]),
                    pick_max=int(columns[8]),
                    pick_amplitude=float(columns[11]),
                    S_of_pick=float(columns[12]),
                    grad_koeff=float(columns[13]),
                    adsorb_or_desorb=int(columns[21]),
                    volume=float(columns[12]) * float(columns[13]) / float(
                        current_sample.mass),
                )
                db.session.add(current_point)
                db.session.commit()

            else:
                raise Exception(f'{columns[0]} not found')

        return str(current_set.id)

    def get_samples(self, set_id: int) -> List[Sample]:
        return MeasuringSet.query.get(set_id).samples

    def get_options_for_graphs(self, sample_id: int):
        sample = Sample.query.get(sample_id)

        models = [
            FullIsoterm(sample, x_axis_name='P/P₀', y_axis_name='V, мл/г'),
            Bet(sample, x_axis_name='h=P/P₀', y_axis_name='f=h/V(1-h)*10⁻³, г/мл'),
            DeBoer(sample, x_axis_name='t, нм', y_axis_name='V, мл/г'),
            Hasley(sample, x_axis_name='t, нм', y_axis_name='V, мл/г'),
            HarkinsJura(sample, x_axis_name='t, нм', y_axis_name='V, мл/г'),
            TechnicalCarbon(sample, x_axis_name='t, нм', y_axis_name='V, мл/г'),
            BrookhoffDeBoer(sample, x_axis_name='t, нм', y_axis_name='V, мл/г'),
        ]

        for model in models:
            model.calculate_params()

        return [model.render() for model in models]
