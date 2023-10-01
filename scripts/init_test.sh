#!/bin/bash
bash ./scripts/build.sh
docker run  --name tests_bbox_visualizer --rm  bbox_visualizer:latest