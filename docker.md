# Docker

## Command Reference
- `docker build -t <image_name> .` - From a directory with a Dockerfile, build an image with the given name
- `docker build -t <image_name> -f <dockerfile> .` - Same, but with a custom Dockerfile path
- `docker build --no-cache -t <image_name> .` - Same, but redo all cached build steps
- `docker ps` - See currently running containers
- `docker ps -a` - See all containers
- `docker attach <container_id>` - Reattach to a running container
- `docker commit <container_id> <image_name>` - Commit the state of a container to a new image
- `docker stop <container_id>` - Stop a running container
- `docker start <container_id>` - Restart a stopped container
- `docker cp <path/on/host> <container_id>:<path/in/container>` - Copy files between host and container
- `docker volume create <volume_name>` - Create a new volume
- `docker volume ls` - List volumes
- `docker run -it <image_name>` -  Start a container in TTY interactive mode
- `docker run --rm ...` - auto-remove the container when it exits
- `docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=docker.for.mac.host.internal:0 <image_name>` - Start a container while making XQuartz available to it
- `docker run -it -v <volume_name>:<path/in/container> <image_name>` - Start a container with a volume attached
- `docker run -it -v <path/in/container> <image_name>` - Start a container with a new, unnamed volume
- `docker run -it -v <path/on/host>:<path/in/container> <image_name>` - Start a container with a host directory mounted
- `docker container prune` - remove stopped containers
- `docker rm <container>` - delete a container