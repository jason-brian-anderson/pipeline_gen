import sys
import pandas as pd
import utils
config = utils.get_config('/tmp/config.yaml')
#filename = 'raw_harvested_data.csv'
#mnt_dir = '/mnt/data'
airflow_timestamp = sys.argv[1]



#harvest data from source
data = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6]})

utils.persist_data_to_disk(mnt_dir = config['container_data_path'], 
                           filename = config['raw_data_file'], 
                           data = data, 
                           airflow_timestamp = airflow_timestamp, 
                           format = config['pandas_data_save_format'],
                            )
