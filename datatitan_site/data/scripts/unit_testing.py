import unittest
import generate_graphs.py

# A very basic unit testing class. For now, it just tests that iso_code isn't empty
# It works in jupyter notebook but not in PyCharm.
# How will we test graph creation? assertTrue file size > 0?

class GraphTest(unittest.TestCase):

    # Naming convention: start names of all test functions with the word "test"
    def setUp(self):
        # Arrange
        self.codes = ("USA", "CAN", "MEX")
        self.nocodes = ()
        self.str1 = ("astring")

    def tearDown(self):
        # print("tearDown called...")
        self.a = ()
        self.str1 = ()

    def test_graph(self):
        # Act
        result = gen_graph(*self.nocodes, category=str(self.str1))

        # Assert
        self.assertEqual(result, "")

# to invoke unittest framework:
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)