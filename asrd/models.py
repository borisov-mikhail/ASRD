import math
from abc import ABC, abstractmethod


class Models(ABC):
    def __init__(self, sample, x_axis_name, y_axis_name, ):
        self.title = None
        self.calculated_values = []
        self.sample = sample
        self.x_axis_name = x_axis_name
        self.y_axis_name = y_axis_name
        self.s_udel = 0

    @abstractmethod
    def calculate_params(self):
        pass

    def get_x_min_max_value(self):
        if len(self.calculated_values[0]) > 0:
            return [
                round(min([value[0] for value in self.calculated_values[0]]),
                      1) - 0.1,
                round(max([value[0] for value in self.calculated_values[0]]),
                      1) + 0.1]
        else:
            return [0, 1]

    @abstractmethod
    def lineal_regression(self, calculated_values):
        n = len(calculated_values[0])
        sum_x = sum(value[0] for value in calculated_values[0])
        sum_y = sum(value[1] for value in calculated_values[0])
        sum_x_y = sum(value[0] * value[1] for value in calculated_values[0])
        sum_x_2 = sum(value[0] * value[0] for value in calculated_values[0])
        a = ((sum_x * sum_y) - (n * sum_x_y)) / (
                (sum_x * sum_x) - (n * sum_x_2))
        b = ((sum_x * sum_x_y) - (sum_x_2 * sum_y)) / (
                (sum_x * sum_x) - (n * sum_x_2))
        if b >= 0:
            equation = 'y = ' + str(round(a, 3)) + 'x + ' + str(round(b, 3))
        else:
            equation = 'y = ' + str(round(a, 3)) + 'x - ' + str(
                round(abs(b), 3))

        regression_points = [(a, b, equation),
                             [(value[0], a * value[0] + b) for value in
                              calculated_values[0]]]
        return regression_points

    @abstractmethod
    def render(self):
        if len(self.calculated_values[0]) > 1:
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

                'xAxis': [{
                    'name': self.x_axis_name,
                    'min': self.get_x_min_max_value()[0],
                    'max': self.get_x_min_max_value()[1],
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
                                    'text': self.s_udel,
                                    'font': '14px Microsoft YaHei',
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
                    {
                        'name': 'Апроксимация',
                        'type': 'line',
                        'data': self.lineal_regression(self.calculated_values)[
                            1],
                        'smooth': True,
                        'symbolSize': 0.1,
                        'symbol': 'circle',
                        'markLine': {
                            'animation': False,
                            'label': {
                                'formatter': self.lineal_regression(
                                    self.calculated_values)[0][2],
                                'align': 'right',
                                'distance': [-15, 20],
                                'fontSize': 14
                            },
                            'lineStyle': {
                                'type': 'solid',
                                'width': 2.5
                            },

                            'data': [[{
                                'coord': self.lineal_regression(
                                    self.calculated_values)[1][0],
                                'symbol': 'none'
                            }, {
                                'coord': self.lineal_regression(
                                    self.calculated_values)[1][-1],
                                'symbol': 'none'
                            }]]
                        }

                    }
                ]
            }


