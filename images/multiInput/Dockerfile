FROM biocontainers/samtools:1.3.1

ENV tool_Description='calculate read depth for a set of genomic intervals'
ENV tool_Version='2.0'
ENV tool_ID='samtools_bedcov'
ENV tool_Name='BedCov'
ENV stdio='1:'

#INPUT1
ENV input_1_format='bed'
ENV input_1_name='input_bed'
ENV input_1_label='BED file'
#INPUT2
ENV input_2_format='bam'
ENV input_2_name='input_bams'
ENV input_2_label='BAM file'
#OUTPUT

ENV output_name='output'
ENV output_format='tabular'
ENV output_label='${tool.name} on ${on_string}'
ENV exec_command='<![CDATA[ \n\
        for bamfile in  \n\
        #for dataset in $input_bams: \n\
            "${dataset}" \n\
        #end for \n\
        ; do \n\
            if [ ! -f \$bamfile.bai ] ; then \n\
                ln -s \$bamfile && samtools index `basename \$bamfile` ; \n\
            else \n\
                ln -s \$bamfile && ln -s \$bamfile.bai ; \n\
            fi ; \n\
        done ; \n\
        samtools bedcov "${input_bed}" \n\
        #for dataset in $input_bams: \n\
            `basename "${dataset}"` \n\
        #end for \n\
        > "${output}" \n\
        ]]>'

