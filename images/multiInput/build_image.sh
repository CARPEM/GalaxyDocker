docker build -t samtools_bedcov .
docker inspect samtools_bedcov >  inspect_samtools_bedcov.txt
docker save -o  samtools_bedcov.tar samtools_bedcov

