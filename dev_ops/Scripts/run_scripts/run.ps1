docker run -it -v $PSScriptRoot/../../../:/nlattice -p 8501:8501 --rm nlattice:v1.0 /bin/bash -c `
". /nlattice/dev_ops/Scripts/on_run.sh; /bin/bash"