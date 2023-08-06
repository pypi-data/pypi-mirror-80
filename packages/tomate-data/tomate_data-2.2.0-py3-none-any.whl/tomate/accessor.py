"""Access data array.

The accessor object allow to put an abstract
layer between the data and Tomate API. This makes
Tomate data-format agnostic (to a certain extent).
The main way is still to store data in numpy arrays.
"""

# This file is part of the 'tomate' project
# (http://github.com/Descanonge/tomate) and subject
# to the MIT License as defined in the file 'LICENSE',
# at the root of this project. © 2020 Clément HAËCK


import logging
from typing import List, Iterable, Union
import itertools

import numpy as np


from tomate.custom_types import Array
from tomate.keys.keyring import Keyring

log = logging.getLogger(__name__)


class AccessorABC():
    """Manages access to arrays.

    Stores static and class methods.
    Can be subclassed for different implementation.

    See :doc:`../accessor`.
    """
    @staticmethod
    def ndim(array: Array) -> int:
        """Return number of dimensions of array."""
        raise NotImplementedError

    @staticmethod
    def shape(array: Array) -> List[int]:
        """Return shape of array."""
        raise NotImplementedError

    @classmethod
    def check_applicable(cls, keyring: Iterable, array: Array):
        """Check if `keyring` can be applied to `array`.

        :raises IndexError: If dimensions do not match.
        """
        if cls.ndim(array) != len(keyring):
            raise IndexError("Keyring not applicable to array,"
                             " difference in dimensions."
                             " (array shape: {}, keyring length: {})"
                             .format(cls.shape(array), len(keyring)))

    @classmethod
    def check_parent(cls, keyring: Keyring, array: Array):
        """Check if `array` could have been obtained with `keyring`.

        :raises IndexError: If dimensions do not match.
        :raises ValueError: If shapes do not match.
        """
        if cls.ndim(array) != len(keyring.get_non_zeros()):
            raise IndexError("Array could not have been obtained with"
                             " keyring. Mismatch in dimensions."
                             " (array shape: {}, keyring shape: {})"
                             .format(cls.shape(array), keyring.shape))
        if not keyring.is_shape_equivalent(cls.shape(array)):
            raise ValueError("Array could not have been obtained with"
                             " keyring. Mismatch in shape."
                             " (array shape: {}, keyring shape: {})"
                             .format(cls.shape(array), keyring.shape))

    @staticmethod
    def allocate(shape: List[int], datatype=None) -> Array:
        """Allocate array of given shape."""
        raise NotImplementedError

    @staticmethod
    def get_datatype(data: Array) -> str:
        """Get array datatype as string."""
        raise NotImplementedError

    @classmethod
    def take(cls, keyring: Keyring, array: Array) -> Array:
        """Retrieve part of an array.

        Amounts to `return array[keyring]`.
        :param keyring: Part of the array to take.
        :returns: View or copy of the array.

        Notes
        -----
        See :doc:`../accessor` for more information.
        """
        raise NotImplementedError

    @classmethod
    def place(cls, keyring: Keyring, array: Array, chunk: Array):
        """Assign a part of array with another array.

        Amounts to `array[keyring] = chunk`.

        :param keyring: Part of array to assign.
        :param array: Array to assign.
        :param chunk: Array to be assigned.
        """
        raise NotImplementedError

    @staticmethod
    def moveaxis(array: Array,
                 source: List[int],
                 destination: List[int]) -> Array:
        """Exchange axes.

        :param source: Original position of axes to move.
        :param destination: Destination positions of axes to move.
        """
        raise NotImplementedError

    @classmethod
    def reorder(cls, current: List[str], array: Array,
                order: List[str], log_lvl: Union[bool, str] = 'DEBUG') -> Array:
        """Reorder array dimensions.

        :param current: Current dimensions order.
        :param order: Target dimensions order. Either of same
            length as current, or of length 2 which will swap
            the two dimensions (if in different order than current)
        :raises IndexError: `order` has incorrect length.
        """
        if len(order) != len(current):
            if len(order) != 2:
                raise IndexError("Length of order must be the same as the array, or 2.")
            source = [current.index(n) for n in order]
            dest = source
            if source[0] > source[1]:
                dest = dest[::-1]
        else:
            source = list(range(len(order)))
            dest = [order.index(n) for n in current]
        if source != dest:
            if log_lvl:
                log.log(getattr(logging, log_lvl.upper()),
                        "Reordering %s -> %s", source, dest)
            return cls.moveaxis(array, source, dest)
        return array

    @staticmethod
    def concatenate(arrays: List[Array],
                    axis: int = 0,
                    out: Array = None) -> Array:
        """Concatenate arrays.

        :param arrays: Arrays to concatenate.
        :param axis: The axis along which the arrays will be joined.
            If None, the arrays are flattened.
        :param out: Array to place the result in.
        """
        raise NotImplementedError

    @staticmethod
    def stack(arrays: List[Array],
              axis: int = 0,
              out: Array = None) -> Array:
        """Stack arrays along a new axis.

        :param arrays: Arrays to stack.
        :param axis: The axis along which the arrays will be joined.
        :param out: Array to place the result in.
        """
        raise NotImplementedError


