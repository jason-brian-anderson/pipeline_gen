from datetime import datetime, timedelta
from airflow import DAG
#from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.docker_operator import DockerOperator
import docker

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'gpu_dag',
    default_args=default_args,
    description='DAG to run GPU-based tasks',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 4, 6),
    catchup=False
)
gpu_task = DockerOperator(
    task_id='gpu_task',
    #image='pytorch/pytorch',
    #image='nvidia/cuda:10.2-base',
    image="nvidia/cuda:11.4.0-cudnn8-runtime-ubuntu20.04",
    command="nvidia-smi",
    device_requests=[
    docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])
],
    #docker_url='tcp://localhost:2375',  # or 'unix://var/run/docker.sock' for WSL 2
    #docker_url=  'unix://var/run/docker.sock', 
    #network_mode='bridge',
    # environment={
    #     'NVIDIA_VISIBLE_DEVICES': 'all',
    #     #'NVIDIA_DRIVER_CAPABILITIES': 'compute,utility',
    #     #'NVIDIA_REQUIRE_CUDA': 'cuda>=10.1'
    # },
    #docker_api_version='auto',
    dag=dag
)




