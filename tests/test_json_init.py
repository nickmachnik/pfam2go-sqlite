#!/usr/bin/env python

import unittest
import os
import json
from utils import json_init

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestJsonInit(unittest.TestCase):
    def test_init(self):
        outdir = os.path.join(THIS_DIR, "test_data")
        pfam2go_test_path = os.path.join(
            THIS_DIR, 'test_data/pfam2go_small.txt')
        pfam_a_test_path = os.path.join(
            THIS_DIR, 'test_data/Pfam-A-test.fasta')
        json_init.create_uniprot_go_pfam_mappings(
            pfam2go_test_path,
            pfam_a_test_path,
            outdir)

        with open(os.path.join(outdir, "pfam2go.json"), "r") as fin:
            pfam2go = json.load(fin)
        with open(os.path.join(outdir, "uniprot2go.json"), 'r') as fin:
            uniprot2go = json.load(fin)
        with open(os.path.join(outdir, "uniprot2pfam.json"), 'r') as fin:
            uniprot2pfam = json.load(fin)

        self.assertEqual(
            pfam2go["PF00001"],
            ['GO:0004930', 'GO:0007186', 'GO:0016021'])
        self.assertEqual(
            uniprot2go["C3Z4K9/144-229"],
            ['GO:0004930', 'GO:0007186', 'GO:0016021'])
        self.assertEqual(
            uniprot2pfam["C3Z4K9/144-229"], "PF00001")


if __name__ == '__main__':
    unittest.main()
