import logging
import os
from definitions import ROOT_DIR

logging_config = {"format": '%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                  "level": logging.INFO,  # make "level": logging.DEBUG for dev purposes
                  "filename": os.path.join(ROOT_DIR, 'server', 'logs', 'server_logs.txt'),
                  "filemode": "a+"}
