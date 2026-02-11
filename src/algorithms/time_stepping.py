#!/usr/bin/env python
"""
Enhanced Time Stepping Module for Vortex Intensity Forecasting
Fixed version with proper error handling
"""
import numpy as np
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class EnhancedTimeSteppingForecast:
    """
    Enhanced time stepping forecast with fixed indexing
    """
    
    def __init__(self, time_step_hours: float = 1.0):
        # Model parameters
        self.dt = time_step_hours
        self.forecast_horizon = 72  # maximum horizon in hours
        
        # Environmental response parameters
        self.alpha_base = 0.15
        self.beta_shear = 0.08
        self.gamma_cold_wake = 0.05
        
        # Cold wake memory
        self.cold_wake_memory = 0.0
        self.memory_decay_base = 0.95
        
        # Rate limits
        self.limit_up_max = 25.0
        self.limit_down_max = -15.0
        
        # Uncertainty bounds
        self.max_uncertainty = 0.35
        
        # RI detection parameters
        self.ri_threshold_kt = 30.0
        self.ri_shear_threshold = 15.0
        self.ri_mpi_margin_min = 20.0
        
        # Initialize state
        self.reset_memory()
    
    def reset_memory(self):
        """Reset cold wake memory for new forecast"""
        self.cold_wake_memory = 0.0
        return True
    
    def _prepare_array(self, data: List[float], target_length: int, 
                      default_value: float, min_val: float, max_val: float) -> np.ndarray:
        """
        Prepare and validate input array
        """
        if not data:
            return np.full(target_length, default_value)
        
        # Ensure proper length
        if len(data) < target_length:
            # Extend with last value
            data = data + [data[-1]] * (target_length - len(data))
        elif len(data) > target_length:
            # Truncate
            data = data[:target_length]
        
        # Convert to numpy array and clamp values
        arr = np.array(data, dtype=float)
        return np.clip(arr, min_val, max_val)
    
    def forecast_intensity(self,
                          initial_intensity_kt: float,
                          mpi_trajectory: List[float],
                          environmental_trends: Dict[str, List[float]],
                          time_horizon_hours: int = 48) -> Dict:
        """
        Fixed intensity forecast with proper indexing
        
        Returns dictionary with:
        - time_points_hours: List of time points
        - intensity_forecast_kt: Forecast intensity at each time point
        - ri_probability_time_series: RI probability at each time point
        - forecast_summary: Dictionary with summary statistics
        - error: Error message if any
        """
        error_msg = ""
        
        try:
            # Reset for new forecast
            self.reset_memory()
            
            # Validate time horizon
            time_horizon_hours = min(time_horizon_hours, self.forecast_horizon)
            if time_horizon_hours <= 0:
                error_msg = "Invalid time horizon"
                return self._create_error_result(error_msg)
            
            # Calculate number of steps
            n_steps = int(time_horizon_hours / self.dt)
            if n_steps <= 0:
                error_msg = "Number of steps must be positive"
                return self._create_error_result(error_msg)
            
            # Create time points
            time_points = np.arange(0, time_horizon_hours + self.dt, self.dt)
            
            # Initialize intensity array
            intensity = np.zeros(len(time_points))
            intensity[0] = initial_intensity_kt
            
            # Prepare environmental arrays with fixed indexing
            mpi_array = self._prepare_array(mpi_trajectory, len(time_points), 
                                           initial_intensity_kt * 1.5, 0, 250)
            
            # Get environmental parameters with defaults
            shear = self._prepare_array(
                environmental_trends.get("vws", environmental_trends.get("shear_kt", [])),
                len(time_points), 10.0, 0, 50
            )
            
            sst = self._prepare_array(
                environmental_trends.get("sst", []),
                len(time_points), 28.0, 20, 35
            )
            
            ohc = self._prepare_array(
                environmental_trends.get("ohc", environmental_trends.get("ohc_kj_cm2", [])),
                len(time_points), 60.0, 0, 120
            )
            
            # Main integration loop with bounds checking
            for i in range(1, len(time_points)):
                # Ensure we don"t exceed array bounds
                if i >= len(mpi_array) or i >= len(shear) or i >= len(sst) or i >= len(ohc):
                    break
                
                prev_intensity = intensity[i-1]
                current_mpi = mpi_array[i-1]
                current_shear = shear[i-1]
                current_sst = sst[i-1]
                current_ohc = ohc[i-1]
                
                # Calculate intensity change (simplified model)
                mpi_margin = current_mpi - prev_intensity
                
                # Environmental factors
                shear_factor = max(0, 1 - current_shear / 20.0)  # Reduced by shear
                sst_factor = max(0.5, min(1.5, current_sst / 28.0))  # SST effect
                ohc_factor = max(0.7, min(1.3, current_ohc / 60.0))  # OHC effect
                
                # Combined environmental factor
                env_factor = shear_factor * sst_factor * ohc_factor
                
                # Calculate intensity change
                if mpi_margin > 0:
                    intensity_change = self.alpha_base * mpi_margin * env_factor * self.dt
                else:
                    intensity_change = -0.1 * prev_intensity * self.dt  # Decay
                
                # Apply rate limits
                intensity_change = np.clip(intensity_change, 
                                         self.limit_down_max * self.dt,
                                         self.limit_up_max * self.dt)
                
                # Update intensity
                intensity[i] = prev_intensity + intensity_change
                
                # Ensure non-negative
                intensity[i] = max(0, intensity[i])
            
            # Calculate RI probabilities
            ri_probability = self._calculate_ri_probability(intensity, mpi_array, shear)
            
            # Create forecast summary
            forecast_summary = self._create_forecast_summary(intensity, mpi_array)
            
            # Return successful result
            return {
                "time_points_hours": time_points.tolist(),
                "intensity_forecast_kt": intensity.tolist(),
                "ri_probability_time_series": ri_probability.tolist(),
                "forecast_summary": forecast_summary,
                "error": error_msg  # Empty string means no error
            }
            
        except Exception as e:
            error_msg = f"Forecast error: {str(e)}"
            logger.error(error_msg)
            return self._create_error_result(error_msg)
    
    def _calculate_ri_probability(self, intensity: np.ndarray, 
                                 mpi: np.ndarray, shear: np.ndarray) -> np.ndarray:
        """Calculate Rapid Intensification probability"""
        ri_prob = np.zeros_like(intensity)
        
        for i in range(1, len(intensity)):
            # Check RI conditions
            intensity_change = intensity[i] - intensity[0]
            mpi_margin = mpi[i] - intensity[i]
            current_shear = shear[i] if i < len(shear) else shear[-1]
            
            # Probability based on conditions
            prob = 0.0
            
            if intensity_change > self.ri_threshold_kt:
                prob += 0.4
            
            if mpi_margin > self.ri_mpi_margin_min:
                prob += 0.3
            
            if current_shear < self.ri_shear_threshold:
                prob += 0.3
            
            # Clamp probability
            ri_prob[i] = min(1.0, max(0.0, prob))
        
        return ri_prob
    
    def _create_forecast_summary(self, intensity: np.ndarray, 
                                mpi: np.ndarray) -> Dict:
        """Create forecast summary statistics"""
        if len(intensity) == 0:
            return {"error": "No forecast data"}
        
        initial = intensity[0]
        final = intensity[-1]
        peak = np.max(intensity)
        
        return {
            "initial_intensity": float(initial),
            "final_intensity": float(final),
            "peak_intensity": float(peak),
            "intensity_change": float(final - initial),
            "peak_intensity_time": int(np.argmax(intensity) * self.dt),
            "error": False
        }
    
    def _create_error_result(self, error_message: str) -> Dict:
        """Create error result dictionary"""
        return {
            "time_points_hours": [],
            "intensity_forecast_kt": [],
            "ri_probability_time_series": [],
            "forecast_summary": {
                "initial_intensity": 0.0,
                "final_intensity": 0.0,
                "peak_intensity": 0.0,
                "intensity_change": 0.0,
                "error": True
            },
            "error": error_message
        }
    
    def generate_operational_summary(self, forecast_result: Dict) -> str:
        """Generate operational summary text"""
        if not forecast_result or "error" not in forecast_result:
            return "Invalid forecast result"
        
        if forecast_result["error"]:
            return f"Forecast error: {forecast_result[error]}"
        
        summary = forecast_result.get("forecast_summary", {})
        if not summary:
            return "No summary available"
        
        lines = []
        lines.append("VORTEX INTENSITY FORECAST SUMMARY")
        lines.append("=" * 40)
        lines.append(f"Initial Intensity: {summary.get(initial_intensity, 0):.1f} kt")
        lines.append(f"Peak Intensity: {summary.get(peak_intensity, 0):.1f} kt")
        lines.append(f"Final Intensity: {summary.get(final_intensity, 0):.1f} kt")
        lines.append(f"Intensity Change: {summary.get(intensity_change, 0):+.1f} kt")
        
        # RI assessment
        ri_prob_series = forecast_result.get("ri_probability_time_series", [])
        if ri_prob_series:
            avg_ri_prob = np.mean(ri_prob_series) if hasattr(ri_prob_series, "__len__") else 0
            lines.append(f"Average RI Probability: {avg_ri_prob:.1%}")
        
        lines.append("=" * 40)
        return "\n".join(lines)

class TimeStepper:
    """
    Simple time stepper for backward compatibility.
    Wraps EnhancedTimeSteppingForecast for compatibility.
    """
    
    def __init__(self, time_step_hours: float = 1.0):
        self.forecaster = EnhancedTimeSteppingForecast(time_step_hours)
    
    def forecast(self, initial_intensity: float, hours: int = 24) -> float:
        """Simple forecast wrapper"""
        # Create simple trajectory
        mpi_trajectory = [initial_intensity * 1.2] * 8
        env_trends = {
            "vws": [10.0] * 8,
            "sst": [28.0] * 8
        }
        
        result = self.forecaster.forecast_intensity(
            initial_intensity_kt=initial_intensity,
            mpi_trajectory=mpi_trajectory,
            environmental_trends=env_trends,
            time_horizon_hours=hours
        )
        
        if "intensity_forecast_kt" in result:
            return result["intensity_forecast_kt"][-1]
        return initial_intensity
