from datetime import timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
import dag_utils as du

config_file = "/opt/airflow/dags/pipeline/config.yaml"
config = du.get_config(config_file)


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
    schedule_interval=timedelta(minutes=240),
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

cuda_test = du.pipeline_operator(
        config_file = config_file,
        task_id='cuda_test',
        container_name = 'cuda_test',
        command = f"python {config['container_code_path']}/{config['cuda_test']}",
        dag = dag,
        )

harvest_data = du.pipeline_operator(
        config_file = config_file,
        task_id='harvest_data',
        container_name = 'harvest_data',
        command = f"python {config['container_code_path']}/{config['harvest_data']}  {{{{ ts }}}}",
        dag = dag,
        )

transform_data = du.pipeline_operator(
        config_file = config_file,
        task_id='transform_data',
        container_name = 'transform_data',
        command = f"python {config['container_code_path']}/{config['transform_data']}  {{{{ ts }}}}",
        dag = dag,
        )

train_model = du.pipeline_operator(
        config_file = config_file,
        task_id='train_model',
        container_name = 'train_model',
        command = f"python {config['container_code_path']}/{config['train_model']}  {{{{ ts }}}}",
        dag = dag,
        )

deploy_model = du.pipeline_operator(
        config_file = config_file,
        task_id='deploy_model',
        container_name = 'deploy_model',
        command = f"python {config['container_code_path']}/{config['deploy_model']}  {{{{ ts }}}}",
        dag = dag,
        )

start >>  cuda_test >> harvest_data >> transform_data >> train_model >> deploy_model >> stop