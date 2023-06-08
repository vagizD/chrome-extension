import logging
from os.path import dirname, join, abspath

parent_dir = dirname(abspath(__file__))
logs_file = join(parent_dir, 'server_logs.txt')

logging_config = {"format": '%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                  "level": logging.INFO,  # make "level": logging.DEBUG for dev purposes
                  "filename": logs_file,
                  "filemode": "a+"}
