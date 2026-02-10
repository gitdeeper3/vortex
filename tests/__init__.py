"""
Test suite for Vortex framework.

Contains unit tests, integration tests, and test utilities for
verifying the functionality of the Vortex forecasting system.
"""

__version__ = "1.0.0"
__author__ = "Samir Baladi"
__test_suite_version__ = "1.0.0"

# Test categories
TEST_CATEGORIES = [
    'unit',
    'integration', 
    'performance',
    'regression'
]

# Test coverage targets
COVERAGE_TARGET = 0.85  # 85% test coverage target

def test_import():
    """Test that vortex can be imported"""
    try:
        import vortex
        return True
    except ImportError:
        return False

__all__ = ['test_import', 'TEST_CATEGORIES', 'COVERAGE_TARGET']
