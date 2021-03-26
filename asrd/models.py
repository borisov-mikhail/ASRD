from abc import ABC, abstractmethod


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
