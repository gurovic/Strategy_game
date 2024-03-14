import logging, os, inspect, functools

def method_log(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        frame = inspect.currentframe().f_back
        file_name = os.path.abspath(frame.f_code.co_filename)
        relative_file_path = os.path.relpath(file_name, start=root_folder_path)
        line_number = frame.f_lineno

        try:
            result = method.__get__(self)(*args, **kwargs)
            log_message = f"{relative_file_path}:{line_number} {self.__class__.__name__}.{method.__name__} args={args}, kwargs={kwargs}"
            if len(log_message) > 200:
                log_message = log_message[:197] + "..."
            logger.info(log_message)
            return result
        except Exception as e:
            log_message = f"{relative_file_path}:{line_number} in {self.__class__.__name__}.{method.__name__} Error: {str(e)}. args={args}, kwargs={kwargs} "
            if len(log_message) > 200:
                log_message = log_message[:197] + "..."
            logger.error(log_message)
            raise
    return wrapper

def class_log(cls):
    for name, method in vars(cls).items():
        if callable(method):
            setattr(cls, name, method_log(method))
    return cls


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


logs_file_path = os.path.join(os.path.dirname(__file__), '../../media/logs.txt')

file_handler = logging.FileHandler(logs_file_path)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.propagate = False


root_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

