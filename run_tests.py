#!/usr/bin/env python
"""
Run Vortex test suite with relative paths
"""
import unittest
import sys
import os

def run_all_tests():
    """Discover and run all tests using relative paths"""
    # Add project root to path using relative path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Add src to path
    src_dir = os.path.join(project_root, "src")
    sys.path.insert(0, src_dir)
    
    print("=" * 60)
    print("VORTEX TEST SUITE (Relative Paths)")
    print("=" * 60)
    print(f"Project root: {project_root}")
    print(f"Python path[0]: {sys.path[0]}")
    print()
    
    try:
        # Discover tests
        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover('tests', pattern='test_*.py')
        
        # Run tests
        test_runner = unittest.TextTestRunner(verbosity=2)
        result = test_runner.run(test_suite)
        
        # Print summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped)}")
        
        if result.wasSuccessful():
            print("\n✅ All tests passed!")
            return 0
        else:
            print("\n❌ Some tests failed")
            return 1
            
    except Exception as e:
        print(f"\n💥 ERROR running tests: {e}")
        import traceback
        traceback.print_exc()
        return 2

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
