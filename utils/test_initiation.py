#!/usr/bin/env python

import unittest
import initiation
import os


class TestLevenshteinSamplingFunctions(unittest.TestCase):
    def test_init(self):
        test_db_name = "test.db"
        if os.path.isfile(test_db_name):
            os.remove(test_db_name)
        initiation.initiate_db(test_db_name)
        connection = initiation._connect(test_db_name)
        with connection:
            c = connection.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            db_descr = c.fetchall()
        self.assertEqual(
            db_descr,
            [('Pfam',), ('GO',), ('PfamGORelation',),
             ('UniProt',), ('PfamUniProtRelation',)])


if __name__ == '__main__':
    unittest.main()
