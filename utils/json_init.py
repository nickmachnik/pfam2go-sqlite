import os
import json
from . import parsing
from collections import defaultdict


def create_uniprot_go_mapping(pfam2go_path, pfam_a_path, outdir):
    # pfam -> go
    pfam2go = defaultdict(set)
    for entry in parsing.parse_pfam2go(pfam2go_path):
        pfam2go[entry.pfam_accession].add(entry.go_id)

    # (uniprot accession, position in protein) -> {goterms}
    uniprot2go = {}
    uniprot2pfam = {}
    for entry in parsing.parse_pfam_A_fasta(pfam_a_path):
        uniprot2pfam[(entry.uniprot_accession, entry.location)] = (
            entry.pfam_accession)
        if entry.pfam_accession not in pfam2go:
            continue
        uniprot2go[(entry.uniprot_accession, entry.location)] = (
            pfam2go[entry.pfam_accession])

    # write mappings to json
    json.dump(pfam2go, os.path.join(outdir, "pfam2go.json"))
    json.dump(uniprot2go, os.path.join(outdir, "uniprot2go.json"))
    json.dump(uniprot2pfam, os.path.join(outdir, "uniprot2pfam.json"))
