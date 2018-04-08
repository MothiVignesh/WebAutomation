import unittest
from tests.Amazon.BookSearchTest import cBookSearch

# Get all tests from the test classes
tc1 = unittest.TestLoader().loadTestsFromTestCase(cBookSearch)
#tc2 = unittest.TestLoader().loadTestsFromTestCase(RegisterCoursesCSVDataTests)

# Create a test suite combining all test classes
SmokeTest = unittest.TestSuite([tc1])

unittest.TextTestRunner(verbosity=2).run(SmokeTest)