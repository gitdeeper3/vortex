"""
Utility modules for the Vortex framework.

Contains helper functions, path management, and common utilities
used throughout the Vortex framework.
"""

from .paths import get_data_path, get_config_path, get_report_path

__all__ = [
    'get_data_path',
    'get_config_path', 
    'get_report_path',
]

__version__ = "1.0.0"
__description__ = "Utility modules for Vortex framework"
