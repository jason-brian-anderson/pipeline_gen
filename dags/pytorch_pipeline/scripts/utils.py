import os
import yaml
import pandas as pd
    


def get_config(config_file = "/tmp/config.yaml"):
    with open(config_file, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

def _create_data_directory(mnt_dir, airflow_timestamp):
    directory_name = os.path.join(mnt_dir,airflow_timestamp,)
    if not os.path.exists(directory_name):
        print(f"path {directory_name} does not exist, creating it")
        os.makedirs(directory_name)
    return directory_name

def persist_data_to_disk(filename, data, airflow_timestamp):
    config = get_config()
    format = config['pandas_data_save_format']
    directory_name = _create_data_directory(config['container_data_path'], airflow_timestamp)

    if format == 'csv':
            data_file = os.path.join(directory_name,filename)
            data.to_csv(data_file,index = False)
            print(f"wrote {data_file} to disk")
    else:
            raise "format not implemented"


def read_data_from_disk(filename,airflow_timestamp):
    config = get_config()
    format = config['pandas_data_save_format']
    directory_name = _create_data_directory(config['container_data_path'], airflow_timestamp)

    if format == 'csv':
            data_file = os.path.join(directory_name,filename)
            data = pd.read_csv(data_file)
            print(f"read {data_file} from disk")
    else:
            raise "format not implemented"
    return data