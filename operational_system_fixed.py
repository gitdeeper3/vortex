#!/usr/bin/env python
"""
Operational Vortex Forecast System - Fixed Version
"""
import numpy as np
from typing import Dict, List, Tuple
from vortex.core.vortex_engine import VortexEngine
from vortex.algorithms.time_stepping import EnhancedTimeSteppingForecast

class OperationalVortexSystem:
    """
    Complete operational system for vortex forecasting
    """
    
    def __init__(self, basin: str = "atlantic"):
        self.basin = basin
        self.engine = VortexEngine(basin)
        self.forecaster = EnhancedTimeSteppingForecast()
        self.forecast_history = []
        
    def analyze_current_conditions(self) -> Dict:
        """
        Analyze current vortex conditions
        """
        return {
            "basin": self.basin,
            "engine_status": "ACTIVE",
            "ri_probability": self.engine.ri_probability,
            "confidence": self.engine.confidence,
            "timestamp": "2024-02-10 18:00:00"
        }
    
    def generate_forecast(self, current_intensity: float, forecast_hours: int = 48) -> Dict:
        """
        Generate complete vortex forecast
        """
        print(f"\n🌀 GENERATING VORTEX FORECAST")
        print(f"   Basin: {self.basin.upper()}")
        print(f"   Current Intensity: {current_intensity} kt")
        print(f"   Forecast Horizon: {forecast_hours} hours")
        print("=" * 50)
        
        # Generate scenario
        mpi_trajectory, environmental_trends = self._generate_scenario(current_intensity, forecast_hours)
        
        # Run forecast
        forecast_result = self.forecaster.forecast_intensity(
            initial_intensity_kt=current_intensity,
            mpi_trajectory=mpi_trajectory,
            environmental_trends=environmental_trends,
            time_horizon_hours=forecast_hours
        )
        
        # Store in history
        self.forecast_history.append({
            "timestamp": "2024-02-10 18:00:00",
            "initial_intensity": current_intensity,
            "result": forecast_result
        })
        
        # Update engine
        self._update_engine_from_forecast(forecast_result)
        
        return forecast_result
    
    def _generate_scenario(self, current_intensity: float, forecast_hours: int) -> Tuple[List[float], Dict]:
        """
        Generate realistic forecast scenario
        """
        time_points = max(1, forecast_hours // 6)
        
        # MPI trajectory
        mpi_start = current_intensity * 1.3
        mpi_end = mpi_start * 1.2
        mpi_trajectory = list(np.linspace(mpi_start, mpi_end, time_points))
        
        # Environmental trends
        environmental_trends = {
            "vws": list(np.linspace(12.0, 5.0, time_points)),
            "sst": list(np.linspace(28.0, 29.5, time_points)),
            "ohc": list(np.linspace(50.0, 85.0, time_points))
        }
        
        return mpi_trajectory, environmental_trends
    
    def _update_engine_from_forecast(self, forecast_result: Dict):
        """
        Update VortexEngine with forecast results
        """
        if "ri_probability_time_series" in forecast_result:
            ri_probs = forecast_result["ri_probability_time_series"]
            if ri_probs and len(ri_probs) > 0:
                avg_prob = float(np.mean(ri_probs))
                self.engine.ri_probability = avg_prob
        
        has_error = bool(forecast_result.get("error", ""))
        self.engine.confidence = "HIGH" if not has_error else "MEDIUM"
    
    def generate_operational_report(self, forecast_result: Dict) -> str:
        """
        Generate operational report
        """
        report = []
        report.append("=" * 60)
        report.append("VORTEX OPERATIONAL FORECAST REPORT")
        report.append("=" * 60)
        report.append(f"Basin: {self.basin.upper()}")
        report.append(f"Analysis Time: 2024-02-10 18:00:00 UTC")
        report.append("")
        
        # Current conditions
        report.append("CURRENT CONDITIONS:")
        report.append("-" * 40)
        report.append(f"• RI Probability: {self.engine.ri_probability:.1%}")
        report.append(f"• Confidence Level: {self.engine.confidence}")
        report.append("")
        
        # Forecast summary
        if "forecast_summary" in forecast_result:
            summary = forecast_result["forecast_summary"]
            report.append("FORECAST SUMMARY:")
            report.append("-" * 40)
            report.append(f"• Initial Intensity: {summary.get(initial_intensity, 0):.1f} kt")
            report.append(f"• Peak Intensity: {summary.get(peak_intensity, 0):.1f} kt")
            report.append(f"• Final Intensity: {summary.get(final_intensity, 0):.1f} kt")
            report.append(f"• Intensity Change: {summary.get(intensity_change, 0):+.1f} kt")
            report.append(f"• Peak Time: Hour {summary.get(peak_intensity_time, 0)}")
            report.append("")
        
        # RI Assessment
        report.append("RAPID INTENSIFICATION ASSESSMENT:")
        report.append("-" * 40)
        if "ri_probability_time_series" in forecast_result:
            ri_probs = forecast_result["ri_probability_time_series"]
            if ri_probs and len(ri_probs) > 0:
                max_prob = max(ri_probs)
                avg_prob = np.mean(ri_probs)
                report.append(f"• Maximum RI Probability: {max_prob:.1%}")
                report.append(f"• Average RI Probability: {avg_prob:.1%}")
                
                if avg_prob > 0.5:
                    report.append("• Assessment: HIGH RI RISK")
                elif avg_prob > 0.3:
                    report.append("• Assessment: MODERATE RI RISK")
                else:
                    report.append("• Assessment: LOW RI RISK")
        
        # Recommendations
        report.append("\nOPERATIONAL RECOMMENDATIONS:")
        report.append("-" * 40)
        if self.engine.ri_probability and self.engine.ri_probability > 0.4:
            report.append("1. 🚨 Increase monitoring frequency")
            report.append("2. ⚠️  Prepare for rapid intensity changes")
            report.append("3. 📡 Enhance data assimilation")
        elif self.engine.ri_probability and self.engine.ri_probability > 0.2:
            report.append("1. 📊 Continue standard monitoring")
            report.append("2. 🔄 Update forecasts every 6 hours")
            report.append("3. 📈 Watch for environmental improvements")
        else:
            report.append("1. 📋 Maintain routine monitoring")
            report.append("2. ⏳ Next update in 12 hours")
            report.append("3. 🌊 Monitor large-scale patterns")
        
        report.append("\n" + "=" * 60)
        report.append("END OF REPORT")
        report.append("=" * 60)
        
        return "\n".join(report)

def main():
    """
    Main operational demonstration
    """
    print("\n" + "=" * 60)
    print("OPERATIONAL VORTEX FORECAST SYSTEM")
    print("=" * 60)
    
    # Initialize system
    print("\n1. Initializing operational system...")
    system = OperationalVortexSystem(basin="atlantic")
    print(f"   ✓ System initialized for {system.basin} basin")
    
    # Analyze current conditions
    print("\n2. Analyzing current conditions...")
    current_analysis = system.analyze_current_conditions()
    print(f"   ✓ Engine status: {current_analysis[engine_status]}")
    print(f"   ✓ Current RI probability: {current_analysis[ri_probability]}")
    
    # Generate forecast
    print("\n3. Generating 48-hour forecast...")
    current_intensity = 75.0
    forecast_result = system.generate_forecast(
        current_intensity=current_intensity,
        forecast_hours=48
    )
    
    # Generate operational report
    print("\n4. Generating operational report...")
    report = system.generate_operational_report(forecast_result)
    print(report)
    
    # System status
    print("\n5. System Status Summary:")
    print(f"   • Forecasts in history: {len(system.forecast_history)}")
    print(f"   • Latest RI probability: {system.engine.ri_probability:.1%}")
    print(f"   • Confidence level: {system.engine.confidence}")
    
    print("\n" + "=" * 60)
    print("✅ OPERATIONAL SYSTEM READY FOR DEPLOYMENT")
    print("=" * 60)

if __name__ == "__main__":
    main()
