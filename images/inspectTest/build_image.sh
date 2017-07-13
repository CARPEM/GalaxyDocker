docker build -t samtools_idxstats .
docker inspect samtools_idxstats >  inspect_samtools_idxstats.txt
docker save -o  samtools_idxstats.tar samtools_idxstats

