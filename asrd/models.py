from abc import ABC, abstractmethod


class Models(ABC):

    @abstractmethod
    def calculate_params(self):
        pass
