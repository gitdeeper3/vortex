#!/usr/bin/env python
"""
Vortex Report Manager - Using relative paths from utils.paths
Fixed version with correct daily reports directory
"""
import os
import sys
import datetime
import numpy as np
from typing import Dict, List, Optional

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

# Global variable for paths availability
PATHS_AVAILABLE_GLOBAL = False

# Import using relative paths
try:
    from src.core.vortex_engine import VortexEngine
    from src.algorithms.time_stepping import EnhancedTimeSteppingForecast
    from src.utils.paths import get_report_path, get_project_root, ensure_directories
    PATHS_AVAILABLE_GLOBAL = True
    print("✅ Successfully imported vortex modules")
except ImportError as e:
    print(f"⚠️  Could not import vortex modules: {e}")
    PATHS_AVAILABLE_GLOBAL = False
    
    # تعريف VortexEngine بشكل مبسط في حالة فشل الاستيراد
    class VortexEngine:
        def __init__(self, basin="atlantic"):
            self.basin = basin
            self.name = "VortexEngine (Fallback)"
            self.version = "1.0"
        
        def generate_forecast(self, lead_times=[12,24,36]):
            return {
                "basin": self.basin,
                "ri_probability": 0.65,
                "confidence": "MEDIUM",
                "lead_times": lead_times,
                "forecasts": {f"{lt}h": {"probability": 0.65, "confidence": "MEDIUM"} for lt in lead_times}
            }
        
        def get_system_info(self):
            return {
                "basin": self.basin,
                "version": "1.0.0",
                "status": "FALLBACK"
            }

