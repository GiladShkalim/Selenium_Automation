"""
Test utilities for Harry Potter Books API tests.

This module contains utility classes and functions used by the test suite.
"""

import os
from datetime import datetime
from io import StringIO

class ResultFileWriter:
    """Utility class for writing test results to a file."""
    
    def __init__(self, output_file="API-Test-Result.txt"):
        """Initialize the ResultFileWriter with output file path."""
        self.output_file = output_file
        # Clear existing file if it exists
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
    
    def write_results(self, test_result):
        """
        Write test results to file.
        
        Args:
            test_result: unittest.TestResult object containing test results
        """
        total_tests = test_result.testsRun
        failed = len(test_result.failures) + len(test_result.errors)
        passed = total_tests - failed
        
        with open(self.output_file, 'w') as f:
            f.write(f"Harry Potter Books API Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            
            # Write failures and errors
            if test_result.failures or test_result.errors:
                f.write("Failed Tests:\n")
                f.write("-" * 20 + "\n")
                for failure in test_result.failures:
                    test_case = failure[0]
                    f.write(f"{test_case.id()}: FAIL\n")
                    f.write(f"Reason: {failure[1]}\n\n")
                for error in test_result.errors:
                    test_case = error[0]
                    f.write(f"{test_case.id()}: ERROR\n")
                    f.write(f"Reason: {error[1]}\n\n")
            
            # Write successes
            if hasattr(test_result, 'successes'):
                f.write("\nPassed Tests:\n")
                f.write("-" * 20 + "\n")
                for test in test_result.successes:
                    test_name = test.id().split('.')[-2:]  # Get class and method name
                    test_class = test_name[0].replace('Test', '')  # Remove 'Test' prefix
                    test_method = test_name[1].replace('test_', '')  # Remove 'test_' prefix
                    f.write(f"{test_class} - {test_method}: PASS\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write(f"\nSummary:")
            f.write(f"\nTotal Tests: {total_tests}")
            f.write(f"\nPassed: {passed}")
            f.write(f"\nFailed: {failed}")

class SilentStream(StringIO):
    """A custom stream class that implements the required TextTestRunner methods."""
    
    def writeln(self, msg=None):
        """Write a line to the stream."""
        if msg is not None:
            self.write(msg)
        self.write('\n')

    def flush(self):
        """Flush the stream."""
        pass 