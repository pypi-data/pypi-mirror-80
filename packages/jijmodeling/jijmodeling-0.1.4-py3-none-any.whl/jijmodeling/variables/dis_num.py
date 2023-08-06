from jijmodeling.variables import placeholder
from jijmodeling.variables.variable import Variable
from jijmodeling.variables.to_pyqubo import ToPyQUBO, to_pyqubo
from jijmodeling.express.express import Express
from jijmodeling.variables.log_int import LogEncInteger
import numpy as np
import pyqubo


class DisNum(Express, Variable, ToPyQUBO):
    """Discreated number class

    .. math::
        x = \\frac{\\text{upper}-\\text{lower}}{2^{\\text{bits}}-1} \sum_{l=0}^{\\text{bits}-1} 2^l s_l + \\text{lower},~
        (s_l \in \{0, 1\}~ \\forall l)

    .. math::
        \\text{lower} \leq x \leq \\text{upper}

    """
    def __init__(self, label: str, lower: float=0.0, upper: float=1.0, bits: int=3):
        super().__init__([])
        self._label = label
        self.var_label = label
        self.lower = lower
        self.upper = upper
        self.bits = bits

    def __repr__(self) -> str:
        return self.label

    def to_pyqubo(self, index:dict={}, placeholder:dict={}, fixed_variables: dict = {}):
        if self.label in fixed_variables:
            return fixed_variables[self.label]
        var_label = self.label + '[{}]'
        upper = to_pyqubo(self.upper, placeholder=placeholder)
        lower = to_pyqubo(self.lower, placeholder=placeholder)
        bits = to_pyqubo(self.bits, placeholder=placeholder)
        coeff = (upper - lower)/(2**bits - 1)
        return coeff * sum(2**i * pyqubo.Binary(var_label.format(i)) for i in range(self.bits)) + self.lower


    def decode_dict_sample(self, sample: dict, placeholder: dict={}, additional_label: str = '') -> dict:
        """decode dict type sample

        Args:
            sample (dict): sample solution (ex. {'a': 1, 'b': 0}). sample should have key is variable's label.
            additional_label (str): Defaults ''.

        Returns:
            dict: decoded sample.

        Examples:
            >>> x = DisNum('x', lower=0.0, upper=7.0, bits=3)
            >>> sample = {'x[0]': 0, 'x[1]': 1, 'x[2]': 1}
            >>> decoded = x.decode_dict_sample(sample)
            >>> decoded
            {'x': 6.0}
        """
        var_name = self.var_label + additional_label
        value = 0.0
        for bit in range(self.bits):
            var_indices = var_name +'[{}]'.format(bit)
            value += 2**bit * sample[var_indices]
        upper = to_pyqubo(self.upper, placeholder=placeholder)
        lower = to_pyqubo(self.lower, placeholder=placeholder)
        bits = to_pyqubo(self.bits, placeholder=placeholder)

        coeff = (upper - lower)/(2**bits-1)
        value = coeff * value + self.lower
        return {self.var_label: value}

       