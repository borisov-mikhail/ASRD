from abc import ABC, abstractmethod
import math

class Models(ABC):

    def __init__(self, sample):
        self.calculated_values = []
        self.sample = sample

    @abstractmethod
    def calculate_params(self):
        pass


class FullIsoterm(Models):

    def calculate_params(self):
        for point in self.sample.points:
            volume = float(point.S_of_pick) * float(point.grad_koeff) / \
                     float(self.sample.mass)
            point.volume = volume

        y_adsorb = [[point.p_p1, point.volume] for point in self.sample.points
                    if
                    point.adsorb_or_desorb == 0]
        y_desorb = [[point.p_p1, point.volume] for point in self.sample.points
                    if
                    point.adsorb_or_desorb == 1]
        self.calculated_values = [y_adsorb, y_desorb]


class Bet(Models):

    def calculate_params(self):
        for point in self.sample.points:
            f_param = point.p_p1 / point.volume / (1 - point.p_p1)
            point.f_param = f_param

        y = [[point.p_p1, point.f_param] for point in self.sample.points if
             0.06 <= point.p_p1 <= 0.2 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]


class DeBoer(Models):

    def calculate_params(self):
        for point in self.sample.points:
            t_param = 0.1 * math.sqrt(13.99 / (0.034 - math.log10(point.p_p1)))
            point.t_param = t_param

        y = [[point.t_param, point.volume] for point in self.sample.points if
             0.1 <= point.p_p1 <= 0.75 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]


class Hasley(Models):

    def calculate_params(self):
        for point in self.sample.points:
            hasley_param = 0.354 * math.pow(-5 / math.log(point.p_p1), 1/3)
            point.hasley_param = hasley_param

        y = [[point.hasley_param, point.volume] for point in self.sample.points if
             0.1 <= point.p_p1 <= 0.75 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]


class GarkinsYura(Models):

    def calculate_params(self):
        for point in self.sample.points:
            garkins_param = 0.1 * math.pow(
                60.65 / (0.03071 - math.log10(point.p_p1)), 0.3968)
            point.garkins_param = garkins_param

        y = [[point.garkins_param, point.volume] for point in
             self.sample.points if
             0.1 <= point.p_p1 <= 0.95 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]


class TechnicalCarbon(Models):

    def calculate_params(self):
        for point in self.sample.points:
            carbon_param = 0.088 * math.pow(point.p_p1, 2) + \
                           0.645 * point.p_p1 + 0.298

            point.carbon_param = carbon_param

        y = [[point.carbon_param, point.volume] for point in
             self.sample.points if
             0.2 <= point.p_p1 <= 0.5 and point.adsorb_or_desorb == 0]

        self.calculated_values = [y]
