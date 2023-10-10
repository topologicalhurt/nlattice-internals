#!/usr/bin/env bash
var conf = require('./config.json');

if [ -z conf.Meta.ContainerId ]
then
    conf.Meta.ContainerId = docker run -it -d pymesh/pymesh;
fi

var CONTAINER_ID = conf.Meta.ContainerId;
docker cp install.tar "$($CONTAINER_ID):/root/";
docker exec -i $CONTAINER_ID /bin/bash -c \
"tar -xf install.tar; rm install.tar; cd install; ./install.sh $1 $2";