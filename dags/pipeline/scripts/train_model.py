import sys
import torch
import pandas as pd
import utils

config = utils.get_config('/tmp/config.yaml')
airflow_timestamp = sys.argv[1]
source_file = config['transformed_data_file']


df = utils.read_data_from_disk(filename = source_file, 
                           airflow_timestamp = airflow_timestamp, 
                           )


#train model and persist to dir