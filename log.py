import logging

logger = logging.getLogger('Logger')
formatting = '[%(asctime)s] [%(levelname)s]: %(message)s'
logging.basicConfig(level=logging.INFO, format=formatting)
success_log = 'success.log'  # INFO
warning_log = 'warning.log'  # WARNING
error_log = 'error.log'  # ERROR


def log_write_to_file(file_name: str, message: str):
    '''запись в файл лога'''
    with open(file_name, 'a', encoding='utf8') as file:
        file.write(message + '\n')