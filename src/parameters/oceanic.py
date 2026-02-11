"""
Oceanic Parameters Module
- OHC (Ocean Heat Content)
- SST (Sea Surface Temperature)
"""
import numpy as np
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class OceanicParameters:
    """Calculate oceanic parameters for RI forecasting"""
    
    def __init__(self, basin: str):
        """
        Initialize oceanic parameters calculator
        
        Parameters:
        -----------
        basin : str
            Tropical cyclone basin
        """
        self.basin = basin
        self.ohc_thresholds = self._get_basin_thresholds(basin)
        
    def _get_basin_thresholds(self, basin: str) -> Dict:
        """Get basin-specific thresholds for oceanic parameters"""
        thresholds = {
            'atlantic': {'ohc_ri': 50, 'ohc_high': 80, 'sst_ri': 28.0},
            'epacific': {'ohc_ri': 40, 'ohc_high': 70, 'sst_ri': 27.5},
            'wpacific': {'ohc_ri': 60, 'ohc_high': 90, 'sst_ri': 29.0}
        }
        return thresholds.get(basin, thresholds['atlantic'])
    
    def calculate_ohc(self, sst: float, mixed_layer_depth: float, 
                     ocean_temp_profile: np.ndarray) -> Dict[str, float]:
        """
        Calculate Ocean Heat Content (OHC)
        
        OHC = ρ * Cp * ∫(T(z) - 26°C) dz from surface to 26°C isotherm
        
        Parameters:
        -----------
        sst : float
            Sea surface temperature (°C)
        mixed_layer_depth : float
            Mixed layer depth (m)
        ocean_temp_profile : np.ndarray
            Ocean temperature profile
            
        Returns:
        --------
        dict: OHC value and normalized score
        """
        try:
            # Constants
            rho = 1025  # kg/m³ (seawater density)
            cp = 3850   # J/kg/°C (specific heat capacity)
            
            # Calculate OHC (simplified)
            # In practice, this would integrate temperature above 26°C
            t_excess = max(0, sst - 26.0)
            ohc_value = rho * cp * t_excess * mixed_layer_depth / 1e9  # Convert to kJ/cm²
            
            # Normalize score (0-1)
            ohc_norm = min(1.0, ohc_value / self.ohc_thresholds['ohc_high'])
            
            logger.info(f"OHC calculated: {ohc_value:.1f} kJ/cm² (Score: {ohc_norm:.2f})")
            
            return {
                'value': ohc_value,
                'normalized': ohc_norm,
                'category': self._categorize_ohc(ohc_value),
                'ri_favorable': ohc_value > self.ohc_thresholds['ohc_ri']
            }
            
        except Exception as e:
            logger.error(f"Error calculating OHC: {e}")
            return {'value': None, 'normalized': 0.0, 'category': 'unknown', 'ri_favorable': False}
    
    def _categorize_ohc(self, ohc_value: float) -> str:
        """Categorize OHC value"""
        if ohc_value < 20:
            return 'very_low'
        elif ohc_value < 40:
            return 'low'
        elif ohc_value < 60:
            return 'moderate'
        elif ohc_value < 80:
            return 'high'
        else:
            return 'very_high'
    
    def calculate_sst(self, sst_data: np.ndarray) -> Dict[str, float]:
        """
        Calculate Sea Surface Temperature metrics
        
        Parameters:
        -----------
        sst_data : np.ndarray
            SST data array
            
        Returns:
        --------
        dict: SST metrics
        """
        try:
            sst_mean = float(np.nanmean(sst_data))
            sst_std = float(np.nanstd(sst_data))
            sst_gradient = self._calculate_sst_gradient(sst_data)
            
            # Normalize (28-30°C is optimal for RI)
            sst_norm = max(0, min(1, (sst_mean - 26) / 4))
            
            return {
                'mean': sst_mean,
                'std': sst_std,
                'gradient': sst_gradient,
                'normalized': sst_norm,
                'ri_favorable': sst_mean > self.ohc_thresholds['sst_ri']
            }
            
        except Exception as e:
            logger.error(f"Error calculating SST: {e}")
            return {'mean': None, 'normalized': 0.0, 'ri_favorable': False}
    
    def _calculate_sst_gradient(self, sst_data: np.ndarray) -> float:
        """Calculate SST gradient magnitude"""
        # Simplified gradient calculation
        # In practice, use proper spatial gradient
        if sst_data.ndim != 2:
            return 0.0
        
        try:
            grad_x = np.gradient(sst_data, axis=1)
            grad_y = np.gradient(sst_data, axis=0)
            grad_mag = np.sqrt(grad_x**2 + grad_y**2)
            return float(np.nanmean(grad_mag))
        except:
            return 0.0
    
    def calculate(self) -> Dict[str, float]:
        """
        Calculate all oceanic parameters
        
        Returns:
        --------
        dict: All oceanic parameters
        """
        # TODO: Replace with actual data loading
        # Example data - in real implementation, load from data sources
        sst_example = 29.5  # °C
        mld_example = 50    # m
        temp_profile_example = np.array([29.5, 29.0, 28.5, 28.0, 27.5])
        
        ohc_results = self.calculate_ohc(
            sst=sst_example,
            mixed_layer_depth=mld_example,
            ocean_temp_profile=temp_profile_example
        )
        
        sst_results = self.calculate_sst(np.array([[sst_example]]))
        
        return {
            'ohc_value': ohc_results['value'],
            'ohc_normalized': ohc_results['normalized'],
            'ohc_category': ohc_results['category'],
            'sst_mean': sst_results['mean'],
            'sst_normalized': sst_results['normalized'],
            'sst_gradient': sst_results['gradient']
        }

# Example usage
if __name__ == "__main__":
    oceanic = OceanicParameters("atlantic")
    results = oceanic.calculate()
    print("Oceanic Parameters:", results)
