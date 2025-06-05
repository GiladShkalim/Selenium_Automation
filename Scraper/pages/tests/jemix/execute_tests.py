import unittest
import sys
from test_utils import ResultFileWriter, SilentTestRunner
from Scraper.pages.tests.jemix.HomePage_load import TestHomePageLoad
from Scraper.pages.tests.jemix.LoginPage_test import TestLogin
from Scraper.pages.tests.jemix.test_logout import TestLogout
from Scraper.pages.tests.jemix.test_main_navigation import TestMainNavigation
from Scraper.pages.tests.jemix.test_category_navigation import TestCategoryNavigation

if __name__ == '__main__':
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test cases
    test_cases = [
        TestHomePageLoad,
        TestLogin,
        TestLogout,
        TestMainNavigation,
        TestCategoryNavigation
    ]
    
    for test_case in test_cases:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_case))
    
    # Run tests silently
    runner = SilentTestRunner()
    result = runner.run(suite)
    
    # Write results to file
    writer = ResultFileWriter()
    writer.write_results(result)
    
    # Exit with appropriate code
    sys.exit(not result.wasSuccessful())
