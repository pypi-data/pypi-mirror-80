from typing import List, Tuple, Union, Type, Dict
import numbers

from numpy.lib.function_base import place
from pyqubo import array

from jijmodeling.variables.variable import Variable
from jijmodeling.variables.to_pyqubo import ToPyQUBO, to_pyqubo
from jijmodeling.variables.binary import Binary
from jijmodeling.variables.placeholder import Placeholder
from jijmodeling.sum import Sum
from jijmodeling.express.express import Express, from_serializable
import pyqubo
import numpy as np


class Tensor(Express, ToPyQUBO):
    """Tensor class for each variables

    Args:
        label
    """

    def __init__(self, label: str, variable, shape: tuple, indices: List[str]):
        """Tensor class for each variables

        Args:
            label (str): label for variable
            variable ([type]): variable object
            shape (tuple): shape of variable tensor
            indices (List[str]): index labels
        """
        super().__init__([])
        self.label = label
        self.variable = variable
        self.index_labels = indices
        self.shape = (shape, ) if isinstance(shape, int) else shape

    def __repr__(self):
        index_str = ''
        for i in self.index_labels:
            index_str += '[%s]' % i
        return self.label + index_str

    def to_pyqubo(self, index: Dict[str, int]={}, placeholder: dict={}, fixed_variables: dict={}) -> Union[pyqubo.Express, numbers.Number]:
        """Convert to PyQUBO object

        Tensor objects do not have a specific value for the index.
        But PyQUBO objects should be expanded as a concrete variable. 
        `index` argument gives a concrete value for the index of the Tensor object.
        For example, in case of converting `x['i', 'j']` into a PyQUBO object, generate a PyQUBO object labeled `x['i', 'j'].to_pyqubo(index={'i': 1, 'j': 2})` with the label `x[1, 2]'`.

        Args:
            index (Dict[str, int], optional): index values. Defaults to {}.
            placeholder (dict, optional): placeholder values. Defaults to {}.
            fixed_variables (dict, optional): fixed variable's values. Defaults to {}.

        Returns:
            Union[pyqubo.Express, numbers.Number]: converted PyQUBO objects.
        """
        index_label = self.label

        for label in self.index_labels:
            if not isinstance(label, str):
                _label = to_pyqubo(label, index=index, placeholder=placeholder, fixed_variables=fixed_variables)
                index_label += '[%d]' % _label
            else:
                index_label += '[%d]' % index[label]
        
        if index_label in fixed_variables:
            return fixed_variables[index_label]

        self.variable.set_relabel(index_label)
        return self.variable.to_pyqubo(index=index, placeholder=placeholder, fixed_variables=fixed_variables)

    def value(self, solution, placeholder, index):
        if self.label in solution:
            sol = solution[self.label]
        elif self.label in placeholder:
            sol = placeholder[self.label]

        def to_index(obj):
            if isinstance(obj, str):
                return index[obj]
            else:
                return to_pyqubo(obj, placeholder=placeholder)
        index_label = [to_index(label) for label in self.index_labels]
        return sol[tuple(index_label)]

    @classmethod
    def from_serializable(cls, seriablizable: dict):
        label = from_serializable(seriablizable['attributes']['label'])
        variable = from_serializable(seriablizable['attributes']['variable'])
        shape = from_serializable(seriablizable['attributes']['shape'])
        indices = from_serializable(seriablizable['attributes']['index_labels'])
        return cls(label, variable, tuple(shape), indices)






class ArraySizePlaceholder(Placeholder):

    def __init__(self, label:str) -> None:
        super().__init__(label)
        self._array = None

    @property
    def array(self):
        return self._array

    def set_array(self, array, shape_index: int):
        self._array = array
        self._shape_index = shape_index
    
    def to_pyqubo(self, index: Dict[str, int]={}, placeholder: dict={}, fixed_variables: dict={}) -> pyqubo.Express:
        array_data = placeholder[self._array.label]
        if isinstance(array_data, Express):
            raise TypeError('Placeholder "{}" should not be Express class.'.format(self._array.label))

        if isinstance(array_data.shape[self._shape_index], Express):
            raise TypeError('Placeholder "{}" should not be Express class.'.format(self._array.label))
        return array_data.shape[self._shape_index]

    def __eq__(self, other):
        if not isinstance(other, ArraySizePlaceholder):
            return False
        return self.label == self.label

    def __hash__(self):
        return hash(self.label)

    def to_serializable(self):

        return {
            'class': self.__class__.__module__ + '.' + self.__class__.__name__,
            'attributes': {
                'children': [],
                'label': self.label,
                '_array': self._array.to_serializable(),
                '_shape_index': self._shape_index
            },
        }

    @classmethod
    def from_serializable(cls, seriablizable: dict):
        placeholder = cls(seriablizable['attributes']['label'])
        placeholder.set_array(
            array=Array.from_serializable(seriablizable['attributes']['_array']),
            shape_index=seriablizable['attributes']['_shape_index']
        )
        return placeholder




