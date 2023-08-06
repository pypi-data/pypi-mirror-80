from jijmodeling.variables import placeholder
from jijmodeling.variables.variable import Variable
from jijmodeling.variables.to_pyqubo import ToPyQUBO, to_pyqubo
from jijmodeling.express.express import Express
import numpy as np
import pyqubo

class LogEncInteger(Express, Variable, ToPyQUBO):
    """Log encoded interger

    .. math::
        x = \\frac{\\text{upper}-\\text{lower}}{} \sum_{l=0}^{\\text{bits}-1} 2^l s_l + \\text{lower},~
        (s_l \in \{0, 1\}~ \\forall l)

    .. math::
        \\text{lower} \leq x \leq \\text{upper}

    """
    def __init__(self, label: str, lower: int, upper: int):
        super().__init__([])
        self._label = label
        self.var_label = label
        self.lower = lower
        self.upper = upper
        

    def __repr__(self) -> str:
        return self.label

    def to_pyqubo(self, index:dict={}, placeholder:dict={}, fixed_variables: dict = {}):
        if self.label in fixed_variables:
            return fixed_variables[self.label]
        var_label = self.label + '[{}]'
        upper = to_pyqubo(self.upper, placeholder=placeholder)
        lower = to_pyqubo(self.lower, placeholder=placeholder)
        bits = int(np.log2(upper - lower))+1
        return sum(2**i * pyqubo.Binary(var_label.format(i)) for i in range(bits)) + lower


    def decode_dict_sample(self, sample: dict, placeholder: dict={}, additional_label: str = '') -> dict:
        """decode dict type sample

        Args:
            sample (dict): sample solution (ex. {'a': 1, 'b': 0}). sample should have key is variable's label.
            additional_label (str): Defaults ''.

        Returns:
            dict: decoded sample.

        Examples:
            >>> x = LogEncInteger('x', lower=0, upper=7)
            >>> sample = {'x[0]': 0, 'x[1]': 1, 'x[2]': 1}
            >>> decoded = x.decode_dict_sample(sample)
            >>> decoded
            {'x': 6}
        """
        var_name = self.var_label + additional_label

        upper = to_pyqubo(self.upper, placeholder=placeholder)
        lower = to_pyqubo(self.lower, placeholder=placeholder)
        bits = int(np.log2(upper - lower))+1

        value = 0.0
        for bit in range(bits):
            var_indices = var_name +'[{}]'.format(bit)
            value += 2**bit * sample[var_indices]
        
        value = int(value + lower)
        return {self.var_label: value}