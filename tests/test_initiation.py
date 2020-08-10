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
        pfam_a_test_path = os.path.join(
            THIS_DIR, 'test_data/Pfam-A-test.fasta')
        self.test_db_name = "test.db"
        if os.path.isfile(self.test_db_name):
            os.remove(self.test_db_name)
        initiation.initiate_db(
            self.test_db_name, pfam2go_test_path, pfam_a_test_path)

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

    def test_init_insert_go(self):
        connection = initiation._connect(self.test_db_name)
        with connection:
            c = connection.cursor()
            c.execute("SELECT * FROM GO")
            go_table = c.fetchall()
        self.assertEqual(
            go_table,
            [('GO:0004930', 'G protein-coupled receptor activity'),
             ('GO:0007186', 'G protein-coupled receptor signaling pathway'),
             ('GO:0016021', 'integral component of membrane')])

    def test_init_insert_pfam_go_relations(self):
        connection = initiation._connect(self.test_db_name)
        with connection:
            c = connection.cursor()
            c.execute("SELECT * FROM PfamGORelation")
            rel_table = c.fetchall()
        self.assertEqual(
            rel_table,
            [('PF00001', 'GO:0004930'), ('PF00001', 'GO:0007186'),
             ('PF00001', 'GO:0016021'), ('PF00002', 'GO:0004930'),
             ('PF00002', 'GO:0007186'), ('PF00002', 'GO:0016021'),
             ('PF00003', 'GO:0004930'), ('PF00003', 'GO:0007186'),
             ('PF00003', 'GO:0016021')])

    def test_init_insert_uniprot(self):
        connection = initiation._connect(self.test_db_name)
        with connection:
            c = connection.cursor()
            c.execute("SELECT * FROM UniProt")
            uniprot_table = c.fetchall()
        self.assertEqual(
            uniprot_table,
            [('A0A1S3GR90', 'DIPOR'), ('H9JMZ1', 'BOMMO'), ('W5NMM9', 'LEPOC'),
             ('A0A498M701', 'LABRO'), ('C3Z4K9', 'BRAFL'),
             ('A0A369RQL1', '9METZ'), ('H3BCE7', 'LATCH'), ('F7BBL0', 'ORNAN'),
             ('A0A1Y3N5N1', 'PIRSE'), ('A0A493T6H5', 'ANAPP'),
             ('A0A1L8GCA2', 'XENLA'), ('A0A3P8PJJ8', 'ASTCA'),
             ('A0A3B1JRC8', 'ASTMX'), ('A0A158PBE8', 'ANGCA'),
             ('A0A482VPN5', '9CUCU')])

    def test_init_insert_pfam_uniprot_relations(self):
        connection = initiation._connect(self.test_db_name)
        with connection:
            c = connection.cursor()
            c.execute("SELECT * FROM PfamUniProtRelation")
            rel_table = c.fetchall()
        self.assertEqual(
            rel_table,
            [('PF00001', 'A0A1S3GR90', '54-327'),
             ('PF00001', 'H9JMZ1', '45-143'),
             ('PF00001', 'W5NMM9', '44-295'),
             ('PF00001', 'A0A498M701', '58-314'),
             ('PF00001', 'C3Z4K9', '144-229'),
             ('PF00001', 'A0A369RQL1', '50-274'),
             ('PF00001', 'H3BCE7', '40-292'),
             ('PF00003', 'F7BBL0', '596-841'),
             ('PF00003', 'A0A1Y3N5N1', '320-559'),
             ('PF00003', 'A0A493T6H5', '488-719'),
             ('PF00003', 'A0A1L8GCA2', '499-734'),
             ('PF00003', 'A0A3P8PJJ8', '520-719'),
             ('PF00003', 'A0A3B1JRC8', '60-287'),
             ('PF00003', 'A0A158PBE8', '363-598'),
             ('PF00003', 'A0A482VPN5', '481-733')])


if __name__ == '__main__':
    unittest.main()
