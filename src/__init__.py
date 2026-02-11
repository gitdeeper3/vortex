"""
Vortex - Multi-Parameter Assessment Protocol for Tropical Cyclone Rapid Intensification

A comprehensive framework for predicting Rapid Intensification (RI) in tropical cyclones
using an 8-parameter physical assessment protocol.

Version: 1.0.0
Author: Samir Baladi
Year: 2026
"""

__version__ = "1.0.0"
__author__ = "Samir Baladi"
__email__ = "gitdeeper@gmail.com"
__license__ = "MIT"
__year__ = "2026"

# Core exports
from vortex.core.vortex_engine import VortexEngine
from vortex.core.thermodynamic_model import ThermodynamicModel

# Parameter modules
from vortex.parameters.oceanic import OceanicParameters
from vortex.parameters.structural import StructuralParameters
from vortex.parameters.environmental import EnvironmentalParameters
from vortex.parameters.dynamical import DynamicalParameters

# Algorithm modules
from vortex.algorithms.time_stepping import EnhancedTimeSteppingForecast
from vortex.algorithms.probability import RIProbabilityCalculator
from vortex.algorithms.integration import ParameterIntegration

__all__ = [
    # Core
    'VortexEngine',
    'ThermodynamicModel',
    
    # Parameters
    'OceanicParameters',
    'StructuralParameters', 
    'EnvironmentalParameters',
    'DynamicalParameters',
    
    # Algorithms
    'EnhancedTimeSteppingForecast',
    'RIProbabilityCalculator',
    'ParameterIntegration',
    
    # Metadata
    '__version__',
    '__author__',
    '__email__',
    '__license__',
    '__year__',
]

# Package initialization message
print(f"🌀 Vortex Framework v{__version__} ({__year__})")
print("   Multi-Parameter Assessment Protocol for Tropical Cyclone RI")
print("   Author:", __author__)
print("   License:", __license__)
