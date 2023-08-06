import unittest
import elutils.utils

class TestUtils(unittest.TestCase):

    def sum_dicts(self):
        a = {"apples": 4, "beets": 12}
        b = {"apples": 2, "beets": 1, "oranges": 2}
        self.assertEquals(elutils.utils.sum_dicts(a,b),{"apples":6,"beets":13,"oranges":2})
        self.assertEquals(elutils.utils.sum_dicts({},{}),{})
        self.assertEquals(elutils.utils.sum_dicts({"cars":12},{}),{"cars":12})

