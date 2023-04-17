# pipeline_gen
[![Build Status](https://travis-ci.com/yourusername/airflow-orchestration-environment.svg?branch=main)](https://travis-ci.com/yourusername/airflow-orchestration-environment)
[![Docker Image](https://img.shields.io/docker/cloud/build/yourusername/airflow-orchestration-environment)](https://hub.docker.com/r/yourusername/airflow-orchestration-environment)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## TLDR
Avoid the regret of building Jupyter notebooks that end up in production,  build a simple data pipeline instead.

## Goals
* Ease the transition from exploratory data analysis to reliable model deployment and basic data pipeline orchestration
* Ease the transition from basic data pipeline orchestartion to an enterprise-grade Airflow orchestration

## Description
This GitHub project is a Git repo template to quickly spin up a Docker containerized Airflow orchestration environment. This of it as an 'opinionated' data pipeline template. 

## Audience
Those who need a semi-reliable data pipeline quickly.

## Design Principles
0. *Seprate the orchestration from the data processing* Airflow by default expects to run code on the Airflow python itself. It's better to perform all data processing on a docker image designed and built for that purpose.  Airflow's DockerOperator conveniently provides a great pairing of the orchestrator and the pipeline environment.
1. *Customize Sparingly* Do not add what is not critical to a basic data pipeline.  The code should deviate as little as possible from the most basic implementation of airflow
2. *Steer the user toward [good data pipelining practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html) such as atomicity and idemportency
3. *Keep the orchestrator out of the way* Airflow is an extremely powerful and flexible tool, but it can be daunting to new users who haven't considered the data engineering implications of data science deployemnt.
 4. *Make code development easy with Jupyter* The application spins up a [local Jupyter Environment](http://localhost:8888/) powered by the pipeline

## Motivation
It's not easy to extract, refine, and transform raw data into production ML models.  It's much worse to keep models updated as data evolves over time.  It is much easier to start with the pipeline orchestration in mind.  You don't want to be in a position of having to rerun a Jupyter notebook to refresh production ML models.

I'd love to know if you have a *better* way to train models with airflow that doesn't take this approach!


## What this project ** is not **
Airflow has a world of capability that is not used in this project.  It can be deployed much more reliably than what is offered here. We're literally using a small fraction of it's capabilities with this project.  Importantly, this is *by design*. This project represents the step *between* a simple Jupyter EDA and a high availability, high throughput enterprise datapipeline.


## Prerequisites

To use this template, you'll need:

- [Docker](https://www.docker.com/) installed on your system
- [Git](https://git-scm.com/) for cloning the repository

## Quick Start

1. **Clone the repository**

   ```
   git clone https://github.com/yourusername/airflow-orchestration-environment.git
   cd airflow-orchestration-environment
   ```

2. **Build the Docker image**

   ```
   docker build -t yourusername/airflow-orchestration-environment .
   ```

3. **Start the Airflow environment**

   ```
   docker-compose up -d
   ```

   This command will start the Airflow web server, scheduler, and all necessary components in separate containers.

4. **Access the Airflow web interface**

   Open your browser and navigate to `http://localhost:8080`. You should see the Airflow web interface with no pipelines.

## Usage

### Creating a New Data Pipeline

1. Create a new Python script in the `dags` folder following the naming convention `your_dag_name.py`.

2. Define your data pipeline using Airflow's [Directed Acyclic Graph (DAG)](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html) and [task](https://airflow.apache.org/docs/apache-airflow/stable/concepts/tasks.html) objects. For example:

   ```python
   from datetime import datetime, timedelta
   from airflow import DAG
   from airflow.operators.python_operator import PythonOperator

   def print_hello():
       print("Hello from your first task!")

   default_args = {
       "owner": "airflow",
       "depends_on_past": False,
       "email_on_failure": False,
       "email_on_retry": False,
       "retries": 1,
       "retry_delay": timedelta(minutes=5),
   }

   dag = DAG(
       "hello_world",
       default_args=default_args,
       description="A simple hello world DAG",
       schedule_interval=timedelta(days=1),
       start_date=datetime(2023, 4, 16),
       catchup=False,
   )

   t1 = PythonOperator(
       task_id="print_hello",
       python_callable=print_hello,
       dag=dag,
   )
   ```

3. Save the file, and the new pipeline will automatically appear in the Airflow web interface.

### Updating an Existing Data Pipeline

To update an existing pipeline, simply modify the corresponding Python script in the `dags` folder and save your changes. Airflow will automatically update the pipeline in the web interface.

## Contributing

We welcome contributions to improve this template. Please fork the repository, make your changes