FROM wdcarpem/samtools

ENV input_format='bam'
ENV input_name='input'
ENV input_label='BAM file'
ENV output_name='output'
ENV output_format='tabular'
ENV output_label='${tool.name} on ${on_string}'
ENV exec_command='<![CDATA[ \n\
if [ ! -f "${input}.bai" ] ; then \n\
    ln -s "${input}" input.bam ; \n\
    samtools sort -o sorted.bam -O bam -T sts "${input}" ; \n\
    samtools index sorted.bam ; \n\
    samtools idxstats sorted.bam > "${output}" ; \n\
else \n\
    samtools idxstats "${input}" > "${output}" ; \n\
fi]]>'
ENV tool_Description='tabulate mapping statistics for BAM dataset'
ENV tool_Version='2.0'
ENV tool_ID='samtools_idxstats'
ENV tool_Name='IdxStats'
ENV stdio='1:'

