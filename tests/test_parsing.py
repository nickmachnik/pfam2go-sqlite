#!/usr/bin/env python

import unittest
import os
from utils import parsing

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestParsing(unittest.TestCase):
    def test_pfam2go_entry_from_line(self):
        line = "Pfam:PF00009 GTP_EFTU > GO:GTPase activity ; GO:0003924"
        expected = parsing.Pfam2GOEntry()
        expected.pfam_accession = "PF00009"
        expected.pfam_id = "GTP_EFTU"
        expected.go_id = "GO:0003924"
        expected.go_name = "GTPase activity"
        parsed = parsing.Pfam2GOEntry()
        parsed.from_line(line)
        self.assertEqual(expected, parsed)

    def test_parse_pfam2go(self):
        pfam2go_test_path = os.path.join(
            THIS_DIR, 'test_data/pfam2go_small.txt')
        pfam2go_parser = parsing.parse_pfam2go(pfam2go_test_path)
        self.assertEqual(
            str(next(pfam2go_parser)),
            "<7tm_1, PF00001, GO:0004930, G protein-coupled receptor activity>"
            )

    def test_pfam_a_entry_from_line(self):
        line = ">F6R8L2_ORNAN/163-198 F6R8L2.1 PF10417.10;1-cysPrx_C;"
        expected = parsing.UniProtMatch()
        expected.pfam_accession = "PF10417"
        expected.uniprot_entry_name = "ORNAN"
        expected.uniprot_accession = "F6R8L2"
        expected.location = "163-198"
        parsed = parsing.UniProtMatch()
        parsed.from_line(line)
        self.assertEqual(expected, parsed)

    def test_parse_pfam_a(self):
        pfam_a_test_path = os.path.join(
            THIS_DIR, 'test_data/Pfam-A-test.fasta')
        pfam_a_parser = parsing.parse_pfam_A_fasta(pfam_a_test_path)
        self.assertEqual(
            str(next(pfam_a_parser)),
            "<A0A1S3GR90, DIPOR, 54-327, PF00001>"
            )


if __name__ == '__main__':
    unittest.main()
