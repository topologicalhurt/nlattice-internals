#!/bin/bash
SCRIPT_P=$(readlink -f "$0")
P=$(dirname "$SCRIPT_P")
# docker run -it -v "$P"/../../..:/nlattice -p 8501:8501 --rm nlattice:v1.0 /bin/bash -c\
#  ". /nlattice/dev_ops/Scripts/on_run.sh; /bin/bash"

docker run -it -v "$P"/../../..:/nlattice -p 8050:8050 --rm nlattice:v1.0 /bin/bash -c\
 ". /nlattice/dev_ops/Scripts/on_run.sh; /bin/bash"
