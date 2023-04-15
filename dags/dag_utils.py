from datetime import timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
import docker
from docker.types import Mount
import yaml


def get_config(config_file):
    with open(config_file, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

def pipeline_operator(config_file, task_id, container_name, command, dag,):
    config = get_config(config_file)
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