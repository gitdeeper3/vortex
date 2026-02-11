"""
Core modules for the Vortex framework.

Contains the main engine and thermodynamic models for tropical cyclone
intensity forecasting and rapid intensification prediction.
"""

from .vortex_engine import VortexEngine
from .thermodynamic_model import ThermodynamicModel

__all__ = ['VortexEngine', 'ThermodynamicModel']

__version__ = "1.0.0"
__description__ = "Core engine and models for Vortex framework"
