FROM pytorch/pytorch


RUN apt-get update && \
    apt-get upgrade -y



ADD requirements.txt . 
RUN pip install -r requirements.txt