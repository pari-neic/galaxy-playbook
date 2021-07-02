# Pre-requisites
# 1) seqkit executable for filtering fasta files
#    https://github.com/shenwei356/seqkit/releases/tag/v0.15.0
# 2) Download sars_covid19_X.X_assembly.fa file from
#    https://public.sfb.uit.no/SarsCovid19DB/versioned_genomes/
# 3) jq - commandline JSON processor
#
# 1) and 2) assumed available in parent folder
# 3) assumed installed using local package manager

# Tested
# - script tested in bash on Ubuntu 18.04LTS linux

# Manually set theses variables
###############################
# Set DB version and date before running script to extract
# sequences to named files per country
#
SARS_COV_2_DB_VERSION=2.8
DATE=23rd-June-2021
#
################################


# GAZ codes and names for PaRI partner countries
declare -a COUNTRY_NO=("00002937" "00002646" "00002729" "00002959" "00003297" "00005851")
declare -a COUNTRY_NAME=("Finland" "Germany" "Sweden" "Estonia" "Denmark" "Norway")

# Countries with zero ENA entries, GAZ codes found in
# https://archive.gramene.org/db/ontology/search?id=GAZ:00003606

#Norway 00005851 
#Denmark 00003297 


echo "Sars-CoV-2 DB version: ${SARS_COV_2_DB_VERSION}"
echo "Date of release: ${DATE}"


len=$(( ${#COUNTRY_NO[@]} - 1 ))

for i in $(seq 0 $len) 
do

    curl -L "https://databasesapi.sfb.uit.no/rpc/v1/SARS-CoV-2/graphs?ver=$SARS_COV_2_DB_VERSION&filter=${COUNTRY_NO[$i]}&sort=x&x%5Bid%5D=each" > saved.json

    jq -r '.[] | .[] | .x' saved.json | cut -d"_" -f3 > ID_list_${COUNTRY_NAME[$i]}.txt

    sample_count=`wc -l ID_list_${COUNTRY_NAME[$i]}.txt | cut -d" " -f1`
    
    echo "Sample count for ${COUNTRY_NAME[$i]}: ${sample_count}"
    
    ../seqkit grep -nr -f ID_list_${COUNTRY_NAME[$i]}.txt ../sars_covid19_${SARS_COV_2_DB_VERSION}_assembly.fa > ${COUNTRY_NAME[$i]}-${sample_count}-samples2-${DATE}-v${SARS_COV_2_DB_VERSION}.fa


done

     
