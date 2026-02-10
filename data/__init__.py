"""
Data management for the Vortex framework.

Contains data structures, sample datasets, and data handling
utilities for the Vortex forecasting system.
"""

__version__ = "1.0.0"
__description__ = "Data management for Vortex framework"

# Data categories
DATA_CATEGORIES = [
    'sample_storms',
    'environmental_data',
    'forecast_results',
    'validation_sets'
]

def get_sample_data_path():
    """Get path to sample data directory"""
    import os
    return os.path.dirname(__file__)

__all__ = ['get_sample_data_path', 'DATA_CATEGORIES']