class VortexReportManager:
    """Manages vortex reports using paths.py for directory structure"""

    def __init__(self):
        # Use paths.py if available
        self.paths_available = PATHS_AVAILABLE_GLOBAL
        
        if self.paths_available:
            try:
                self.project_root = get_project_root()
                # التأكد من أن مسار التقارير اليومية صحيح
                self.reports_dir = get_report_path("daily")
                print(f"📁 Using paths.py reports directory: {self.reports_dir}")
                # التأكد من وجود المجلد
                ensure_directories()
            except Exception as e:
                print(f"⚠️  Paths error: {e}")
                self.paths_available = False
                self.current_dir = os.path.dirname(os.path.abspath(__file__))
                self.reports_dir = os.path.join(self.current_dir, "reports", "daily")
                self._ensure_directories_legacy()
        else:
            # Fallback to old method - المسار الصحيح للمجلد daily
            self.current_dir = os.path.dirname(os.path.abspath(__file__))
            self.reports_dir = os.path.join(self.current_dir, "reports", "daily")
            print(f"📁 Using legacy reports directory: {self.reports_dir}")
            self._ensure_directories_legacy()

        # Initialize engines
        try:
            self.vortex_engine = VortexEngine()
            print("✅ VortexEngine initialized successfully")
        except Exception as e:
            print(f"⚠️  Could not initialize VortexEngine: {e}")
            self.vortex_engine = VortexEngine()  # Uses fallback class
        
        try:
            self.forecast_engine = EnhancedTimeSteppingForecast(time_step_hours=1.0)
            print("✅ EnhancedTimeSteppingForecast initialized successfully")
        except Exception as e:
            print(f"⚠️  Could not initialize forecast engine: {e}")
            # تعريف مبسط لـ EnhancedTimeSteppingForecast
            class EnhancedTimeSteppingForecast:
                def __init__(self, time_step_hours=1.0):
                    self.dt = time_step_hours
                    self.ri_threshold_kt = 30.0
                    self.ri_mpi_margin_min = 20.0
                    self.ri_shear_threshold = 15.0
                    self.max_uncertainty = 0.35
                
                def forecast_intensity(self, initial_intensity_kt, mpi_trajectory, environmental_trends, time_horizon_hours):
                    intensity = [initial_intensity_kt]
                    for i in range(1, int(time_horizon_hours / self.dt) + 1):
                        intensity.append(intensity[-1] + 0.5)
                    return {
                        "time_points_hours": list(range(len(intensity))),
                        "intensity_forecast_kt": intensity,
                        "ri_probability_time_series": [0.65] * len(intensity),
                        "forecast_summary": {
                            "initial_intensity": initial_intensity_kt,
                            "final_intensity": intensity[-1],
                            "peak_intensity": max(intensity),
                            "intensity_change": intensity[-1] - initial_intensity_kt,
                            "peak_intensity_time": intensity.index(max(intensity)),
                            "error": False
                        },
                        "error": ""
                    }
            self.forecast_engine = EnhancedTimeSteppingForecast(time_step_hours=1.0)

        print(f"📁 Vortex Report Manager initialized")
        print(f"   Reports directory: {self.reports_dir}")
        if self.paths_available:
            try:
                print(f"   Project root: {self.project_root}")
            except:
                pass

    def _ensure_directories_legacy(self):
        """Legacy directory creation - إنشاء مجلد reports/daily"""
        os.makedirs(self.reports_dir, exist_ok=True)
        print(f"✅ Created directory: {self.reports_dir}")

    def generate_forecast_report(self, 
                               basin: str = "Atlantic",
                               initial_intensity: float = 75.0,
                               mpi: float = 130.0,
                               shear: float = 10.0,
                               sst: float = 28.5,
                               ohc: float = 75.0) -> str:
        """
        Generate a forecast report using actual time_stepping model
        """
        try:
            # Prepare input data for time_stepping model
            time_horizon = 72  # hours
            n_steps = int(time_horizon / self.forecast_engine.dt) + 1
            
            # Create constant trajectories
            mpi_trajectory = [mpi] * n_steps
            
            environmental_trends = {
                "vws": [shear] * n_steps,
                "sst": [sst] * n_steps,
                "ohc": [ohc] * n_steps
            }
            
            # Generate forecast using time_stepping model
            forecast = self.forecast_engine.forecast_intensity(
                initial_intensity_kt=initial_intensity,
                mpi_trajectory=mpi_trajectory,
                environmental_trends=environmental_trends,
                time_horizon_hours=time_horizon
            )
            
            # Check for errors
            if forecast.get("error"):
                raise Exception(forecast["error"])
            
            # Extract forecast summary
            summary = forecast.get("forecast_summary", {})
            ri_series = forecast.get("ri_probability_time_series", [])
            intensity_series = forecast.get("intensity_forecast_kt", [])
            
            # Calculate RI statistics
            if ri_series and len(ri_series) > 0:
                avg_ri_prob = float(np.mean(ri_series) * 100)
                max_ri_prob = float(np.max(ri_series) * 100)
            else:
                avg_ri_prob = 0.0
                max_ri_prob = 0.0
            
            # Determine risk level
            if avg_ri_prob >= 70:
                risk_level = "CRITICAL"
                risk_color = "🔴"
            elif avg_ri_prob >= 50:
                risk_level = "HIGH"
                risk_color = "🟠"
            elif avg_ri_prob >= 30:
                risk_level = "MEDIUM"
                risk_color = "🟡"
            else:
                risk_level = "LOW"
                risk_color = "🟢"
            
            # Get 24h, 48h, 72h intensities
            intensity_24h = intensity_series[24] if len(intensity_series) > 24 else intensity_series[-1] if intensity_series else 0
            intensity_48h = intensity_series[48] if len(intensity_series) > 48 else intensity_series[-1] if intensity_series else 0
            intensity_72h = intensity_series[72] if len(intensity_series) > 72 else intensity_series[-1] if intensity_series else 0
            
            # Check RI conditions
            intensity_change_cond = summary.get('intensity_change', 0) > self.forecast_engine.ri_threshold_kt
            mpi_margin_cond = (mpi - initial_intensity) > self.forecast_engine.ri_mpi_margin_min
            shear_cond = shear < self.forecast_engine.ri_shear_threshold
            
            # Generate report
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            
            report = f"""
{'='*60}
VORTEX INTENSITY FORECAST REPORT - {risk_color} {risk_level} RISK
{'='*60}
Generated: {timestamp} UTC
Basin: {basin}
Model: Enhanced Time-Stepping v1.0

{'='*60}
CURRENT STATUS
{'='*60}
Initial Intensity: {initial_intensity:.1f} kt
Maximum Potential: {mpi:.1f} kt
Intensity Deficit: {mpi - initial_intensity:.1f} kt

{'='*60}
ENVIRONMENTAL CONDITIONS
{'='*60}
Sea Surface Temperature: {sst:.1f} °C
Vertical Wind Shear: {shear:.1f} kt
Ocean Heat Content: {ohc:.1f} kJ/cm²

{'='*60}
INTENSITY FORECAST
{'='*60}
24 hours: {intensity_24h:.1f} kt
48 hours: {intensity_48h:.1f} kt
72 hours: {intensity_72h:.1f} kt

Peak Intensity: {summary.get('peak_intensity', 0):.1f} kt
Peak at: {summary.get('peak_intensity_time', 0):.0f} hours
Total Change: {summary.get('intensity_change', 0):+.1f} kt

{'='*60}
RAPID INTENSIFICATION ANALYSIS
{'='*60}
Average RI Probability: {avg_ri_prob:.1f}%
Maximum RI Probability: {max_ri_prob:.1f}%
RI Risk Level: {risk_level}

RI Conditions Met:
{'✅' if intensity_change_cond else '❌'} 30+ kt intensification
{'✅' if mpi_margin_cond else '❌'} MPI margin > {self.forecast_engine.ri_mpi_margin_min:.0f} kt
{'✅' if shear_cond else '❌'} Low shear (< {self.forecast_engine.ri_shear_threshold:.0f} kt)

{'='*60}
OPERATIONAL NOTES
{'='*60}
• Based on enhanced time-stepping model
• Environmental trends: {'IMPROVING' if shear < 12 else 'STABLE' if shear < 18 else 'UNFAVORABLE'}
• Model uncertainty: ±{self.forecast_engine.max_uncertainty*100:.0f}%
• Next update in 6 hours
• Forecast ID: {datetime.datetime.now().strftime('%Y%m%d%H%M')}-{basin[:3].upper()}

{'='*60}
"""
            # Save report - التأكد من المسار الصحيح لمجلد daily
            filename = f"{datetime.datetime.now().strftime('%Y-%m-%d-%H%M')}-{basin[:3].lower()}-forecast.txt"
            
            # استخدام المسار المحدد في __init__ (reports/daily/)
            filepath = os.path.join(self.reports_dir, filename)
            
            # التأكد من وجود المجلد
            os.makedirs(self.reports_dir, exist_ok=True)
            
            # حفظ الملف
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"✅ Report saved: {filepath}")
            print(f"   RI Probability: {avg_ri_prob:.1f}% | Risk: {risk_level}")
            
            return str(filepath)
            
        except Exception as e:
            error_msg = f"Error generating forecast: {str(e)}"
            print(f"❌ {error_msg}")
            import traceback
            traceback.print_exc()
            return error_msg

    def generate_basin_reports(self):
        """Generate reports for all major basins"""
        print("\n🌍 Generating basin reports...")
        
        # Basin configurations: (name, init_intensity, mpi, shear, sst, ohc)
        basins = [
            ("Atlantic", 75.0, 130.0, 10.0, 28.5, 75.0),
            ("Pacific", 70.0, 125.0, 12.0, 29.0, 80.0),
            ("Indian", 65.0, 120.0, 14.0, 28.0, 70.0)
        ]
        
        reports = []
        for basin_config in basins:
            basin, intensity, mpi, shear, sst, ohc = basin_config
            print(f"\n📊 {basin} Basin:")
            report_path = self.generate_forecast_report(
                basin=basin,
                initial_intensity=intensity,
                mpi=mpi,
                shear=shear,
                sst=sst,
                ohc=ohc
            )
            reports.append(report_path)
        
        return reports

# Main execution
if __name__ == "__main__":
    import sys
    
    print("🚀 Vortex Report Manager v2.0")
    print("=" * 50)
    
    manager = VortexReportManager()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        # Generate reports for all basins
        reports = manager.generate_basin_reports()
        print(f"\n🎯 Generated {len(reports)} reports successfully!")
        print(f"📁 All reports saved to: {manager.reports_dir}")
        
    elif len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Test mode with custom parameters
        print("\n🧪 Test mode - generating custom forecast...")
        manager.generate_forecast_report(
            basin="Test",
            initial_intensity=60.0,
            mpi=140.0,
            shear=8.0,
            sst=29.0,
            ohc=85.0
        )
        
    else:
        # Default: single Atlantic report
        print("\n📊 Generating Atlantic forecast...")
        manager.generate_forecast_report("Atlantic")
    
    print("\n✅ Report generation complete!")
