#!/usr/bin/env python

import unittest
import initiation
import os


class TestLevenshteinSamplingFunctions(unittest.TestCase):
    def test_init(self):
        os.remove("test.db")
        initiation.initiate_db("test.db")
        connection = initiation._connect("test.db")
        with connection:
            c = connection.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            print(c.fetchall())
        # self.assertEqual(
        #     sample._lev_jit(
        #         np.array(['a', 'b', 'c']),
        #         np.array(['a', 'a', 'a']))[-1, -1],
        #     2)


if __name__ == '__main__':
    unittest.main()
