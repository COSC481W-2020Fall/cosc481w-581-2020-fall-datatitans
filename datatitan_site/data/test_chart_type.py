import unittest



class ChartTest(unittest.TestCase):
    
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


if __name__ == "__main__":
    unittest.main()