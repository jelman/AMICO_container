#!/bin/bash
# Rebuild the docker and singularity containers

DockerTag=jaelman/amico
SingularityImage=amico.img
SingularityBootstrapFile=singularity.def

docker build --no-cache -t "$DockerTag":latest .
docker push "$DockerTag"

if [ ! -f "$SingularityImage" ]; then
  sudo singularity create --size 2000 "$SingularityImage"
fi

sudo singularity bootstrap "$SingularityImage" "$SingularityBootstrapFile"
