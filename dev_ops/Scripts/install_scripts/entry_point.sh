#!/bin/sh

# Upgrade apt-get
# apt-get update && apt-get upgrade


#PY_V=$(python -V 2>&1)
## Compile python3.11.3
#if [ "$PY_V" != "Python 3.11.3" ]; then
#  cd /tmp || return
#  wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz
#  tar xzf Python-3.11.3.tgz
#  cd Python-3.11.3 || return
#  ./configure --enable-optimizations
#  make Scripts
#fi

if [[ $(uname -m) == 'arm64' ]]; then
  echo "Uninstalling watchdog to get arm64 support"
  pip uninstall watchdog
fi

# Install python requirements
pip3 install virtualenv

# Create new VENV (if not found)
if [ ! -f "/root/.venv" ]; then
  virtualenv /root/.venv
fi

# Install library requirements
#. /root/.venv/bin/activate
#/root/.venv/bin/pip install -r /tmp/requirements.txt
#deactivate

# Install as root user
pip install -r /tmp/requirements.txt
