import os
import unittest
import sys
from datetime import datetime
from io import StringIO

class ResultFileWriter:
    def __init__(self, output_file="Selenium-Test-Result.txt"):
        self.output_file = output_file
        # Clear existing file if it exists
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
    
    def write_results(self, test_result):
        """Write test results to file"""
        total_tests = test_result.testsRun
        failed = len(test_result.failures) + len(test_result.errors)
        passed = total_tests - failed
        
        with open(self.output_file, 'w') as f:
            f.write(f"Selenium Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            
            # Write failures and errors
            if test_result.failures or test_result.errors:
                f.write("Failed Tests:\n")
                f.write("-" * 20 + "\n")
                for failure in test_result.failures:
                    test_case = failure[0]
                    f.write(f"{test_case.id().split('.')[-1]}: FAIL\n")
                    f.write(f"Reason: {failure[1]}\n\n")
                for error in test_result.errors:
                    test_case = error[0]
                    f.write(f"{test_case.id().split('.')[-1]}: ERROR\n")
                    f.write(f"Reason: {error[1]}\n\n")
            
            # Write successes
            if hasattr(test_result, 'successes'):
                f.write("\nPassed Tests:\n")
                f.write("-" * 20 + "\n")
                for test in test_result.successes:
                    f.write(f"{test.id().split('.')[-1]}: PASS\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write(f"\nSummary:")
            f.write(f"\nTotal Tests: {total_tests}")
            f.write(f"\nPassed: {passed}")
            f.write(f"\nFailed: {failed}")

class SilentStream(StringIO):
    """A custom stream class that implements the required TextTestRunner methods"""
    def writeln(self, msg=None):
        if msg is not None:
            self.write(msg)
        self.write('\n')

    def flush(self):
        pass

class SilentTestRunner(unittest.TextTestRunner):
    """Custom test runner that minimizes console output"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stream = SilentStream()
        self.resultclass = unittest.TestResult
        self.verbosity = 0
        
    def run(self, test):
        """Run the tests silently and collect results"""
        result = super().run(test)
        result.successes = []
        
        # Get all test cases from the suite
        def get_all_tests(test_suite):
            tests = []
            for test in test_suite:
                if isinstance(test, unittest.TestCase):
                    tests.append(test)
                elif hasattr(test, '_tests'):
                    tests.extend(get_all_tests(test._tests))
            return tests
            
        all_tests = get_all_tests(test)
        failed_tests = [failure[0] for failure in result.failures]
        failed_tests.extend(error[0] for error in result.errors)
        
        # Add successful tests to result
        for test in all_tests:
            if test not in failed_tests:
                result.successes.append(test)
        
        return result 