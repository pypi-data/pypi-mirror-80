from numpy.lib.ufunclike import fix
from build.lib.jijmodeling.variables.to_pyqubo import to_pyqubo
from typing import Union, Dict
from jijmodeling.express.express import Express, from_serializable
from jijmodeling.variables.to_pyqubo import ToPyQUBO
from jijmodeling.variables.placeholder import Placeholder
from abc import ABCMeta, abstractmethod

import math


# TODO: この内部はまだ実装中なので使えません。LogなどPlaceholderに対しての演算を表すExpress関数を記述していきます。

PlaceholderType = Union[Placeholder, int, float]

class PlaceholderMathFunc(Express, ToPyQUBO, metaclass=ABCMeta):
    """実装中です. 使えません.
    """
    def __init__(self, terms: list, **kwargs):
        super().__init__(terms)
        self.parameters = kwargs

    @abstractmethod
    def _math_func(self, terms, **kwargs):
        pass

    def to_pyqubo(self, index: Dict[str, int], placeholder: dict, fixed_variables: dict):
        terms = [to_pyqubo(t, placeholder=placeholder, fixed_variables=fixed_variables) for t in self.children]
        params = {k: to_pyqubo(v, placeholder=placeholder, fixed_variables=fixed_variables) for k, v in self.parameters.items()}
        return self._math_func(terms, **params)

    def value(self, solution, placeholder: dict, index: dict):
        def to_value(term):
            if isinstance(term, Express):
                return term.value(solution, placeholder, index)
            else:
                return term
        terms = [to_value(t) for t in self.children]



class Log(Express, ToPyQUBO):
    """実装中です. 使えません.
    """
    def __init__(self, antilogarithm: PlaceholderType, base:float = math.e):
        super().__init__([antilogarithm])
        self.base = base
        self.antilogarithm = antilogarithm

    def to_pyqubo(self, index: Dict[str, int], placeholder: dict, fixed_variables: dict) -> pyqubo.Express:
        base = to_pyqubo(self.base, placeholder=placeholder, fixed_variables=fixed_variables)
        antilogarithm = to_pyqubo(self.antilogarithm, placeholder=placeholder, fixed_variables=fixed_variables)
        return math.log(antilogarithm, base)
    
    def value(self, solution, placeholder: dict, index: dict):
        base = self.base.value(solution, placeholder, index)
        antilogarithm = self.antilogarithm.value(solution, placeholder, index)
        return math.log(antilogarithm, base)

    @classmethod
    def from_serializable(cls, seriablizable: dict):
        base = from_serializable(seriablizable['attributes']['base'])
        antilog = from_serializable(seriablizable['attributes']['antilogarithm'])
        return cls(antilog, base)



