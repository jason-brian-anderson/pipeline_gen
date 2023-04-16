import sys
import pandas as pd
import utils

config = utils.get_config('/tmp/config.yaml')
airflow_timestamp = sys.argv[1]
dest_file = config['raw_data_file']


#harvest data from source
data = pd.DataFrame({'a':[1.0,2.0,3.0], 
                     'b':[4.0,5.0,6.0], 
                     'c':[7.0,8.0,9.0],
                     })

utils.persist_data_to_disk(filename = dest_file, 
                           data = data, 
                           airflow_timestamp = airflow_timestamp, 
                           )
