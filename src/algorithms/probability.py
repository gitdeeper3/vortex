"""
RI Probability Calculation
Implements logistic calibration from equation 2.6
"""
import numpy as np
from typing import Dict, Tuple, Optional
import yaml
import logging

logger = logging.getLogger(__name__)

class RIProbabilityCalculator:
    """
    Calculate RI probability using logistic regression
    
    P(RI) = 1 / (1 + exp(-(β₀ + β₁·VI + β₂·VI² + β₃·CI)))
    where VI = Vortex Index, CI = Confidence Index
    """
    
    def __init__(self, basin: str = "atlantic"):
        """
        Initialize probability calculator
        
        Parameters:
        -----------
        basin : str
            Tropical cyclone basin
        """
        self.basin = basin
        self.calibration_coeffs = self._load_calibration_coeffs(basin)
        
    def _load_calibration_coeffs(self, basin: str) -> Dict:
        """Load basin-specific calibration coefficients"""
        config_path = f"config/basins/{basin}.yaml"
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config.get('calibration', {})
        except FileNotFoundError:
            logger.warning(f"Calibration for {basin} not found, using defaults")
            return self._get_default_calibration()
    
    def _get_default_calibration(self) -> Dict:
        """Default calibration coefficients"""
        return {
            'beta_0': -3.5,
            'beta_1': 7.0,
            'beta_2': -3.0,
            'beta_3': 1.0
        }
    
    def calculate(self, parameters: Dict[str, float], 
                  indices: Dict[str, float],
                  lead_time: int = 24,
                  confidence: float = 0.8) -> Dict[str, float]:
        """
        Calculate RI probability for given lead time
        
        Parameters:
        -----------
        parameters : dict
            Dictionary of parameter values
        indices : dict
            Dictionary of integrated indices
        lead_time : int
            Forecast lead time in hours (12, 24, 36)
        confidence : float
            Data confidence factor (0-1)
            
        Returns:
        --------
        dict: Probability results
        """
        try:
            # Extract Vortex Index
            vortex_index = indices.get('combined_index', 0.0)
            
            # Apply logistic function (equation 2.6)
            beta_0 = self.calibration_coeffs.get('beta_0', -3.5)
            beta_1 = self.calibration_coeffs.get('beta_1', 7.0)
            beta_2 = self.calibration_coeffs.get('beta_2', -3.0)
            beta_3 = self.calibration_coeffs.get('beta_3', 1.0)
            
            # Calculate probability
            linear_component = beta_0 + beta_1 * vortex_index
            quadratic_component = beta_2 * (vortex_index ** 2)
            confidence_component = beta_3 * confidence
            
            z = linear_component + quadratic_component + confidence_component
            probability = 1.0 / (1.0 + np.exp(-z))
            
            # Adjust for lead time (shorter lead times = higher confidence)
            lead_time_factor = self._get_lead_time_factor(lead_time)
            probability *= lead_time_factor
            
            # Categorize probability
            category = self._categorize_probability(probability)
            
            # Check threshold exceedance
            thresholds_exceeded = self._check_thresholds(parameters)
            
            logger.info(f"RI Probability ({lead_time}h): {probability:.1%} ({category})")
            
            return {
                'probability': float(probability),
                'category': category,
                'lead_time': lead_time,
                'vortex_index': float(vortex_index),
                'confidence': float(confidence),
                'threshold_exceedance': thresholds_exceeded,
                'calibration_coeffs': self.calibration_coeffs
            }
            
        except Exception as e:
            logger.error(f"Error calculating probability: {e}")
            return {
                'probability': 0.0,
                'category': 'unknown',
                'lead_time': lead_time,
                'confidence': 0.0
            }
    
    def _get_lead_time_factor(self, lead_time: int) -> float:
        """Adjust probability based on lead time"""
        # From paper: probability decreases with longer lead times
        if lead_time <= 12:
            return 1.0
        elif lead_time <= 24:
            return 0.9
        elif lead_time <= 36:
            return 0.8
        elif lead_time <= 48:
            return 0.7
        else:
            return 0.6
    
    def _categorize_probability(self, probability: float) -> str:
        """Categorize probability based on operational thresholds"""
        if probability < 0.2:
            return 'very_low'
        elif probability < 0.4:
            return 'low'
        elif probability < 0.6:
            return 'moderate'
        elif probability < 0.8:
            return 'high'
        else:
            return 'very_high'
    
    def _check_thresholds(self, parameters: Dict[str, float]) -> Dict[str, bool]:
        """Check which RI thresholds are exceeded"""
        thresholds = {
            'ohc_favorable': parameters.get('ohc_normalized', 0) > 0.7,
            'sigma_sym_favorable': parameters.get('sigma_sym', 0) > 0.6,
            'vws_favorable': parameters.get('vws_normalized', 0) < 0.3,
            'rh_mid_favorable': parameters.get('rh_mid_normalized', 0) > 0.6,
            'conv_org_favorable': parameters.get('convective_org_score', 0) > 0.5,
            'intensity_increasing': parameters.get('intensity_trend', 0) > 0
        }
        
        # Count favorable conditions
        favorable_count = sum(1 for v in thresholds.values() if v)
        thresholds['favorable_count'] = favorable_count
        thresholds['majority_favorable'] = favorable_count >= 4  # Half of 8 parameters
        
        return thresholds
    
    def calculate_for_multiple_lead_times(self, parameters: Dict, indices: Dict,
                                         lead_times: list = [12, 24, 36, 48]) -> Dict:
        """Calculate probability for multiple lead times"""
        results = {}
        
        for lt in lead_times:
            prob_result = self.calculate(parameters, indices, lead_time=lt)
            results[f'{lt}h'] = prob_result
        
        # Calculate probability trend
        if len(lead_times) >= 2:
            trend = self._calculate_probability_trend(results)
            results['trend'] = trend
        
        return results
    
    def _calculate_probability_trend(self, results: Dict) -> str:
        """Calculate if probability is increasing/decreasing with lead time"""
        lead_times = sorted([k for k in results.keys() if k.endswith('h')])
        if len(lead_times) < 2:
            return 'unknown'
        
        probs = [results[lt]['probability'] for lt in lead_times]
        
        if probs[-1] > probs[0] + 0.1:
            return 'increasing'
        elif probs[-1] < probs[0] - 0.1:
            return 'decreasing'
        else:
            return 'stable'

# Test function
if __name__ == "__main__":
    calculator = RIProbabilityCalculator("atlantic")
    
    example_params = {
        'ohc_normalized': 0.8,
        'sigma_sym': 0.7,
        'vws_normalized': 0.2,
        'rh_mid_normalized': 0.6,
        'convective_org_score': 0.6,
        'intensity_trend': 0.3
    }
    
    example_indices = {
        'combined_index': 0.75
    }
    
    results = calculator.calculate(example_params, example_indices, lead_time=24)
    print("Probability Results:", results)
