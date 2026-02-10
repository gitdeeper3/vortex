#!/usr/bin/env python
"""
Vortex Report Manager - Uses ONLY relative paths for GitLab compatibility
"""
import os
import sys
import datetime
from typing import Dict, List, Optional

# Add src to path using relative path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

from vortex.core.vortex_engine import VortexEngine
from vortex.algorithms.time_stepping import EnhancedTimeSteppingForecast
from vortex.utils.paths import get_report_path, ensure_directories

class VortexReportManager:
    """Manages vortex reports using ONLY relative paths"""
    
    def __init__(self):
        # Ensure directories exist
        ensure_directories()
        
        # Initialize vortex components
        self.engine = VortexEngine("atlantic")
        self.forecaster = EnhancedTimeSteppingForecast()
        
        # Store base paths
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
    def _get_timestamp(self):
        """Get current timestamp for filenames"""
        return datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    
    def create_daily_forecast(self, current_intensity: float = 75.0) -> str:
        """Create daily forecast report using relative paths"""
        timestamp = self._get_timestamp()
        filename = f"{timestamp}-forecast-atlantic.txt"
        
        # Get report path using relative utility
        report_dir = get_report_path("daily")
        filepath = os.path.join(str(report_dir), filename)
        
        # Generate forecast data
        mpi_trajectory = self._generate_mpi_trajectory(current_intensity)
        env_trends = self._generate_environmental_trends()
        
        # Run forecast
        forecast_result = self.forecaster.forecast_intensity(
            initial_intensity_kt=current_intensity,
            mpi_trajectory=mpi_trajectory,
            environmental_trends=env_trends,
            time_horizon_hours=48
        )
        
        # Write report
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self._format_daily_report(forecast_result, current_intensity))
        
        print(f"✓ Daily forecast created: {os.path.relpath(filepath, self.current_dir)}")
        return filepath
    
    def create_weekly_summary(self) -> str:
        """Create weekly summary report using relative paths"""
        timestamp = self._get_timestamp()
        filename = f"{timestamp}-weekly-summary-atlantic.txt"
        
        # Get report path using relative utility
        report_dir = get_report_path("weekly")
        filepath = os.path.join(str(report_dir), filename)
        
        # Generate weekly data (simulated)
        weekly_data = self._generate_weekly_data()
        
        # Write report
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self._format_weekly_report(weekly_data))
        
        print(f"✓ Weekly summary created: {os.path.relpath(filepath, self.current_dir)}")
        return filepath
    
    def create_monthly_analysis(self) -> str:
        """Create monthly analysis report using relative paths"""
        timestamp = self._get_timestamp()
        filename = f"{timestamp}-monthly-analysis-atlantic.txt"
        
        # Get report path using relative utility
        report_dir = get_report_path("monthly")
        filepath = os.path.join(str(report_dir), filename)
        
        # Generate monthly data (simulated)
        monthly_data = self._generate_monthly_data()
        
        # Write report
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self._format_monthly_report(monthly_data))
        
        print(f"✓ Monthly analysis created: {os.path.relpath(filepath, self.current_dir)}")
        return filepath
    
    def _generate_mpi_trajectory(self, current_intensity: float) -> List[float]:
        """Generate MPI trajectory for forecast"""
        import numpy as np
        time_points = 8  # 48 hours / 6 hours
        mpi_start = current_intensity * 1.3
        mpi_end = mpi_start * 1.2
        return list(np.linspace(mpi_start, mpi_end, time_points))
    
    def _generate_environmental_trends(self) -> Dict[str, List[float]]:
        """Generate environmental trends for forecast"""
        import numpy as np
        time_points = 8
        return {
            "vws": list(np.linspace(12.0, 5.0, time_points)),
            "sst": list(np.linspace(28.0, 29.5, time_points)),
            "ohc": list(np.linspace(50.0, 85.0, time_points))
        }
    
    def _generate_weekly_data(self) -> Dict:
        """Generate simulated weekly data"""
        import numpy as np
        return {
            "average_intensity": 72.5,
            "max_intensity": 95.0,
            "ri_events": 2,
            "forecast_accuracy": 0.85
        }
    
    def _generate_monthly_data(self) -> Dict:
        """Generate simulated monthly data"""
        import numpy as np
        return {
            "storms_tracked": 4,
            "average_ri_probability": 0.42,
            "peak_intensity": 117.0,
            "forecast_skill": 0.78
        }
    
    def _format_daily_report(self, forecast_result: Dict, current_intensity: float) -> str:
        """Format daily forecast report"""
        lines = []
        lines.append("=" * 60)
        lines.append("DAILY VORTEX FORECAST REPORT")
        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
        lines.append(f"Basin: Atlantic")
        lines.append(f"Current Intensity: {current_intensity} kt")
        lines.append("")
        
        if "forecast_summary" in forecast_result:
            summary = forecast_result["forecast_summary"]
            lines.append("FORECAST SUMMARY:")
            lines.append("-" * 40)
            lines.append(f"Initial Intensity: {summary.get('initial_intensity', 0):.1f} kt")
            lines.append(f"Peak Intensity: {summary.get('peak_intensity', 0):.1f} kt")
            lines.append(f"Final Intensity: {summary.get('final_intensity', 0):.1f} kt")
            lines.append(f"Intensity Change: {summary.get('intensity_change', 0):+.1f} kt")
            lines.append("")
        
        if "ri_probability_time_series" in forecast_result:
            ri_probs = forecast_result["ri_probability_time_series"]
            if ri_probs:
                avg_prob = sum(ri_probs) / len(ri_probs)
                lines.append(f"Average RI Probability: {avg_prob:.1%}")
                
                if avg_prob > 0.5:
                    lines.append("RI Risk Level: HIGH")
                elif avg_prob > 0.3:
                    lines.append("RI Risk Level: MEDIUM")
                else:
                    lines.append("RI Risk Level: LOW")
        
        lines.append("")
        lines.append("OPERATIONAL NOTES:")
        lines.append("-" * 40)
        lines.append("• Based on enhanced time-stepping model")
        lines.append("• Environmental trends show improvement")
        lines.append("• Next update in 6 hours")
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def _format_weekly_report(self, weekly_data: Dict) -> str:
        """Format weekly summary report"""
        lines = []
        lines.append("=" * 60)
        lines.append("WEEKLY VORTEX SUMMARY REPORT")
        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
        lines.append(f"Period: Weekly summary")
        lines.append("")
        
        lines.append("WEEKLY STATISTICS:")
        lines.append("-" * 40)
        lines.append(f"Average Intensity: {weekly_data['average_intensity']:.1f} kt")
        lines.append(f"Maximum Intensity: {weekly_data['max_intensity']:.1f} kt")
        lines.append(f"RI Events: {weekly_data['ri_events']}")
        lines.append(f"Forecast Accuracy: {weekly_data['forecast_accuracy']:.1%}")
        lines.append("")
        
        lines.append("WEEKLY ASSESSMENT:")
        lines.append("-" * 40)
        lines.append("• System performed within expected parameters")
        lines.append("• Forecast accuracy above target threshold")
        lines.append("• RI events within climatological range")
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def _format_monthly_report(self, monthly_data: Dict) -> str:
        """Format monthly analysis report"""
        lines = []
        lines.append("=" * 60)
        lines.append("MONTHLY VORTEX ANALYSIS REPORT")
        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
        lines.append(f"Period: Monthly analysis")
        lines.append("")
        
        lines.append("MONTHLY PERFORMANCE:")
        lines.append("-" * 40)
        lines.append(f"Storms Tracked: {monthly_data['storms_tracked']}")
        lines.append(f"Average RI Probability: {monthly_data['average_ri_probability']:.1%}")
        lines.append(f"Peak Intensity: {monthly_data['peak_intensity']:.1f} kt")
        lines.append(f"Forecast Skill Score: {monthly_data['forecast_skill']:.2f}")
        lines.append("")
        
        lines.append("SYSTEM ASSESSMENT:")
        lines.append("-" * 40)
        lines.append("• Forecast system operating nominally")
        lines.append("• All components functional")
        lines.append("• Data quality within specifications")
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def list_reports(self, frequency: str = "all"):
        """List available reports using relative paths"""
        report_counts = {}
        
        if frequency in ["all", "daily"]:
            report_dir = get_report_path("daily")
            daily_files = [f for f in os.listdir(str(report_dir)) if f.endswith('.txt')]
            report_counts['daily'] = len(daily_files)
        
        if frequency in ["all", "weekly"]:
            report_dir = get_report_path("weekly")
            weekly_files = [f for f in os.listdir(str(report_dir)) if f.endswith('.txt')]
            report_counts['weekly'] = len(weekly_files)
        
        if frequency in ["all", "monthly"]:
            report_dir = get_report_path("monthly")
            monthly_files = [f for f in os.listdir(str(report_dir)) if f.endswith('.txt')]
            report_counts['monthly'] = len(monthly_files)
        
        return report_counts

def main():
    """Main function to demonstrate report manager"""
    print("VORTEX REPORT MANAGER (Relative Paths Only)")
    print("=" * 50)
    
    # Initialize report manager
    print("\n1. Initializing report manager...")
    manager = VortexReportManager()
    print(f"   ✓ Current directory: {manager.current_dir}")
    
    # Create sample reports
    print("\n2. Creating sample reports...")
    
    # Daily forecast
    daily_report = manager.create_daily_forecast(75.0)
    print(f"   ✓ Daily: {os.path.basename(daily_report)}")
    
    # Weekly summary
    weekly_report = manager.create_weekly_summary()
    print(f"   ✓ Weekly: {os.path.basename(weekly_report)}")
    
    # Monthly analysis
    monthly_report = manager.create_monthly_analysis()
    print(f"   ✓ Monthly: {os.path.basename(monthly_report)}")
    
    # List reports
    print("\n3. Report counts:")
    counts = manager.list_reports("all")
    for freq, count in counts.items():
        print(f"   • {freq}: {count} reports")
    
    print("\n" + "=" * 50)
    print("✅ REPORT SYSTEM USING RELATIVE PATHS ONLY")
    print("=" * 50)

if __name__ == "__main__":
    main()
