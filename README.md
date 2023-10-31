# nlattice-internals

## Project integration

```
├── README.md
├── config
│   └── config.json
├── dev_ops
│   ├── Deprecated
│   ├── Dockerfile
│   ├── Scripts
│   ├── build.sh
│   └── requirements.txt
├── main.py
├── out
│   └── point_cloud.stl
├── python
│   ├── frontend
│   └── pc
└── source
    ├── test_model.stl
    └── test_model2.stl
```

- config: configs storing project meta information in here. I.e. anytime you need to fetch information or metadata it belongs here.
- dev_ops: developer operation folder.
  - Deprecated: contains old build scripts (still useful if you want to minimise build times.)
  - Dockerfile: dockerfile (modify if you want to change the target image or other docker RUN commands.)
  - Scripts: contains the scripts used in the docker install and as entrypoints
  - build.sh: builds the docker for ARM64 / m1 macs or for general linux
  - requirements.txt: **Add any dependencies that you need into here**
    - ***Tip***: A .venv was installed at root so that you can keep track of dependencies ```~/.venv/bin/activate && pip freeze > requirements.txt && deactivate``` to generate a new requirements     list. Keep in mind that you'll need to deactivate the virtual environment to use pymesh however.
- main.py: follow from here for the code pipeline
- out: this is where all the cached or saved models will go when you wrap them with the context handler made for saving files
- python: **!All code is to go in here!**
    - pc: point cloud folder (the tesselation approach topologicalhurt / myself is using
    - frontend: gui, streamlit stuff lives in here
- source: any common resources go in here.
    - ***Tip***: In python -> pc modify consts.py to add new object references or directories

## How to run 

clone the repository
```
git clone https://github.com/topologicalhurt/nlattice-internals.git
```

To run the program do the following **You will first have to build the docker if you haven't done so already!**

### Building the docker

***On linux***
```
cd dev_ops
chmod +x build.sh
./build.sh
```

***On windows***
```
cd dev_ops
docker build -t nlattice:v1.0 .
```

This builds from the dockerfile. The dockerfile builds an image using a forked/patched version of the now obsolete pymesh library.

### Run the docker container

***On windows*** 
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
./dev_ops/Scripts/run_scripts/run.ps1
```

***On linux***
```
chmod +x ./dev_ops/Scripts/run_scripts/run.sh
./dev_ops/Scripts/run_scripts/run.sh
```

On repeated runs omit the file access modifier commands of course (just run ```./dev_ops/Scripts/run_scripts/run.ps1```, ```./dev_ops/Scripts/run_scripts/run.sh```)

### Starting the UI

And then in the root terminal (where the prior commands were just run):

***Streamlit***
```
python main.py -ui streamlit
```
and navigate to **localhost:8501** for the web view.

***Dash***
```
python main.py -ui dash
```
and navigate to **localhost:8050** for the web view.

***No gui (CLI mode)***
```
python main.py --no-gui
```

Please run:
```
python main.py --help
```
for more commands

