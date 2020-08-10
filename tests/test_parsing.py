#!/usr/bin/env python

import unittest
from utils import parsing


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


if __name__ == '__main__':
    unittest.main()
