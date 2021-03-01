From python:3


RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    libblas-dev \
    liblapack-dev \
    software-properties-common \
    build-essential 



  WORKDIR /opt
  
  COPY . .
  
  # Install require AMICO and requirements
  RUN pip install --no-cache-dir -r requirements.txt
  RUN pip install dmri-amico
  
  # install Oracle JAVA
  WORKDIR /opt
  #RUN add-apt-repository ppa:webupd8team/java
  RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      default-jdk \
      default-jre

  # install camino
  ENV CAMINO_HEAP_SIZE=1800
  RUN git clone git://git.code.sf.net/p/camino/code camino
  WORKDIR /opt/camino
  RUN make
  ENV PATH=${PATH}:/opt/camino/bin
  
  WORKDIR /opt
 

  ENTRYPOINT ["python", "run_amico.py"]
