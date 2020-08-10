#!/usr/bin/env python

import unittest
from utils import initiation
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestInitiation(unittest.TestCase):
    def test_init(self):
        pfam2go_test_path = os.path.join(
            THIS_DIR, 'test_data/pfam2go_small.txt')
        test_db_name = "test.db"
        if os.path.isfile(test_db_name):
            os.remove(test_db_name)
        initiation.initiate_db(test_db_name, pfam2go_test_path)
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