class Accessor(AccessorABC):
    """Manages access to numpy arrays.

    See :doc:`../accessor`.
    """

    @staticmethod
    def ndim(array: np.ndarray) -> int:
        return array.ndim

    @staticmethod
    def shape(array: np.ndarray) -> List[int]:
        return list(array.shape)

    @staticmethod
    def allocate(shape: List[int], datatype=None) -> np.ndarray:
        return np.zeros(shape, dtype=datatype)

    @staticmethod
    def get_datatype(data: Array) -> str:
        return data.dtype.str

    @classmethod
    def has_normal_access(cls, keyring: Keyring) -> bool:
        """Check if keyring would need complex access."""
        n_list = [k.type for k in keyring.keys].count('list')
        n_int = [k.type for k in keyring.keys].count('int')
        if n_list >= 2:
            return False
        if n_list > 1 and n_int >= 1:
            return False

        return True

    @classmethod
    def take(cls, keyring: Keyring, array: np.ndarray) -> np.ndarray:
        """Retrieve part of an array.

        Amounts to `return array[keyring]`.

        Uses numpy normal indexing when possible.
        If not, uses more complex method to access array.

        :param keyring: Part of the array to take.
        :returns: View of the input array in the case
            of normal indexing, or a copy otherwise.

        Notes
        -----
        See :doc:`../accessor` for more information.

        See Numpy docpage on `indexing
        <https://docs.scipy.org/doc/numpy/user/basics.indexing.html>`__

        See also
        --------
        take_normal: Function used for normal indexing.
        take_complex: Function used when normal indexing would not work.
        """
        if cls.has_normal_access(keyring):
            return cls.take_normal(keyring, array)
        return cls.take_complex(keyring, array)

    @classmethod
    def take_normal(cls, keyring: Keyring, array: np.ndarray) -> np.ndarray:
        """Retrieve part of an array with normal indexing.

        Amounts to `array[keyring]`.
        Returns a view into the array.

        :param keyring: Part of the array to take.
        """
        cls.check_applicable(keyring, array)
        return array[tuple(keyring.keys_values)]

    @classmethod
    def take_complex(cls, keyring: Keyring, array: np.ndarray) -> np.ndarray:
        """Retrieve part of an array without normal indexing.

        Amounts to `array[keyring]`.
        Returns a copy of the array.

        :param keyring: Part of the array to take.
        """
        cls.check_applicable(keyring, array)

        out = array
        keys = []
        for i, k in enumerate(keyring.keys):
            keys_ = tuple(keys + [k.value])
            log.debug('take_complex executing out = %s%s',
                      'array' if i == 0 else 'out', list(keys_))
            out = out[keys_]
            if k.shape != 0:
                keys.append(slice(None, None))
        return out

    @classmethod
    def place(cls, keyring: Keyring, array: np.ndarray, chunk: np.ndarray):
        """Assign a part of array with another array.

        Amounts to `array[keyring] = chunk`.
        Uses numpy normal indexing when possible.
        If not, uses more complex method to access array.

        :param keyring: Part of array to assign.
        :param array: Array to assign.
        :param chunk: Array to be assigned.

        See also
        --------
        take: Function to access part of array, with more
             details on normal and complexed indexing.
        """
        if cls.has_normal_access(keyring):
            cls.place_normal(keyring, array, chunk)
        else:
            cls.place_complex(keyring, array, chunk)

    @classmethod
    def place_normal(cls, keyring: Keyring, array: np.ndarray, chunk: np.ndarray):
        """Assign a part of an array with normal indexing.

        Amounts to `array[keyring] = chunk`.
        Uses numpy normal indexing when possible.
        If not, uses more complex method to access array.

        :param keyring: Part of array to assign.
        :param array: Array to assign.
        :param chunk: Array to be assigned.
       """
        if len(keyring.shape) > 0:
            cls.check_parent(keyring, chunk)
        array[tuple(keyring.keys_values)] = chunk

    @classmethod
    def place_complex(cls, keyring: Keyring, array: np.ndarray, chunk: np.ndarray):
        """Assign part of an array without normal indexing.

        Amounts to `array[keyring] = chunk`.
        List keys are transformed in combination of integers.

        :param keyring: Part of array to assign.
        :param array: Array to assign.
        :param chunk: Array to be assigned.
        """
        cls.check_parent(keyring, chunk)

        list_keys = [n for n, k in keyring.items() if k.type == 'list']
        krg = keyring.copy()
        for m in itertools.product(*[range(keyring[d].shape) for d in list_keys]):
            krg_chunk = [0] * len(list_keys)
            for i_d, d in enumerate(list_keys):
                krg[d] = keyring[d].value[m[i_d]]
                krg_chunk[i_d] = m[i_d]
            log.debug('place_complex executing array%s = chunk%s',
                      krg.print(), krg_chunk)
            array[tuple(krg.keys_values)] = chunk[tuple(krg_chunk)]

    @staticmethod
    def moveaxis(array: np.ndarray,
                 source: List[int],
                 destination: List[int]) -> np.ndarray:
        """ Exchange axes.

        :param source: Original position of axes to move.
        :param destination: Destination positions of axes to move.

        See also
        --------
        numpy.moveaxis: Function used.
        """
        out = np.moveaxis(array, source, destination)
        return out

    @staticmethod
    def concatenate(arrays: List[np.ndarray],
                    axis: int = 0,
                    out: np.ndarray = None) -> np.ndarray:
        """Concatenate arrays.

        :param arrays: Arrays to concatenate.
        :param axis: The axis along which the arrays will be joined.
            If None, the arrays are flattened.
        :param out: Array to place the result in.

        See also
        --------
        numpy.concatenate: Function used.
        """
        return np.concatenate(arrays, axis=axis, out=out)

    @staticmethod
    def stack(arrays: List[Array],
              axis: int = 0,
              out: Array = None) -> Array:
        """Stack arrays along a new axis.

        :param arrays: Arrays to stack.
        :param axis: The axis along which the arrays will be joined.
        :param out: Array to place the result in.

        See also
        --------
        numpy.stack: Function used.
        """
        return np.stack(arrays, axis=axis, out=out)
