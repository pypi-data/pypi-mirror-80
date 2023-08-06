from abc import ABCMeta, abstractmethod
from typing import Dict, Union
import numbers
import pyqubo


class ToPyQUBO(metaclass=ABCMeta):

    def __init__(self, label: str) -> None:
        self.label = label
        self.index_labels = []

    @abstractmethod
    def to_pyqubo(self, index: Dict[str, int]={}, placeholder: dict={}, fixed_variables: dict={})->pyqubo.Express:
        raise NotImplementedError()
        


def to_pyqubo(object: ToPyQUBO, **kwargs)->Union[pyqubo.Express, numbers.Number]:
    """convert to PyQUBO object.

    Args:
        object (:obj:`ToPyQUBO`): Convertable to PyQUBO object.

    Raises:
        TypeError: if `object` does not inherit ToPyQUBO class.

    Returns:
        (:obj: `pyqubo.Express`, :obj: `numbers.Number`): [description]
    """
    if isinstance(object, ToPyQUBO):
        return object.to_pyqubo(**kwargs)
    elif isinstance(object, numbers.Number):
        return object
    else:
        raise TypeError('{} cannnot convert to PyQUBO object.'.format(object))