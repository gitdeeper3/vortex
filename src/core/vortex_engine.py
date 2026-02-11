"""
Vortex Engine - Core processing engine for RI forecasting
Fixed to use relative paths
"""
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

# Use relative path utilities
from ..utils.paths import get_project_root, ensure_directories
from ..parameters.oceanic import OceanicParameters
from ..parameters.structural import StructuralParameters
from ..parameters.environmental import EnvironmentalParameters
from ..parameters.dynamical import DynamicalParameters
from ..algorithms.integration import ParameterIntegration
from ..algorithms.probability import RIProbabilityCalculator

logger = logging.getLogger(__name__)

class VortexEngine:
    """
    Main Vortex engine for Rapid Intensification forecasting

    Integrates 8 parameters:
    1. OHC - Ocean Heat Content
    2. σ_sym - Eyewall Symmetry
    3. VWS - Vertical Wind Shear
    4. RH_mid - Mid-Level Humidity
    5. ζ_850 - Low-Level Vorticity
    6. Org_conv - Convective Organization
    7. Eff_outflow - Outflow Efficiency
    8. ΔInt_trend - Intensity Trend
    """

    def __init__(self, basin: str = "atlantic"):
        """
        Initialize Vortex engine for specific basin

        Parameters:
        -----------
        basin : str
            Tropical cyclone basin ('atlantic', 'epacific', 'wpacific')
        """
        self.basin = basin
        self.parameters = {}
        self.ri_probability = None
        self.confidence = None

        # Ensure directories exist
        ensure_directories()

        # Get project root for relative paths
        self.project_root = get_project_root()
        
        # Initialize parameter modules
        self.oceanic = OceanicParameters(basin)
        self.structural = StructuralParameters(basin)
        self.environmental = EnvironmentalParameters(basin)
        self.dynamical = DynamicalParameters(basin)
        
        # Initialize algorithm modules
        self.integrator = ParameterIntegration()
        self.ri_calculator = RIProbabilityCalculator()

        logger.info(f"VortexEngine initialized for {basin} basin")
        logger.info(f"Project root: {self.project_root}")

    def calculate_parameters(self) -> Dict:
        """Calculate all 8 RI parameters"""
        try:
            parameters = {
                "ohc": self.oceanic.get_parameters(),
                "structural": self.structural.get_parameters(),
                "environmental": self.environmental.get_parameters(),
                "dynamical": self.dynamical.get_parameters(),
            }
            
            self.parameters = parameters
            logger.debug(f"Parameters calculated: {list(parameters.keys())}")
            return parameters
            
        except Exception as e:
            logger.error(f"Error calculating parameters: {e}")
            return {}

    def calculate_ri_probability(self, intensity_data: np.ndarray) -> float:
        """Calculate Rapid Intensification probability"""
        try:
            if self.ri_calculator and intensity_data.size > 0:
                probability = self.ri_calculator.calculate_probability(intensity_data)
                self.ri_probability = probability
                logger.info(f"RI probability calculated: {probability:.1%}")
                return probability
            return 0.0
        except Exception as e:
            logger.error(f"Error calculating RI probability: {e}")
            return 0.0

    def load_storm_data(self, storm_id: str, time: str) -> bool:
        """Load storm data (placeholder for future implementation)"""
        try:
            logger.info(f"Loading data for storm {storm_id} at {time}")
            # This would connect to a database or file system in production
            return True
        except Exception as e:
            logger.error(f"Error loading storm data: {e}")
            return False

    def generate_forecast(self, lead_times: List[int] = [12, 24, 36]) -> Dict:
        """Generate RI forecast for specified lead times"""
        try:
            forecast = {
                "basin": self.basin,
                "ri_probability": self.ri_probability,
                "confidence": self.confidence,
                "lead_times": lead_times,
                "forecasts": {}
            }
            
            for lead_time in lead_times:
                forecast["forecasts"][f"{lead_time}h"] = {
                    "probability": self.ri_probability if self.ri_probability else 0.0,
                    "confidence": self.confidence if self.confidence else "LOW"
                }
            
            logger.info(f"Forecast generated for lead times: {lead_times}")
            return forecast
            
        except Exception as e:
            logger.error(f"Error generating forecast: {e}")
            return {}

    def get_system_info(self) -> Dict:
        """Get system information including paths"""
        return {
            "basin": self.basin,
            "version": "1.0.0",
            "project_root": str(self.project_root),
            "ri_probability": self.ri_probability,
            "confidence": self.confidence,
            "parameters_loaded": bool(self.parameters),
            "status": "OPERATIONAL"
        }

    def __str__(self):
        return f"VortexEngine(basin='{self.basin}', ri_probability={self.ri_probability}, confidence={self.confidence})"

    def __repr__(self):
        return self.__str__()
