#!/bin/bash
docker build . -f ./containers/Dockerfile.tests -t bbox_visualizer:latest --rm