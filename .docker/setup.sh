#!/bin/bash

function setup_container() {
    local os=$1
    local dockerfile=".docker/os/${os}.Dockerfile"
    local container_name="games-tui-testenv-${os}"

    if [ -f $dockerfile ]; then
        echo "Building docker container for ${os}"
        docker build -t "$container_name" -f $dockerfile .
        echo "Running docker container for ${os}..."
        docker run -it --rm --name "$container_name" "$container_name" 
    else
        echo "Invalid OS: ${os}. Dockerfile does not exist."
        exit 1
    fi
}


function destroy() {
    echo "Destroying any containers with 'games-tui' in the name..."
    docker ps --filter "name=games-tui" --quiet | xargs -r docker stop
    docker ps -a --filter "name=games-tui" --quiet | xargs -r docker rm -f
    echo "Destroyed all 'games-tui' containers."
}


case $1 in
    "setup")
        setup_container $2
        ;;
    "destroy")
        destroy
        ;;
    *)
        echo "No Args??"
        ;;
esac
