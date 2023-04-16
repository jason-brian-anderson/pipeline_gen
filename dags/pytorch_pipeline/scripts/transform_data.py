import sys
import pandas as pd
import utils
from sklearn.preprocessing import MinMaxScaler

config = utils.get_config('/tmp/config.yaml')
airflow_timestamp = sys.argv[1]
source_file = config['raw_data_file']
dest_file = config['transformed_data_file']

df = utils.read_data_from_disk(filename = source_file, 
                           airflow_timestamp = airflow_timestamp, 
                           )


#transform some data
df_normalized = pd.DataFrame(MinMaxScaler().fit_transform(df), columns=df.columns)


utils.persist_data_to_disk(filename = dest_file, 
                           data = df_normalized,
                           airflow_timestamp=airflow_timestamp,
                           )