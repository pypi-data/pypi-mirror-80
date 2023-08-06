class HuoYanError(Exception):
    """nothing"""


def _raise_huoyanerror_object():
    raise HuoYanError('Please use the right object')


def _raise_huoyanerror_parameter():
    raise HuoYanError('All parameters you pass in must have default values')


__version__ = '1.5.2'
__author__ = 'F.S'
__thank__ = ['Bingyi Liu', 'Ziyv Yan', 'Zeyv Zhong']
__all__ = ["request", 'c', 'log_in', 'print', 'print_logo', 'python_plot',
           'spark_word']
