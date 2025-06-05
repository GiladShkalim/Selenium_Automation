"""
Test runner for Harry Potter API tests.

This module executes all test cases for the Harry Potter Books API
and generates a test results file.
"""

import unittest
import sys
from test_utils import ResultFileWriter
from Scraper.pages.tests.potter_api.api_get import TestHarryPotterBooksAPI
from Scraper.pages.tests.potter_api.api_houses import TestHarryPotterHousesAPI

if __name__ == '__main__':
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test cases
    test_cases = [
        TestHarryPotterBooksAPI,
        TestHarryPotterHousesAPI
    ]
    
    for test_case in test_cases:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_case))
    
    # Run tests with output
    # Verbosity levels:
    # 0 = quiet (dots for success)
    # 1 = default (dots for success with basic details)
    # 2 = verbose (detailed test names and results)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Write results to file
    writer = ResultFileWriter()
    writer.write_results(result)
    
    # Exit with appropriate code
    sys.exit(not result.wasSuccessful()) 