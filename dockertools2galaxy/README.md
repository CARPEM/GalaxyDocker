#tool Information 
look at https://docs.galaxyproject.org/en/master/dev/schema.html
in order to have more information about tools 

ENV tool_Description='tool description'
ENV tool_Version='tool version'
ENV tool_ID='tool ID must be unique'
ENV tool_Name='tool name'
ENV stdio='how to handle alert' 

#In case you use only one input and one ouptut
ENV input_format='bam'
ENV input_name='input'
ENV input_label='BAM file'
ENV output_name='output'
ENV output_format='tabular'
ENV output_label='${tool.name} on ${on_string}'


#If multiple input or output
ENV input_1_format='bed'
ENV input_1_name='input_bed'
ENV input_1_label='BED file'
ENV output_1_name='output'
ENV output_1_format='tabular'
ENV output_1_label='${tool.name} on ${on_string}'

ENV exec_command='<![CDATA[ \n\
if [ ! -f "${input}.bai" ] ; then \n\
    ln -s "${input}" input.bam ; \n\
    samtools sort -o sorted.bam -O bam -T sts "${input}" ; \n\
    samtools index sorted.bam ; \n\
    samtools idxstats sorted.bam > "${output}" ; \n\
else \n\
    samtools idxstats "${input}" > "${output}" ; \n\
fi]]>'

NB: in this version we do not suport directly user custom parameter
