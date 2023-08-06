# -*- coding: utf-8 -*-


class dict_with_default(dict):
    """Dictionary that returns a default value when key is missing

    :param default: default value to return when key is missing
    """
    def __init__(self, default, *args, **kwargs):
        super(dict_with_default, self).__init__(*args, **kwargs)
        self.default = default

    def __missing__(self, key):
        return self.default


def dict_factory(name, default):
    """Return a subclass of dict with a default value

    :param name: name of the subclass
    :type name: string
    :param default: the default value returned by the dict instead of KeyError
    """
    def __missing__(self, key):
        return default
    new_class = type(name, (dict,), {"__missing__": __missing__})
    return new_class


class dict_default(dict):
    """Dictionary subclass that returns the key instead of a KeyError
    """
    def __missing__(self, key):
        return key


def bitwise_operator(frame, operator):
    """Returns the result of applying the bitwise ``|`` or ``&`` operator to a
    list of series

    :param frame: data with colums to apply the bitwise operator to
    :type frame: DataFrame
    :param operator: the operator to apply. 'and' and 'or' are acceptable
                     values
    """
    num_cols = frame.shape[1]
    if num_cols == 1:
        return frame.iloc[:, 0]
    else:
        series = frame.iloc[:, 0]
        for i in range(1, num_cols):
            if operator == 'and':
                series = series & frame.iloc[:, i]
            elif operator == 'or':
                series = series | frame.iloc[:, i]
    return series


def bitwise_xor(frame):
    """Returns the result of applying the bitwise ``^`` operator to two Series
    in a DataFrame

    :param frame: data with colums to apply the bitwise or operator to
    :type frame: DataFrame
    """
    num_cols = frame.shape[1]
    if num_cols != 2:
        raise ValueError("DataFrame must have 2 columns.")
    else:
        series = frame.iloc[:, 0] ^ frame.iloc[:, 1]
    return series


def bitwise_not(frame):
    """Returns the result of applying the bitwise ``~`` operator to the
    boolean conversion of the DataFrame

    :param frame: data with colums to apply the bitwise or operator to
    :type frame: DataFrame
    """
    return ~frame.astype('bool')
