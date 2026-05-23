:: set docker settings
SET DOCKER_USER=oislen
SET DOCKER_REPO=agenticnewsletter
SET DOCKER_TAG=latest
SET DOCKER_IMAGE=%DOCKER_USER%/%DOCKER_REPO%:%DOCKER_TAG%
SET DOCKER_CONTAINER_NAME=anl

:: remove existing docker containers and images
docker image rm -f %DOCKER_IMAGE%

:: build docker image
call docker build --no-cache -t %DOCKER_IMAGE% .

:: run docker container
:: SET UBUNTU_DIR=/home/ubuntu
:: call docker run --name %DOCKER_CONTAINER_NAME% %DOCKER_IMAGE%
:: call docker run --name %DOCKER_CONTAINER_NAME%w --memory 7GB --volume E:\GitHub\RandomTelecomPayments\data:/home/ubuntu/RandomTelecomPayments/data --rm %DOCKER_IMAGE%  --n_users 13000 --use_random_seed 1 --n_itr 2
:: call docker run -it --entrypoint bash --name %DOCKER_CONTAINER_NAME% --memory 7GB --volume E:\GitHub\RandomTelecomPayments\data:/home/ubuntu/RandomTelecomPayments/data --rm %DOCKER_IMAGE%
:: call docker run --name %DOCKER_CONTAINER_NAME% --publish 8000:8000 --memory 7GB --entrypoint fastapi --rm %DOCKER_IMAGE% run generator/api.py
:: docker run --name anl --rm oislen/agenticnewsletter:latest

:: useful docker commands
:: docker images
:: docker ps -a
:: docker exec -it {container_hash} /bin/bash
:: docker stop {container_hash}
:: docker start -ai {container_hash}
:: docker rm {container_hash}
:: docker image rm {docker_image}
:: docker push {docker_image}