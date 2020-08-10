#!/usr/bin/env python

import unittest
from utils import initiation
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestInitiation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInitiation, self).__init__(*args, **kwargs)
        pfam2go_test_path = os.path.join(
            THIS_DIR, 'test_data/pfam2go_small.txt')
        self.test_db_name = "test.db"
        if os.path.isfile(self.test_db_name):
            os.remove(self.test_db_name)
        initiation.initiate_db(self.test_db_name, pfam2go_test_path)

    def test_init_tables(self):
        connection = initiation._connect(self.test_db_name)
        with connection:
            c = connection.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            db_descr = c.fetchall()
        self.assertEqual(
            db_descr,
            [('Pfam',), ('GO',), ('PfamGORelation',),
             ('UniProt',), ('PfamUniProtRelation',)])

    def test_init_insert_pfam(self):
        connection = initiation._connect(self.test_db_name)
        with connection:
            c = connection.cursor()
            c.execute("SELECT * FROM Pfam")
            pfam_table = c.fetchall()
        self.assertEqual(
            pfam_table,
            [('PF00001', '7tm_1'), ('PF00002', '7tm_2'), ('PF00003', '7tm_3')])


if __name__ == '__main__':
    unittest.main()
