"""
Report system for the Vortex framework.

Contains report generation, formatting, and management utilities
for operational forecast reports and analyses.
"""

__version__ = "1.0.0"
__description__ = "Report system for Vortex framework"

# Report frequencies
REPORT_FREQUENCIES = [
    'daily',
    'weekly', 
    'monthly',
    'archived'
]

def get_report_path(frequency='daily'):
    """Get path to report directory for given frequency"""
    import os
    reports_dir = os.path.dirname(__file__)
    return os.path.join(reports_dir, frequency)

__all__ = ['get_report_path', 'REPORT_FREQUENCIES']
