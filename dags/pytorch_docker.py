from datetime import timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
import docker
from docker.types import Mount



default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(1),
}




dag = DAG(
    'pytorch_docker_dag',
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



image = "dockeroperator_deploy_image:latest"
dockerfile_dir = "/opt/airflow/dags/pytorch_pipeline"

pytorch_build = BashOperator(
    task_id='build_docker_image',
    bash_command=f'docker build -t {image} {dockerfile_dir}',
    dag=dag,
)

host_path = '/c/Users/kraut/Documents/My_Code/development_template_with_airflow/scripts'
#host_path = '/d/scripts'
container_path = '/tmp/scripts'

pytorch_task = DockerOperator(
    task_id='run_pytorch_container',
    api_version='auto',
    container_name = 'trainer',

    image=image,
    #image="nvidia/cuda:11.4.0-cudnn8-runtime-ubuntu20.04",
    #image='my_pytorch',

    command = f'/bin/bash -c "date;id;date;date;cd ~; echo xxxxxxxxxxxxxxxxxxxxxx;nvidia-smi;ls -latrs {container_path}; python {container_path}/run_this.py" ',
    
    mounts=[
        Mount(source=host_path, 
              target=container_path, 
              type="bind",
              ),
    ],
    auto_remove=True,
    user='root',
    privileged = True,
    docker_url='unix://var/run/docker.sock',
    mount_tmp_dir=False, 
    
    device_requests=[
    docker.types.DeviceRequest(count=-1, capabilities=[['gpu']]),
    ],
    network_mode='bridge',

    dag=dag,
)
#build_docker_image >> pytorch_task
start >> pytorch_build >> pytorch_task >> stop