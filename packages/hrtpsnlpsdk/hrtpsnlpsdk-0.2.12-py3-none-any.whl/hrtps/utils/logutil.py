import functools
import inspect
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_current_function_name():
    """
    inspect.stack():动态获取运行的函数名
    """
    return inspect.stack()


def invalid_log(param):
    if callable(param):
        def wrapper(*args, **kw):
            res = get_current_function_name()
            func_names = [res[2][3], res[1][3], res[0][3]]
            logger.warning('invalid method [%s]' % (param.__name__,))
            logger.warning('invalid method {}'.format(func_names))
            # print('invalid method [%s]' % (param.__name__,))
            param(*args, **kw)

        return wrapper

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            res = get_current_function_name()
            func_names = [res[2][3], res[1][3], res[0][3]]
            logger.warning('invalid method [%s]' % (func.__name__,))
            logger.warning('invalid method {}'.format(func_names))
            print('invalid method [%s]' % (func.__name__,))
            # print('%s %s():' % (param, func.__name__))
            return func(*args, **kw)

        return wrapper

    return decorator


def wrap_class(cls):
    """
    函数装饰类装饰器
    :param cls:
    :return:
    """

    def inner(**kwargs):
        res = get_current_function_name()
        func_names = [res[2][3], res[1][3], res[0][3]]
        print(func_names)

        case_name = ''
        for func_name in func_names:
            if func_name.startswith('test_'):
                case_name = func_name
                break
        if case_name.startswith('test_'):
            return cls(pvid=case_name)
        else:
            return cls(**kwargs)

    return inner