class Array(Variable):
    """Tensor object generator
    This class generate Tensor class by index access

    """
    def __init__(self, variable, shape: Union[int, tuple, ArraySizePlaceholder, None]):
        self.variable = variable
        self._label = variable.label
        shape_list = list(shape) if isinstance(shape, tuple) else [shape] 
        for i, s in enumerate(shape_list):
            if isinstance(s, ArraySizePlaceholder):
                if s.array is None:
                    s.set_array(self, i)
                shape_list[i] = s
        self._shape = shape_list

        self.dim = len(self._shape)

    def to_serializable(self):
        def express_to_ser(s):
            if 'to_serializable' in dir(s):
                return s.to_serializable()
            elif isinstance(s, list):
                return [express_to_ser(t) for t in s]
            else:
                return s
        
        # shape が　ArraySizePlaceholder の場合,
        # このクラスへの参照を持つのでそれは避けるようにする
        variables = vars(self)
        variables['shape'] = self._shape


        serializable = {
            'class': self.__class__.__module__ + '.' + self.__class__.__name__,
            'attributes': {k: express_to_ser(v) for k, v in variables.items()}
        }

        return serializable

    @classmethod
    def from_serializable(cls, serializable):
        variable = from_serializable(serializable['attributes']['variable'])
        shape = from_serializable(serializable['attributes']['shape'])
        return cls(variable, shape)
    
    @property
    def shape(self):
        shape = []
        for i, s in enumerate(self._shape):
            if s is None:
                asph = ArraySizePlaceholder(label=self.label + '_shape_%d' % i)
                asph.set_array(self, i)
                shape.append(asph)
            else:
                shape.append(s)
        return tuple(shape)


    def __getitem__(self, key: Union[str, slice, Tuple[Union[str, slice], ...]])->Type[Express]:
        """Gerate Tensor class

        Args:
            key (Union[str, slice, Tuple[Union[str, slice], ...]]): [description]

        Raises:
            ValueError: [description]

        Returns:
            Type[Express]: [description]
        """
        if not isinstance(key, tuple):
            key = (key, )

        if len(key) != self.dim:
            raise ValueError("{}'s dimension is {}.".format(self.label, self.dim))

        indices: List[str] = []
        summation_index = []
        for i, k in enumerate(list(key)):
            # for syntaxsugar x[:]
            if isinstance(k, slice):
                indices.append(':_{}'.format(i))
                summation_index.append((i, indices[i]))
            elif isinstance(k, (int, str, Express)):
                indices.append(k)

        term = Tensor(self.label, self.variable, self.shape, indices)

        # for syntaxsugar x[:]
        for i, ind in summation_index:
            term = Sum({ind: self.shape[i]}, term)

        return term

    # def decode_dimod_response(self, response, placeholder)->dict:
    #     # decode shape
    #     _shape = tuple([to_pyqubo(s, placeholder=placeholder) for s in self.shape])
    #     return self.variable.decode_dimod_response(response, shape=_shape)

    def decode_dict_sample(self, sample: dict, placeholder: dict)->dict:
        # self.shape is not necessarily an `int`, such as the size of another Array object,
        # and the shape itself to be decoded using the `to_pyqubo` method.
        # TODO: The decoding method (to_pyqubo) needs to be renamed to make it
        # independent of PyQUBO in the future.
        shape = tuple([to_pyqubo(s, placeholder=placeholder) for s in self.shape])
        var_label = self.variable.var_label

        # initialize decoded array (return object)
        array_value = np.full(shape, np.nan, dtype=np.float)

        # Based on the `self.shape`, we recursively call `set_value`
        # and add the decoded value to the `array_value`.
        def set_value(fixed_indice: list):
            if len(fixed_indice) == len(shape):
                # When the number of `fixed_indices` equals dimension of the array,
                # i.e. len(shape), the elements of the array can finally be accessed.
                # The result of accessing and decoding the elements is stored in `array_value`.
                indices_str = str(fixed_indice).replace(',', '][').replace(' ', '')
                decoded_value = self.variable.decode_dict_sample(sample, placeholder, additional_label=indices_str)
                array_value[tuple(fixed_indice)] = decoded_value[var_label]
            else:
                # When `len(fixed_indices) < len(shape)`,
                # the values of all indices to access elements
                # have not yet been determinded.
                # Next, we will determined the value of the next dimension's
                # due to move on to the next recursive step.
                fixed_num = len(fixed_indice)
                for i in range(shape[fixed_num]):
                    new_fixed = fixed_indice + [i]
                    set_value(new_fixed)
        # start recursive iteration to set value for array_value.
        set_value([])
        return {var_label: array_value}