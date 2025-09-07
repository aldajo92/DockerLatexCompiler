#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "$0")"; cd ..; pwd)"
source ${PROJECT_ROOT}/config_docker.sh

# Check if article parameter is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <article_directory>"
    echo "Example: $0 article"
    echo "This will compile the LaTeX files in ws_latex/<article_directory>/"
    exit 1
fi

ARTICLE_DIR="$1"

# Check if the article directory exists
if [ ! -d "${PROJECT_ROOT}/ws_latex/${ARTICLE_DIR}" ]; then
    echo "Error: Directory 'ws_latex/${ARTICLE_DIR}' does not exist"
    exit 1
fi

echo "🚀 Compiling LaTeX files in ws_latex/${ARTICLE_DIR}/"

docker run --rm \
    --volume ${PROJECT_ROOT}/ws_latex:/home/dockeruser/ws_latex \
    --network ${DOCKER_NETWORK} \
    --dns=8.8.8.8 \
    ${DOCKER_IMAGE_NAME} \
    "${ARTICLE_DIR}"