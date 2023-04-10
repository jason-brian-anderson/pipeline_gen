FROM apache/airflow:2.5.3 

ADD requirements.txt . 
RUN pip install -r requirements.txt

#USER root
#RUN apt update && apt upgrade -y
#USER AIRFLOW