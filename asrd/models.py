import math
from abc import ABC, abstractmethod


class Models(ABC):
    def __init__(self, sample, title, x_axis_name, y_axis_name, ):
        self.calculated_values = []
        self.sample = sample
        self.title = title
        self.x_axis_name = x_axis_name
        self.y_axis_name = y_axis_name

    @abstractmethod
    def calculate_params(self):
        pass

    def get_x_min_max_value(self):
        return [round(min([value[0] for value in self.calculated_values[0]]), 1) - 0.1,
                round(max([value[0] for value in self.calculated_values[0]]), 1) + 0.1]

    @abstractmethod
    def render(self):
        return {
            # 'dataset': [{
            #     'source': self.calculated_values[0],
            # }, {
            #     'transform': {
            #         'type': 'ecStat:regression'
            #         # 'linear' by default.
            #         # config: { method: 'linear', formulaOn: 'end'}
            #     }
            # }],
            'title': {
                'text': self.title,
                'left': 'center',
                'top': 10,
                'textStyle': {
                    'fontSize': 24,
                },
            },
            'tooltip': {
                'trigger': 'axis',
                'axisPointer': {
                    'type': 'cross'
                },
            },

            'xAxis': [{
                'name': self.x_axis_name,
                'min': self.get_x_min_max_value()[0],
                'man': self.get_x_min_max_value()[1],
                'nameTextStyle': {
                    'fontWeight': 'bolder',
                    'fontStyle': 'italic',
                    'fontSize': 16,
                },
                'splitNumber': 10,
            }],
            'yAxis': {
                'name': self.y_axis_name,
                'nameTextStyle': {
                    'fontWeight': 'bolder',
                    'fontStyle': 'italic',
                    'fontSize': 16,
                },
            },
            'graphic': [
                {
                    'type': 'group',
                    'left': '10%',
                    'top': '15%',
                    'children': [
                        {
                            'type': 'rect',
                            'z': 100,
                            'left': 'center',
                            'top': 'middle',
                            'shape': {
                                'width': 150,
                                'height': 40
                            },
                            'style': {
                                'fill': '#fff',
                                'stroke': '#555',
                                'lineWidth': 1,
                                'shadowBlur': 8,
                                'shadowOffsetX': 3,
                                'shadowOffsetY': 3,
                                'shadowColor': 'rgba(0,0,0,0.2)'
                            }
                        },
                        {
                            'type': 'text',
                            'z': 100,
                            'left': 'center',
                            'top': 'middle',
                            'style': {
                                'fill': '#333',
                                'text': 'S уд\nS',
                                'font': '14px Microsoft YaHei'
                            }
                        }
                    ]
                }
            ],
            'series': [{
                'symbolSize': 10,
                'data': self.calculated_values[0],
                'type': 'scatter',
            },
                # {
                # 'name': 'line',
                # 'type': 'line',
                # 'datasetIndex': 1,
                # 'symbolSize': 0.1,
                # 'symbol': 'circle',
                # 'label': {'show': True, 'fontSize': 16},
                # 'labelLayout': {'dx': -20},
                # 'encode': {'label': 2, 'tooltip': 1}
            ]
        }


class FullIsoterm(Models):
    def calculate_params(self):
        y_adsorb = [(round(point.p_p1, 2), point.get_volume(self.sample)) for
                    point in
                    self.sample.points
                    if point.adsorb_or_desorb == 0]

        y_desorb = [(round(point.p_p1, 2), point.get_volume(self.sample)) for
                    point in
                    self.sample.points
                    if point.adsorb_or_desorb == 1]

        self.calculated_values = [y_adsorb, y_desorb]

    def render(self):
        return {
            'title': {
                'text': self.title,
                'left': 'center',
                'top': 10,
                'textStyle': {
                    'fontSize': 24,
                },
            },

            'tooltip': {
                'trigger': 'axis',
                'axisPointer': {
                    'type': 'cross'
                },
            },
            'legend': {
                'bottom': 20,
            },
            'xAxis': {
                'name': self.x_axis_name,
                'nameTextStyle': {
                    'fontWeight': 'bolder',
                    'fontStyle': 'italic',
                    'fontSize': 16,
                },
                'splitNumber': 10,
            },
            'yAxis': {
                'name': self.y_axis_name,
                'nameTextStyle': {
                    'fontWeight': 'bolder',
                    'fontStyle': 'italic',
                    'fontSize': 16,
                },
            },
            'series': [{
                'symbolSize': 10,
                'data': self.calculated_values[0],
                'name': 'адсорбция',
                'type': 'scatter'
            }, {
                'symbolSize': 10,
                'data': self.calculated_values[1],
                'name': 'десорбция',
                'type': 'scatter'
            }]
        }


class Bet(Models):
    def _get_f_param(self, point):
        return round(
            (point.p_p1 / point.get_volume(self.sample) / (1 - point.p_p1)), 4)

    def calculate_params(self):
        y = [(round(point.p_p1, 2), self._get_f_param(point)) for
             point in self.sample.points if
             0.06 <= point.p_p1 <= 0.2 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]

    def render(self):
        return super().render()


class DeBoer(Models):
    def _get_f_param(self, point):
        return 0.1 * math.sqrt(13.99 / (0.034 - math.log10(point.p_p1)))

    def calculate_params(self):
        y = [(self._get_f_param(point), point.get_volume(self.sample)) for
             point in
             self.sample.points if
             0.1 <= point.p_p1 <= 0.75 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]

    def render(self):
        return super().render()


class Hasley(Models):
    def _get_hasley_param(self, point):
        return 0.354 * math.pow(-5 / math.log(point.p_p1), 1 / 3)

    def calculate_params(self):
        y = [(self._get_hasley_param(point), point.get_volume(self.sample)) for
             point in self.sample.points
             if 0.1 <= point.p_p1 <= 0.75 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]

    def render(self):
        return super().render()


class GarkinsYura(Models):
    def _get_garkins_param(self, point):
        return 0.1 * math.pow(60.65 / (0.03071 - math.log10(point.p_p1)),
                              0.3968)

    def calculate_params(self):
        y = [(self._get_garkins_param(point), point.get_volume(self.sample))
             for point in
             self.sample.points if
             0.1 <= point.p_p1 <= 0.95 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]

    def render(self):
        return super().render()


class TechnicalCarbon(Models):
    def _get_carbon_param(self, point):
        return 0.088 * math.pow(point.p_p1, 2) + \
               0.645 * point.p_p1 + 0.298

    def calculate_params(self):
        y = [(self._get_carbon_param(point), point.get_volume(self.sample)) for
             point in
             self.sample.points if
             0.2 <= point.p_p1 <= 0.5 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]

    def render(self):
        return super().render()
