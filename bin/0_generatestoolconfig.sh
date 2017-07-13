#!/bin/bash

cd ../images/inspectTest/
sh build_image.sh
cd ../multiInput/
sh build_image.sh
cd ../../dockertools2galaxy/
python dockertools2galaxy.py -i ../images/inspectTest/inspect_samtools_idxstats.txt -o ../tools/samtools_docker/samtools_idxstats/samtools_idxstats.xml
python dockertools2galaxy.py -i ../images/multiInput/inspect_samtools_bedcov.txt -o ../tools/samtools_docker/samtools_bedcov/samtools_bedcov.xml

