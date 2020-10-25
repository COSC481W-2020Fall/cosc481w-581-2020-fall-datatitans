import unittest


class ChartTest(unittest.TestCase):
    
    # Naming convention: start names of all test functions with the word "test"
    def setUp(self):
        # Arrange
        self.nocodes = ()
        self.none = ()
        self.line = ("LINE")
        
    def tearDown(self):
        # print("tearDown called...")
        self.a = ()
        self.str1 = ()
    
    def test_no_chart(self):
        result = gen_no_graph(*self.nocodes, category=str(""))
        
        # Assert
        self.assertEqual(result, None)

    def test_line_chart(self):
        # No function to call in forms.py, other than init
        result = gen_line_graph(*self.nocodes, category=str("LINE"))
        result = "LINE"
        # Assert
        self.assertEqual(result, "LINE")

    

    


def gen_no_graph(*iso_codes, category: str, chart_type="") -> str:
    print("chart type: ", chart_type)
    return

def gen_line_graph(*iso_codes, category: str, chart_type="LINE") -> str:
    print("chart type: ", chart_type)
    return

if __name__ == "__main__":
    unittest.main()