"""
Parameter Integration Algorithm
Implements the Vortex RI Index from equation 2.3
"""
import numpy as np
from typing import Dict, List, Optional
import yaml
import logging

logger = logging.getLogger(__name__)

class ParameterIntegration:
    """
    Integrate 8 parameters into Vortex RI Index
    
    Vortex Index = Σ(α_i * P_i)
    where α_i are basin-dependent weights
    P_i are normalized parameters (0-1 scale)
    """
    
    def __init__(self, basin: str = "atlantic"):
        """
        Initialize integration for specific basin
        
        Parameters:
        -----------
        basin : str
            Tropical cyclone basin
        """
        self.basin = basin
        self.weights = self._load_basin_weights(basin)
        
    def _load_basin_weights(self, basin: str) -> Dict:
        """Load basin-specific weights from config"""
        config_path = f"config/basins/{basin}.yaml"
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config.get('weights', {}).get('initial_phase', {})
        except FileNotFoundError:
            logger.warning(f"Config for {basin} not found, using defaults")
            return self._get_default_weights()
    
    def _get_default_weights(self) -> Dict:
        """Default weights if config not available"""
        return {
            'ohc': 0.15,
            'sigma_sym': 0.10,
            'vws': 0.20,
            'rh_mid': 0.15,
            'vorticity': 0.10,
            'outflow': 0.10,
            'conv_org': 0.10,
            'int_trend': 0.10
        }
    
    def integrate(self, parameters: Dict[str, float], 
                  storm_stage: str = "initial_phase") -> Dict[str, float]:
        """
        Integrate normalized parameters into indices
        
        Parameters:
        -----------
        parameters : dict
            Dictionary of normalized parameters (0-1 scale)
        storm_stage : str
            Storm stage: 'initial_phase', 'intensifying_phase', 'mature_phase'
            
        Returns:
        --------
        dict: Integrated indices
        """
        try:
            # Load appropriate weights for storm stage
            weights = self._get_weights_for_stage(storm_stage)
            
            # Calculate individual indices
            thermodynamic_idx = self._calculate_thermodynamic_index(
                parameters.get('ohc_normalized', 0),
                parameters.get('sst_normalized', 0)
            )
            
            structural_idx = self._calculate_structural_index(
                parameters.get('sigma_sym', 0),
                parameters.get('convective_org_score', 0)
            )
            
            environmental_idx = self._calculate_environmental_index(
                parameters.get('vws_normalized', 0),
                parameters.get('rh_mid_normalized', 0)
            )
            
            # Calculate combined Vortex Index (equation 2.3)
            vortex_index = 0.0
            total_weight = 0.0
            
            # Parameter mapping
            param_mapping = {
                'ohc': 'ohc_normalized',
                'sigma_sym': 'sigma_sym',
                'vws': 'vws_normalized',
                'rh_mid': 'rh_mid_normalized',
                'vorticity': 'vorticity_normalized',
                'outflow': 'outflow_efficiency',
                'conv_org': 'convective_org_score',
                'int_trend': 'intensity_trend'
            }
            
            for param_name, weight in weights.items():
                param_key = param_mapping.get(param_name)
                if param_key and param_key in parameters:
                    param_value = parameters[param_key]
                    # Apply inverse transformation for VWS (equation 2.3: VWS⁻¹)
                    if param_name == 'vws' and param_value > 0:
                        param_value = 1.0 / param_value if param_value > 0.1 else 1.0
                    
                    vortex_index += weight * param_value
                    total_weight += weight
            
            if total_weight > 0:
                vortex_index /= total_weight
            
            # Apply sigmoid transformation for some parameters
            vortex_index = self._sigmoid_transform(vortex_index)
            
            logger.info(f"Vortex Index calculated: {vortex_index:.3f}")
            
            return {
                'thermodynamic_index': thermodynamic_idx,
                'structural_index': structural_idx,
                'environmental_index': environmental_idx,
                'combined_index': vortex_index,
                'weights_used': weights,
                'storm_stage': storm_stage
            }
            
        except Exception as e:
            logger.error(f"Error in parameter integration: {e}")
            return {
                'thermodynamic_index': 0.0,
                'structural_index': 0.0,
                'environmental_index': 0.0,
                'combined_index': 0.0
            }
    
    def _get_weights_for_stage(self, storm_stage: str) -> Dict:
        """Get weights for specific storm stage"""
        try:
            config_path = f"config/basins/{self.basin}.yaml"
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config.get('weights', {}).get(storm_stage, self._get_default_weights())
        except:
            return self._get_default_weights()
    
    def _calculate_thermodynamic_index(self, ohc_norm: float, sst_norm: float) -> float:
        """Calculate thermodynamic potential index"""
        return 0.6 * ohc_norm + 0.4 * sst_norm
    
    def _calculate_structural_index(self, sigma_sym: float, conv_org: float) -> float:
        """Calculate structural organization index"""
        return 0.7 * sigma_sym + 0.3 * conv_org
    
    def _calculate_environmental_index(self, vws_norm: float, rh_mid_norm: float) -> float:
        """Calculate environmental favorability index"""
        # VWS is inverse relationship (lower is better)
        vws_component = 1.0 - vws_norm
        return 0.6 * vws_component + 0.4 * rh_mid_norm
    
    def _sigmoid_transform(self, x: float) -> float:
        """Apply sigmoid transformation to limit range"""
        return 1.0 / (1.0 + np.exp(-10.0 * (x - 0.5)))
    
    def _normalize_vws(self, vws_value: float) -> float:
        """Normalize vertical wind shear (0-1, where 0 is most favorable)"""
        # From paper: <5 m/s highly favorable, >15 m/s inhibitor
        if vws_value < 5.0:
            return 0.1  # Very favorable
        elif vws_value < 10.0:
            return 0.3  # Moderately favorable
        elif vws_value < 15.0:
            return 0.7  # Unfavorable
        else:
            return 1.0  # RI inhibitor

# Test function
if __name__ == "__main__":
    integrator = ParameterIntegration("atlantic")
    
    # Example parameters (normalized 0-1)
    example_params = {
        'ohc_normalized': 0.8,
        'sst_normalized': 0.9,
        'sigma_sym': 0.7,
        'vws_normalized': 0.2,
        'rh_mid_normalized': 0.6,
        'vorticity_normalized': 0.5,
        'outflow_efficiency': 0.4,
        'convective_org_score': 0.6,
        'intensity_trend': 0.3
    }
    
    results = integrator.integrate(example_params, "intensifying_phase")
    print("Integration Results:", results)
