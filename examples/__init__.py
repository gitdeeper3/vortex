"""
Example scripts and usage patterns for the Vortex framework.

Contains demonstration scripts, tutorials, and example workflows
for using the Vortex tropical cyclone forecasting system.
"""

__version__ = "1.0.0"
__description__ = "Example scripts for Vortex framework"

# Available examples
EXAMPLE_SCRIPTS = [
    'basic_forecast.py',
    'parameter_analysis.py',
    'report_generation.py',
    'operational_workflow.py'
]

def list_examples():
    """List available example scripts"""
    import os
    examples_dir = os.path.dirname(__file__)
    scripts = [f for f in os.listdir(examples_dir) 
               if f.endswith('.py') and f != '__init__.py']
    return scripts

__all__ = ['list_examples', 'EXAMPLE_SCRIPTS']
