"""
Configuration management for the Vortex framework.

Contains configuration files, settings, and environment-specific
configurations for the Vortex forecasting system.
"""

__version__ = "1.0.0"
__description__ = "Configuration management for Vortex framework"

# Available configuration files
CONFIG_FILES = [
    'basin_config.yaml',
    'model_parameters.yaml',
    'forecast_settings.yaml'
]

def get_config_path(filename):
    """Get absolute path to configuration file"""
    import os
    config_dir = os.path.dirname(__file__)
    return os.path.join(config_dir, filename)

__all__ = ['get_config_path', 'CONFIG_FILES']
