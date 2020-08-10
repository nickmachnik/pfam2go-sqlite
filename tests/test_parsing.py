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


if __name__ == '__main__':
    unittest.main()
