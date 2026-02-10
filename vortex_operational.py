#!/usr/bin/env python
"""
Vortex Operational System - Using ONLY relative paths
"""
import os
import sys

# Add src to path using relative path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

import numpy as np
from vortex.core.vortex_engine import VortexEngine
from vortex.algorithms.time_stepping import EnhancedTimeSteppingForecast
from vortex.utils.paths import ensure_directories

class VortexOperationalSystem:
    """Operational vortex forecasting system using relative paths only"""
    
    def __init__(self, basin="atlantic"):
        # Ensure directories exist
        ensure_directories()
        
        self.basin = basin
        self.engine = VortexEngine(basin)
        self.forecaster = EnhancedTimeSteppingForecast()
        self.forecast_history = []
        
        # Store current directory for relative paths
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
    
    def get_system_status(self):
        """Get current system status"""
        return {
            "basin": self.basin,
            "engine_status": "OPERATIONAL",
            "ri_probability": self.engine.ri_probability,
            "confidence": self.engine.confidence
        }
    
    def create_forecast(self, current_intensity=75.0, hours=48):
        """Create a new forecast using relative paths"""
        print(f"\n🌪️  Creating {hours}-hour forecast")
        print(f"   Current intensity: {current_intensity} kt")
        print("=" * 50)
        
        # Generate forecast data
        time_points = max(4, hours // 6)
        
        # MPI trajectory
        mpi_start = current_intensity * 1.3
        mpi_end = mpi_start * 1.2
        mpi_trajectory = list(np.linspace(mpi_start, mpi_end, time_points))
        
        # Environmental data
        env_data = {
            "vws": list(np.linspace(12.0, 5.0, time_points)),
            "sst": list(np.linspace(28.0, 29.5, time_points)),
            "ohc": list(np.linspace(50.0, 85.0, time_points))
        }
        
        # Run forecast
        result = self.forecaster.forecast_intensity(
            initial_intensity_kt=current_intensity,
            mpi_trajectory=mpi_trajectory,
            environmental_trends=env_data,
            time_horizon_hours=hours
        )
        
        # Store result
        self.forecast_history.append(result)
        
        # Update engine
        self._update_engine(result)
        
        return result
    
    def _update_engine(self, forecast_result):
        """Update engine with forecast results"""
        if "ri_probability_time_series" in forecast_result:
            ri_probs = forecast_result["ri_probability_time_series"]
            if ri_probs and len(ri_probs) > 0:
                avg_prob = float(np.mean(ri_probs))
                self.engine.ri_probability = avg_prob
        
        has_error = bool(forecast_result.get("error", ""))
        self.engine.confidence = "HIGH" if not has_error else "MEDIUM"
    
    def generate_report(self, forecast_result):
        """Generate operational report"""
        lines = []
        lines.append("=" * 60)
        lines.append("VORTEX OPERATIONAL REPORT")
        lines.append("=" * 60)
        lines.append(f"Basin: {self.basin.upper()}")
        lines.append(f"Time: System Time")
        lines.append("")
        
        # System status
        lines.append("SYSTEM STATUS:")
        lines.append("-" * 40)
        status = self.get_system_status()
        lines.append(f"• Status: {status['engine_status']}")
        lines.append(f"• RI Probability: {status['ri_probability']:.1%}")
        lines.append(f"• Confidence: {status['confidence']}")
        lines.append("")
        
        # Forecast results
        if "forecast_summary" in forecast_result:
            summary = forecast_result["forecast_summary"]
            lines.append("FORECAST RESULTS:")
            lines.append("-" * 40)
            lines.append(f"• Initial: {summary.get('initial_intensity', 0):.1f} kt")
            lines.append(f"• Peak: {summary.get('peak_intensity', 0):.1f} kt")
            lines.append(f"• Final: {summary.get('final_intensity', 0):.1f} kt")
            lines.append(f"• Change: {summary.get('intensity_change', 0):+.1f} kt")
            lines.append("")
        
        # Recommendations
        lines.append("RECOMMENDATIONS:")
        lines.append("-" * 40)
        prob = status['ri_probability']
        if prob and prob > 0.4:
            lines.append("🚨 HIGH RI RISK - Enhanced monitoring required")
            lines.append("   • Increase observation frequency")
            lines.append("   • Prepare for rapid changes")
        elif prob and prob > 0.2:
            lines.append("⚠️  MODERATE RI RISK - Standard monitoring")
            lines.append("   • Update forecast every 6 hours")
            lines.append("   • Watch environmental trends")
        else:
            lines.append("✅ LOW RI RISK - Routine monitoring")
            lines.append("   • Next update in 12 hours")
            lines.append("   • Monitor large-scale patterns")
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)

def main():
    """Main function"""
    print("VORTEX OPERATIONAL SYSTEM (Relative Paths Only)")
    print("=" * 50)
    
    # Initialize
    print("\n1. Initializing system...")
    system = VortexOperationalSystem("atlantic")
    print("   ✓ System ready")
    
    # Get status
    print("\n2. Checking system status...")
    status = system.get_system_status()
    print(f"   • Basin: {status['basin']}")
    print(f"   • Status: {status['engine_status']}")
    print(f"   • RI Probability: {status['ri_probability']}")
    
    # Create forecast
    print("\n3. Running forecast...")
    forecast = system.create_forecast(current_intensity=75.0, hours=48)
    
    # Check for errors
    if forecast.get("error"):
        print(f"   ⚠️  Forecast warning: {forecast['error']}")
    else:
        print("   ✓ Forecast completed successfully")
    
    # Generate report
    print("\n4. Generating report...")
    report = system.generate_report(forecast)
    print(report)
    
    # Final status
    print("\n5. Final system status:")
    final_status = system.get_system_status()
    print(f"   • Forecasts run: {len(system.forecast_history)}")
    print(f"   • Current RI probability: {final_status['ri_probability']:.1%}")
    print(f"   • Confidence level: {final_status['confidence']}")
    
    print("\n" + "=" * 50)
    print("✅ SYSTEM OPERATIONAL (Relative Paths Only)")
    print("=" * 50)

if __name__ == "__main__":
    main()
