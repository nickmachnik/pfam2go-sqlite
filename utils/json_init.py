import os
import json
from . import parsing
from collections import defaultdict


def create_uniprot_go_pfam_mappings(pfam2go_path, pfam_a_path, outdir):
    # pfam -> go
    pfam2go = defaultdict(list)
    for entry in parsing.parse_pfam2go(pfam2go_path):
        pfam2go[entry.pfam_accession].append(entry.go_id)

    # (uniprot accession, position in protein) -> {goterms}
    uniprot2go = {}
    uniprot2pfam = {}
    for entry in parsing.parse_pfam_A_fasta(pfam_a_path):
        uniprot_key = "{}/{}".format(entry.uniprot_accession, entry.location)
        uniprot2pfam[uniprot_key] = entry.pfam_accession
        if entry.pfam_accession not in pfam2go:
            continue
        uniprot2go[uniprot_key] = pfam2go[entry.pfam_accession]

    # write mappings to json
    with open(os.path.join(outdir, "pfam2go.json"), "w") as fout:
        json.dump(pfam2go, fout)
    with open(os.path.join(outdir, "uniprot2go.json"), "w") as fout:
        json.dump(uniprot2go, fout)
    with open(os.path.join(outdir, "uniprot2pfam.json"), "w") as fout:
        json.dump(uniprot2pfam, fout)
