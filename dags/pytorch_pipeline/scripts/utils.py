import os
import yaml
    


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


def xxxpipeline_operator(config, task_id, container_name, command, dag):
    return DockerOperator(
    task_id=task_id,
    api_version='auto',
    container_name = container_name,
    image=config['pipeline_image'],
    command = command,
    mounts=[
        Mount(source=config['host_code_path'], 
              target=config['container_code_path'], 
              type="bind",
              ),
        Mount(source=config['host_data_path'], 
              target=config['container_data_path'], 
              type="bind",
              ),
        Mount(source=config['host_config_path'], 
              target=config['container_config_path'], 
              type="bind",
              ),
            ],
    auto_remove=True,
    user='root',
    privileged = True,
    docker_url='unix://var/run/docker.sock',
    device_requests=[docker.types.DeviceRequest(count=-1, capabilities=[['gpu']]),],
    network_mode='bridge',
    dag=dag,
)
