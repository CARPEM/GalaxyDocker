#My Global var definition
##########################
#URL PROTON
##########################
sequencer_base_url='http://your.proton.fr/rundb/api/v1'
sequencer_root_base_url='http://your.proton.fr'
sequencer_user="usserproton"
sequencer_password="protonpaswd"
sequencer_severName="protonadress"
sequencer_ExperimentLimit=2
##########################
#URL GALAXY
##########################
#galaxydev
galaxy_web_url='http://127.0.0.1:8123'
galaxy_base_url='webgalaxy'
apiKey="yourspecificmasterapikey"
http_proxy=""
https_proxy=""
#either an IP or a name to access the computer on the network 
analysisManagerAccessionAdress="127.0.0.1"
DEBUG_AnalysisManager=True
GALAXY_BRAND="HEGP"
##########################
#Nas Directory path
##########################
inputAbsolutPath="/nas_Dir/"
nasInput="/nas_Dir/INPUT/"
CNVfolderName="/CNV/"
plasmaFolderName="/bam/"
nasResults="/nas_Dir/RESULTS/"
nasBackupFolder="/nas_backup/"
workflowPath="/nas_Dir/workflow"
toolsInformation="/results/regate_tools/"
#toolsInformation="/nas_Dir/toolsInformation_20170123/"

##########################
#SMTP folder
##########################
smtpServerAphp='your.smtp.server'
smtpPortServer=25
fromAddrOfficial='yourofficial@email.com'

##########################
#DATABASE
##########################
POSTGRES_PASSWORD="postgres"
DB_redis="redisam"
DB_redis_port=6379
DB_server="amdatabase"
DB_port=5434
DB_Name="analysismanager"
DB_USER="analysismanageruser"
DB_password="analysismanager"

##########################
#REAL PATH
##########################
genomes_PATH="./nas_genomes"
registry_PATH="./nas_registry"
images_PATH="./images"
REALDATA_PATH="./data"
REALRESULTS_PATH="./test_data"
REALLOGS_PATH="./logs"
tools_default=["ucsc_table_direct1","CONVERTER_wiggle_to_interval_0","MAF_To_BED1","ratmine","lped2fpedconvert","mousemine","join1","cbi_rice_mart","ucsc_table_direct_archaea1","CONVERTER_interval_to_bed6_0","CONVERTER_interval_to_bigwig_0","wig_to_bigWig","MAF_To_Fasta1","metabolicmine","CONVERTER_maf_to_interval_0","Extract_features1","upload1","wc_gnu","pbed2ldindepconvert","CONVERTER_interval_to_bed12_0","random_lines1","modENCODEfly","gff_filter_by_attribute","gtf2bedgraph","ChangeCase","__EXPORT_HISTORY__","wiggle2simple1","GeneBed_Maf_Fasta2","CONVERTER_len_to_linecount","trimmer","createInterval","gff_filter_by_feature_count","Interval2Maf1","genomespace_exporter","Show tail1","barchart_gnuplot","microbial_import1","axt_to_concat_fasta","tabular_to_dbnsfp","Interval2Maf_pairwise1","CONVERTER_interval_to_bedstrict_0","CONVERTER_gff_to_bed_0","maf_by_block_number1","modmine","CONVERTER_gff_to_fli_0","flymine","MAF_Thread_For_Species1","CONVERTER_fasta_to_len","pbed2lpedconvert","vcf_to_maf_customtrack1","__SET_METADATA__","__IMPORT_HISTORY__","biomart","Sff_extractor","CONVERTER_bed_to_fli_0","secure_hash_message_digest","CONVERTER_fasta_to_bowtie_base_index","ebi_sra_main","MAF_Reverse_Complement_1","mergeCols1","gff2bed1","Grouping1","CONVERTER_maf_to_fasta_0","maf_limit_size1","sort1","Convert characters1","MAF_To_Interval1","CONVERTER_fasta_to_bowtie_color_index","genomespace_file_browser_prod","lped2pbedconvert","MAF_filter","CONVERTER_fasta_to_2bit","CONVERTER_fasta_to_tabular","gene2exon1","Cut1","Count1","MAF_Limit_To_Species1","ucsc_table_direct_test1","wormbase","maf_stats1","zebrafishmine","Filter1","Paste1","Interval_Maf_Merged_Fasta2","modENCODEworm","gtf_filter_by_attribute_values_list","Summary_Statistics1","qual_stats_boxplot","cat1","axt_to_lav_1","Grep1","eupathdb","lav_to_bed1","comp1","bed_to_bigBed","liftOver1","bed2gff1","gramenemart","hbvar","CONVERTER_interval_to_bed_0","yeastmine","Show beginning1","CONVERTER_sam_to_bam","wormbase_test","CONVERTER_picard_interval_list_to_bed6","Extract genomic DNA 1","Remove beginning1","flymine_test","CONVERTER_bed_to_gff_0","axt_to_fasta","addValue","MAF_split_blocks_by_species1"]
