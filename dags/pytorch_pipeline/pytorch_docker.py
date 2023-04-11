from datetime import timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
import docker
from docker.types import Mount
import yaml

config_file = "/opt/airflow/dags/pytorch_pipeline/config.yaml"
with open(config_file, "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(1),
    
}

dag = DAG(
    'pytorch_training_pipeline',
    default_args=default_args,
    description='PyTorch container with DockerOperator',
    schedule_interval=timedelta(minutes=5),
    catchup=False,
)

start = DummyOperator(
    task_id='start_pipeline',
    dag=dag,
)

stop = DummyOperator(
    task_id='stpp_pipeline',
    dag=dag,
)

pytorch_build = BashOperator(
    task_id='build_docker_image_for_training',
    bash_command=f"docker build -t {config['training_image']} {config['dockerfile_dir']}",
    dag=dag,
)

pytorch_task = DockerOperator(
    task_id='run_pytorch_training_from_docker',
    api_version='auto',
    container_name = 'trainer',
    image=config['training_image'],
    command = f"python {config['container_path']}/{config['training_executable']}",
    mounts=[
        Mount(source=config['host_path'], 
              target=config['container_path'], 
              type="bind",
              ),
            ],
    auto_remove=True,
    user='root',
    privileged = True,
    docker_url='unix://var/run/docker.sock',
    mount_tmp_dir=False, 
    device_requests=[
    docker.types.DeviceRequest(count=-1, capabilities=[['gpu']]),],
    network_mode='bridge',
    dag=dag,
)
start >> pytorch_build >> pytorch_task >> stop