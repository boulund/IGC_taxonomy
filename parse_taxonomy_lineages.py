#!/usr/bin/env python3.6
# Parse taxonomy lineages from BBMap taxonomy.sh output
# Fredrik Boulund 2017

from sys import argv, exit, stderr
from collections import namedtuple, deque
from functools import partial
import subprocess
import shlex
import argparse
from multiprocessing import Pool


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("KAIJU",
        help="Taxonomy.sh output file (redirected to file from stdout).")
    parser.add_argument("-t", "--taxtree", metavar="FILE",
        default="/home/ctmr/db/bbmap_taxonomy/tree.taxtree.gz",
        help="Path to BBMap taxtree [%(default)s]")

    if len(argv) < 2:
        parser.print_help()
        exit(1)
    return parser.parse_args()


def run_taxonomy(kaiju_line, taxtree=None):
    classified, query_name, tax_assignment = kaiju_line.strip().split()
    if classified == "C":
        taxonomy_cmd = shlex.split("taxonomy.sh threads=5 tree={} {}".format(taxtree, tax_assignment))
        p = subprocess.run(taxonomy_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if p.returncode == 0:
            return query_name, {k: v for k, v in parse_record_stdout(p.stdout.decode("UTF-8"))}
        else:
            print("ERROR", kaiju_line, p, file=stderr)
            return query_name, {"ERROR": "-"}
    else:
        return query_name, {}
    

def parse_record_stdout(lines):
    lines = deque(lines.split("\n")[1:])
    assigned_taxid = lines.popleft().split(":")
    if len(assigned_taxid) != 2:
        print("ERROR!", assigned_taxid)
        exit(2)
    line = lines.popleft()
    while line:
        try:
            level, level_taxid, description = line.split("\t")
            yield level, description
        except ValueError:
            if line.startswith("Could not find node."):
                yield "ERROR", "ERROR"
            else:
                print("ERROR")
                exit(3)
        line = lines.popleft()


def main(kaiju_file, taxtree):
    
    run_tax = partial(run_taxonomy, taxtree=taxtree)

    pool = Pool(20)
    with open(kaiju_file) as f:
        print("sequence\tsuperkingdom\tphylum\tclass\torder\tfamily\tgenus\tspecies\tsubspecies")
        for lineage in pool.imap_unordered(run_tax, f):
            print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                    lineage[0],
                    lineage[1].get("superkingdom", ""),
                    lineage[1].get("phylum", ""),
                    lineage[1].get("class", ""),
                    lineage[1].get("order", ""),
                    lineage[1].get("family", ""),
                    lineage[1].get("genus", ""),
                    lineage[1].get("species", ""),
                    lineage[1].get("subspecies", ""),
                    ))


if __name__ == "__main__":
    options = parse_args()
    main(options.KAIJU, options.taxtree)

