#!/bin/sh

# Upgrade apt-get
apt-get update && apt-get upgrade

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

# Install python requirements
pip3 install virtualenv

# Create new VENV (if not found) & activate
cd /root/install || return
if [ ! -f "./.venv" ]; then
  virtualenv .venv
fi
. .venv/bin/activate

# Install library requirements
.venv/bin/pip install -r requirements.txt
