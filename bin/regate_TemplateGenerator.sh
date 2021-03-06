#!/bin/sh
#WDN
#define parameters which are passed in.
galaxy_base_url=$1
apiKey=$2
fromAddrOfficial=$3
toolsInformationVariable=$4
#define the template.
cat  << EOF


[galaxy_server]
# url to the analyze galaxy instance with api
galaxy_url_api =$galaxy_base_url
# galaxy instance url usable from a web browser
galaxy_url =$galaxy_base_url
# galaxy user api key
api_key =$apiKey
# default tool list in galaxy, this list of tools will not be taken into account for the push process
tools_default = ucsc_table_direct1,CONVERTER_wiggle_to_interval_0,MAF_To_BED1,ratmine,lped2fpedconvert,mousemine,join1,cbi_rice_mart,ucsc_table_direct_archaea1,CONVERTER_interval_to_bed6_0,CONVERTER_interval_to_bigwig_0,wig_to_bigWig,MAF_To_Fasta1,metabolicmine,CONVERTER_maf_to_interval_0,Extract_features1,upload1,wc_gnu,pbed2ldindepconvert,CONVERTER_interval_to_bed12_0,random_lines1,modENCODEfly,gff_filter_by_attribute,gtf2bedgraph,ChangeCase,__EXPORT_HISTORY__,wiggle2simple1,GeneBed_Maf_Fasta2,CONVERTER_len_to_linecount,trimmer,createInterval,gff_filter_by_feature_count,Interval2Maf1,genomespace_exporter,Show tail1,barchart_gnuplot,microbial_import1,axt_to_concat_fasta,tabular_to_dbnsfp,Interval2Maf_pairwise1,CONVERTER_interval_to_bedstrict_0,CONVERTER_gff_to_bed_0,maf_by_block_number1,modmine,CONVERTER_gff_to_fli_0,flymine,MAF_Thread_For_Species1,CONVERTER_fasta_to_len,pbed2lpedconvert,vcf_to_maf_customtrack1,__SET_METADATA__,__IMPORT_HISTORY__,biomart,Sff_extractor,CONVERTER_bed_to_fli_0,secure_hash_message_digest,CONVERTER_fasta_to_bowtie_base_index,ebi_sra_main,MAF_Reverse_Complement_1,mergeCols1,gff2bed1,Grouping1,CONVERTER_maf_to_fasta_0,maf_limit_size1,sort1,Convert characters1,MAF_To_Interval1,CONVERTER_fasta_to_bowtie_color_index,genomespace_file_browser_prod,lped2pbedconvert,MAF_filter,CONVERTER_fasta_to_2bit,CONVERTER_fasta_to_tabular,gene2exon1,Cut1,Count1,MAF_Limit_To_Species1,ucsc_table_direct_test1,wormbase,maf_stats1,zebrafishmine,Filter1,Paste1,Interval_Maf_Merged_Fasta2,modENCODEworm,gtf_filter_by_attribute_values_list,Summary_Statistics1,qual_stats_boxplot,cat1,axt_to_lav_1,Grep1,eupathdb,lav_to_bed1,comp1,bed_to_bigBed,liftOver1,bed2gff1,gramenemart,hbvar,CONVERTER_interval_to_bed_0,yeastmine,Show beginning1,CONVERTER_sam_to_bam,wormbase_test,CONVERTER_picard_interval_list_to_bed6,Extract genomic DNA 1,Remove beginning1,flymine_test,CONVERTER_bed_to_gff_0,axt_to_fasta,addValue,MAF_split_blocks_by_species1
# Contact Name
contactName = platformePRT
# Contact Email
contactEmail =$fromAddrOfficial
# Ressource Name
resourcename =toolsInformations 

[regate_specific_section]
# import all XML to ELIXIR bioregistry
pushtoelixir = False
# import all XML to ELIXIR bioregistry of an already exist specified directory
onlypush =False 
# bioregistry url
bioregistry_host = https://bio.tools 
# registry login required if pushtoelixir and onlypush are True
login = 
# Disable HTTPS verification warnings from urllib3
ssl_verify = False
# Specify if tools must be Open access or Restricted access when you will push them on the ELIXIR bioregistry
accessibility = Open access 
# directory to store the tool json
tool_dir =$toolsInformationVariable
# yaml file generated with remag.py
yaml_file = /home/ReGaTE/regate/data/yaml_mapping.yaml
#XML template for ELIXIR registry
#xmltemplate =
#XSD biotools
#xsdbiotools =
prefix_toolname =
suffix_toolname = 

[remag_specific_section]
# edam owl file to create
edam_file =
# output file format yaml
output_yaml =



EOF
