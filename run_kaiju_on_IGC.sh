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
	-i $igc 

addTaxonNames \
	-t /home/ctmr/db/kaiju/latest/nodes.dmp \
	-n /home/ctmr/db/kaiju/latest/names.dmp \
	-i IGC.kaiju \
	-p \
	-o IGC.kaiju.lineage 
