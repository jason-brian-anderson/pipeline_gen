from datetime import timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
import docker
from docker.types import Mount
import yaml

'''
to do:
1. turn off docker build task
2. ensure can run with pre-existing dockeroperator_deploy_image:latest
3. be able to build that form command line
4. move and rename Dockeroperators to root dir

'''


config_file = "/opt/airflow/dags/pytorch_pipeline/config.yaml"
with open(config_file, "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)



def pipeline_operator(task_id, container_name, command,):

    return DockerOperator(
    task_id=task_id,
    api_version='auto',
    container_name = container_name,
    image=config['pipeline_image'],
    command = command,
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
    device_requests=[docker.types.DeviceRequest(count=-1, capabilities=[['gpu']]),],
    network_mode='bridge',
    dag=dag,
)

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


# pytorch_build = BashOperator(
#     task_id='build_docker_image_for_training',
#     bash_command=f"docker build -t {config['training_image']} {config['dockerfile_dir']}",
#     dag=dag,
# )

# pytorch_task = DockerOperator(
#     task_id='verify_cuda',
#     api_version='auto',
#     container_name = 'trainer',
#     image=config['pipeline_image'],
#     command = f"python {config['container_path']}/{config['training_executable']}",
#     mounts=[
#         Mount(source=config['host_path'], 
#               target=config['container_path'], 
#               type="bind",
#               ),
#             ],
#     auto_remove=True,
#     user='root',
#     privileged = True,
#     docker_url='unix://var/run/docker.sock',
#     device_requests=[docker.types.DeviceRequest(count=-1, capabilities=[['gpu']]),],
#     network_mode='bridge',
#     dag=dag,
# )
cuda_test = pipeline_operator(
        task_id='cuda_test',
        container_name = 'cuda_test',
        command = f"python {config['container_path']}/{config['cuda_test']}",
)


harvest_data = pipeline_operator(
        task_id='harvest_data',
        container_name = 'harvest_data',
        command = f"python {config['container_path']}/{config['harvest_data']}",
)

transform_data = pipeline_operator(
        task_id='transform_data',
        container_name = 'transform_data',
        command = f"python {config['container_path']}/{config['transform_data']}",
)

train_model = pipeline_operator(
        task_id='train_model',
        container_name = 'train_model',
        command = f"python {config['container_path']}/{config['train_model']}",
)

deploy_model = pipeline_operator(
        task_id='deploy_model',
        container_name = 'deploy_model',
        command = f"python {config['container_path']}/{config['deploy_model']}",
)

#start >> pytorch_build >> pytorch_task >> stop
start >>  cuda_test >> harvest_data >> transform_data >> train_model >> deploy_model >> stop