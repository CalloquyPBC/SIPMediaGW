#!/bin/bash
sudo systemctl stop sipmediagw.service
docker kill gw0
IMAGE=$(docker images | grep calloquy | awk '{print $3}')
docker rmi $IMAGE -f
docker pull calloquy/sipmediagw
sudo systemctl start sipmediagw.service
