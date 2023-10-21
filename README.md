# nlattice-internals

To run the program do the following:

On windows:
```
./dev_ops/Scripts/run_scripts/run.ps1
```

On linux:
```
. /dev_ops/Scripts/run_scripts/run.sh
```

And then in the root terminal (where the prior commands were just run):
```
streamlit run main.py
```
and navigate to **localhost:8501** for the web view.

## Building the docker

```
cd dev_ops
docker build . -t nlattice:v1.0
```

This builds from the dockerfile. The dockerfile builds an image using a forked/patched version of the now obsolete pymesh library.
