import math
from abc import ABC, abstractmethod


class Models(ABC):
    def __init__(self, sample):
        self.calculated_values = []
        self.sample = sample

    @abstractmethod
    def calculate_params(self):
        pass

    @abstractmethod
    def render(self):
        pass


class FullIsoterm(Models):
    def calculate_params(self):
        y_adsorb = [(point.p_p1, point.get_volume(self.sample)) for point in
                    self.sample.points
                    if point.adsorb_or_desorb == 0]

        y_desorb = [(point.p_p1, point.get_volume(self.sample)) for point in
                    self.sample.points
                    if point.adsorb_or_desorb == 1]

        self.calculated_values = [y_adsorb, y_desorb]

    def render(self):
        return {
            'xAxis': {},
            'yAxis': {},
            'tooltip': {},
            'series': [{
                'symbolSize': 10,
                'data': self.calculated_values[0],
                'type': 'scatter'
            }, {
                'symbolSize': 10,
                'data': self.calculated_values[1],
                'type': 'scatter'
            }]
        }


class Bet(Models):
    def _get_f_param(self, point):
        return point.p_p1 / point.get_volume(self.sample) / (1 - point.p_p1)

    def calculate_params(self):
        y = [(point.p_p1, self._get_f_param(point)) for
             point in self.sample.points if
             0.06 <= point.p_p1 <= 0.2 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]

    def render(self):
        return {
            'xAxis': {},
            'yAxis': {},
            'tooltip': {},
            'series': [{
                'symbolSize': 10,
                'data': self.calculated_values[0],
                'type': 'scatter'
            }]
        }


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
        return {
            'xAxis': {},
            'yAxis': {},
            'tooltip': {},
            'series': [{
                'symbolSize': 10,
                'data': self.calculated_values[0],
                'type': 'scatter'
            }]
        }


class Hasley(Models):
    def _get_hasley_param(self, point):
        return 0.354 * math.pow(-5 / math.log(point.p_p1), 1 / 3)

    def calculate_params(self):
        y = [(self._get_hasley_param(point), point.get_volume(self.sample)) for
             point in self.sample.points
             if 0.1 <= point.p_p1 <= 0.75 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]

    def render(self):
        return {
            'xAxis': {},
            'yAxis': {},
            'tooltip': {},
            'series': [{
                'symbolSize': 10,
                'data': self.calculated_values[0],
                'type': 'scatter'
            }]
        }


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
        return {
            'xAxis': {},
            'yAxis': {},
            'tooltip': {},
            'series': [{
                'symbolSize': 10,
                'data': self.calculated_values[0],
                'type': 'scatter'
            }]
        }


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
        return {
            'xAxis': {},
            'yAxis': {},
            'tooltip': {},
            'series': [{
                'symbolSize': 10,
                'data': self.calculated_values[0],
                'type': 'scatter'
            }]
        }
