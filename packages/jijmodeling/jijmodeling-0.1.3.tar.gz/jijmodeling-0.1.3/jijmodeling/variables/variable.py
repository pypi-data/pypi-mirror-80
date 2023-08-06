from abc import ABCMeta, abstractmethod

class Variable(metaclass=ABCMeta):
    def __init__(self, label: str):
        self._label = label
        self.var_label = label

    @property
    def label(self):
        return self._label

    def set_relabel(self, label: str):
        self._label = label

    @abstractmethod
    def decode_dict_sample(self, sample: dict, placeholder: dict, additional_label: str=''):
        pass 
