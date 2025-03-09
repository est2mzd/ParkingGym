#!/bin/bash

source ./common.sh

docker run \
    --gpus all \
    --net=host \
    -itd \
    --shm-size=8G \
    --user $USER_NAME:$USER_NAME \
    --user $USER_ID:$USER_GID \
    --name $CONTAINER_NAME \
    -v ${PARENT_DIR}/src/:/home/${USER_NAME}/src \
    $IMAGE_NAME

#     -v ${PARENT_DIR}/PythonRobotics:/home/${USER_NAME}/PythonRobotics \