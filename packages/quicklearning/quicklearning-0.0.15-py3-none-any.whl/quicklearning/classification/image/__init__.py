import logging

def disable_tensorflow_warnings(func):
    def inner(*args, **kwargs):
        logging.getLogger("tensorflow").setLevel(logging.ERROR)
        x = func(*args, **kwargs)
        logging.getLogger("tensorflow").setLevel(logging.WARNING)
        return x
    return inner