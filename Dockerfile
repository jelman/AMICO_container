FROM python:3


RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    libblas-dev \
    liblapack-dev \
    software-properties-common \
    build-essential 



  WORKDIR /opt
  
  COPY . .
  
  # Install require AMICO and requirements
  RUN pip install dmri-amico


  WORKDIR /opt
 

  ENTRYPOINT ["python", "run_amico.py"]
