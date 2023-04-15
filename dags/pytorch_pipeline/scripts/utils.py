import os
import yaml


def get_config(config_file):
    with open(config_file, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

def hello(x):
    print(f"hello {x}..................................")



def _create_data_directory(mnt_dir, airflow_timestamp):
    directory_name = os.path.join(mnt_dir,airflow_timestamp,)
    if not os.path.exists(directory_name):
        print(f"path {directory_name} does not exist, creating it")
        os.makedirs(directory_name)
    return directory_name


def persist_data_to_disk(mnt_dir, filename, data, airflow_timestamp, format = 'csv'):
    directory_name = _create_data_directory(mnt_dir, airflow_timestamp)

    if format == 'csv':
            data_file = os.path.join(directory_name,filename)
            data.to_csv(data_file,index = False)
            print(f"wrote {data_file} to disk")

    else:
            raise "format not implemented"