class FullIsoterm(Models):
    def __init__(self, sample, x_axis_name, y_axis_name):
        super().__init__(sample, x_axis_name, y_axis_name)
        self.title = "Изотерма Адсорбции"

    def lineal_regression(self):
        pass

    def calculate_params(self):
        y_adsorb = [(round(point.p_p0, 2), round(point.volume, 4)) for point in
                    self.sample.points if point.adsorb_or_desorb == 0]

        y_desorb = [(round(point.p_p0, 2), round(point.volume, 4)) for point in
                    self.sample.points if point.adsorb_or_desorb == 1]

        self.calculated_values = [y_adsorb, y_desorb]

    def render(self):
        if len(self.calculated_values[0]) > 1:
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
                    'type': 'value',
                    'nameTextStyle': {
                        'fontWeight': 'bolder',
                        'fontStyle': 'italic',
                        'fontSize': 16,
                    },
                    'splitNumber': 10,
                },
                'yAxis': {
                    'name': self.y_axis_name,
                    'type': 'value',
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
    def __init__(self, sample, x_axis_name, y_axis_name):
        super().__init__(sample, x_axis_name, y_axis_name)
        self.title = 'БЭТ'

    def _get_f_param(self, point):
        return point.p_p0 / point.volume / (1 - point.p_p0) * 1000

    def lineal_regression(self, calculated_values):
        return super().lineal_regression(calculated_values)

    def calculate_params(self):
        y = [(point.p_p0, self._get_f_param(point)) for
             point in self.sample.points if
             0.06 <= point.p_p0 <= 0.2 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]

    def render(self):
        self.s_udel = 'Sуд = ' + str(round(4353.75 / (
                self.lineal_regression(self.calculated_values)[0][0] +
                self.lineal_regression(self.calculated_values)[0][1]),
                                           2)) + ' м²/г'
        return super().render()


class DeBoer(Models):
    def __init__(self, sample, x_axis_name, y_axis_name):
        super().__init__(sample, x_axis_name, y_axis_name)
        self.title = 'Модель Де-Бура'

    def _get_f_param(self, point):
        return round(0.1 * math.sqrt(13.99 / (0.034 - math.log10(point.p_p0))),
                     3)

    def lineal_regression(self, calculated_values):
        return super().lineal_regression(calculated_values)

    def calculate_params(self):
        y = [(self._get_f_param(point), round(point.volume, 4)) for point in
             self.sample.points if
             0.1 <= point.p_p0 <= 0.75 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]

    def render(self):
        # self.s_udel = 'Sуд = ' + str(
        #     round(self.lineal_regression(self.calculated_values)[0][0],
        #           2)) + ' м²/г'
        self.s_udel = 'Sуд = ' + str(round(4.35375 * 0.354 * (
            self.lineal_regression(self.calculated_values)[0][0]),
                                           2)) + ' м²/г'
        return super().render()


class Hasley(Models):
    def __init__(self, sample, x_axis_name, y_axis_name):
        super().__init__(sample, x_axis_name, y_axis_name)
        self.title = 'Модель Хэсли'

    def _get_hasley_param(self, point):
        return round(0.354 * math.pow(-5 / math.log(point.p_p0), 1 / 3), 3)

    def lineal_regression(self, calculated_values):
        return super().lineal_regression(calculated_values)

    def calculate_params(self):
        y = [(self._get_hasley_param(point), round(point.volume, 4)) for
             point in self.sample.points
             if 0.1 <= point.p_p0 <= 0.75 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]

    def render(self):
        self.s_udel = 'Sуд = ' + str(round(4.35375 * 0.354 * (
            self.lineal_regression(self.calculated_values)[0][0]),
                                           2)) + ' м²/г'
        return super().render()


class HarkinsJura(Models):
    def __init__(self, sample, x_axis_name, y_axis_name):
        super().__init__(sample, x_axis_name, y_axis_name)
        self.title = 'Модель Гаркинс-Юра'

    def _get_garkins_param(self, point):
        return round(0.1 * math.pow(60.65 / (0.03071 - math.log10(point.p_p0)),
                                    0.3968), 3)

    def lineal_regression(self, calculated_values):
        return super().lineal_regression(calculated_values)

    def calculate_params(self):
        y = [(self._get_garkins_param(point), round(point.volume, 4))
             for point in
             self.sample.points if
             0.1 <= point.p_p0 < 0.95 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]

    def render(self):
        self.s_udel = 'Sуд = ' + str(round(4.35375 * 0.354 * (
            self.lineal_regression(self.calculated_values)[0][0]),
                                           2)) + ' м²/г'
        return super().render()


class TechnicalCarbon(Models):
    def __init__(self, sample, x_axis_name, y_axis_name):
        super().__init__(sample, x_axis_name, y_axis_name)
        self.title = 'Модель технического углерода',

    def _get_carbon_param(self, point):
        return round(
            (0.088 * math.pow(point.p_p0, 2) + 0.645 * point.p_p0 + 0.298), 3)

    def lineal_regression(self, calculated_values):
        return super().lineal_regression(calculated_values)

    def calculate_params(self):
        y = [(self._get_carbon_param(point), round(point.volume, 4)) for
             point in
             self.sample.points if
             0.2 <= point.p_p0 <= 0.5 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]

    def render(self):
        self.s_udel = 'Sуд = ' + str(
            round(1.547 * self.lineal_regression(self.calculated_values)[0][0],
                  2)) + ' м²/г'
        return super().render()


class BrookhoffDeBoer(Models):
    def __init__(self, sample, x_axis_name, y_axis_name):
        super().__init__(sample, x_axis_name, y_axis_name)
        self.title = 'Модель Брукгоффа-де Бура'

    def _get_f_param(self, point):
        for t in range(5000, 30000):
            val = float(-16.11 / t / t * 1000000 + 0.1682 * math.exp(
                -0.1137 * t / 1000))
            if abs(math.log10(point.p_p0) - val) < 0.0001:
                return t / 10000
            else:
                continue

    def lineal_regression(self, calculated_values):
        return super().lineal_regression(calculated_values)

    def calculate_params(self):
        y = [(self._get_f_param(point), round(point.volume, 4)) for point in
             self.sample.points if
             0.3 <= point.p_p0 <= 0.93 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]

    def render(self):
        self.s_udel = 'Sуд = ' + str(round(4.35375 * 0.354 * (
            self.lineal_regression(self.calculated_values)[0][0]),
                                           2)) + ' м²/г'
        return super().render()
