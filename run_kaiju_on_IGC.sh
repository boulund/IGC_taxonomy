#!/bin/bash
# Run Kaiju to annotate taxonomy for IGC genes 
# Fredrik Boulund 2017

# Unofficial bash strict mode
set -euo pipefail
IFS=$'\n\t'

# Run Kaiju on IGC
igc=/home/ctmr/db/IGC/IGC_stripped_headers.fa

kaiju \
	-t /home/ctmr/db/kaiju/latest/nodes.dmp \
	-f /home/ctmr/db/kaiju/latest/kaiju_db.fmi \
	-o IGC.kaiju \
	-z 35 \
	-i $igc \

# Produce taxonomy lineage output from Kaiju output using BBTools taxonomy.sh
# Run custom Python script to reformat into tab separated columns
./parse_taxonomy_lineages.py IGC.kaiju.linages > IGC.assignments.tab
