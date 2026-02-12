#!/usr/bin/env python
"""
VORTEX Heavy AI Edition Report Manager
LSTM + Transformer neural network predictions for 8 basins
"""
import os
import sys
import json
import datetime
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir)
sys.path.insert(0, src_dir)

from algorithms.lstm_predictor import VortexHeavyAI
from utils.paths import get_report_path, get_project_root, ensure_directories

class VortexHeavyAIReportManager:
    """Heavy AI Edition - Neural network predictions for 8 basins"""
    
    def __init__(self):
        self.reports_dir = get_report_path("daily")
        ensure_directories()
        
        self.project_root = get_project_root()
        self.web_data_dir = self.project_root / "web" / "data"
        self.web_data_dir.mkdir(parents=True, exist_ok=True)
        
        print("🧠 Initializing VORTEX Heavy AI Edition...")
        self.heavy_ai = VortexHeavyAI()
        print("✅ Heavy AI Ready (LSTM + Transformer)")
        print(f"📁 Reports: {self.reports_dir}")
        print(f"🌐 Web: {self.web_data_dir}")
    
    def _get_risk_level(self, ri_prob):
        """Determine risk level and color"""
        if ri_prob >= 70:
            return "CRITICAL", "#ff0000", "🔴"
        elif ri_prob >= 50:
            return "HIGH", "#ff8844", "🟠"
        elif ri_prob >= 30:
            return "MEDIUM", "#ffcc00", "🟡"
        else:
            return "LOW", "#00cc88", "🟢"
    
    def generate_heavy_forecast_report(self, basin_name):
        """Generate Heavy AI forecast report"""
        configs = {
            "North Atlantic": (75.0, 130.0, 10.0, 28.5, 75.0),
            "Tropical Atlantic": (70.0, 125.0, 12.0, 27.5, 65.0),
            "Mediterranean": (45.0, 75.0, 18.0, 26.0, 40.0),
            "East Pacific": (70.0, 125.0, 12.0, 29.0, 80.0),
            "West Pacific": (80.0, 140.0, 8.0, 30.0, 90.0),
            "Indian": (65.0, 120.0, 14.0, 28.0, 70.0),
            "South Indian": (60.0, 115.0, 15.0, 27.5, 65.0),
            "South Pacific": (62.0, 118.0, 13.0, 27.8, 68.0)
        }
        
        if basin_name not in configs:
            return None
            
        intensity, mpi, shear, sst, ohc = configs[basin_name]
        forecast = self.heavy_ai.generate_basin_forecast(
            basin_name, intensity, mpi, shear, sst, ohc
        )
        
        risk_level, color, icon = self._get_risk_level(forecast['ri_probability'])
        
        # Generate report
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        basin_code = basin_name[:3].lower().replace(' ', '')
        
        report = f"""
{'='*70}
VORTEX HEAVY AI EDITION - {icon} {risk_level} RISK
{'='*70}
Generated: {timestamp} UTC
Basin: {basin_name}
Model: {forecast['model']}
Confidence: {forecast['confidence']}%

{'='*70}
NEURAL NETWORK PREDICTIONS
{'='*70}
RI Probability: {forecast['ri_probability']}%
Peak Intensity: {forecast['peak_intensity']} kt at {forecast['peak_hour']}h
Total Change (72h): {forecast['total_change']:+} kt

{'='*70}
INTENSITY TRAJECTORY (LSTM + ATTENTION)
{'='*70}
Initial:  {forecast['forecast_points']['0h']} kt
6h:      {forecast['forecast_points']['6h']} kt
12h:     {forecast['forecast_points']['12h']} kt
18h:     {forecast['forecast_points']['18h']} kt
24h:     {forecast['forecast_points']['24h']} kt
36h:     {forecast['forecast_points']['36h']} kt
48h:     {forecast['forecast_points']['48h']} kt
72h:     {forecast['forecast_points']['72h']} kt

{'='*70}
ENVIRONMENTAL CONDITIONS
{'='*70}
SST: {sst:.1f}°C | OHC: {ohc:.1f} kJ/cm²
Shear: {shear:.1f} kt | MPI: {mpi:.0f} kt

{'='*70}
BASIN STATISTICS
{'='*70}
Historical Peak: {self.heavy_ai.lstm.basin_patterns[basin_name]['max_intensity']} kt
Season Peak: {self.heavy_ai.lstm.basin_patterns[basin_name]['season_peak']}
Typical Lifetime: {self.heavy_ai.lstm.basin_patterns[basin_name]['typical_lifetime']}h

{'='*70}
Forecast ID: {datetime.datetime.now().strftime('%Y%m%d%H%M')}-{basin_code}-HEAVY
{'='*70}
"""
        
        # Save report
        filename = f"{datetime.datetime.now().strftime('%Y-%m-%d-%H%M')}-{basin_code}-heavy-ai.txt"
        filepath = os.path.join(self.reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"✅ {basin_name}: {forecast['ri_probability']}% | {risk_level} | Confidence: {forecast['confidence']}%")
        
        return {
            "basin": basin_name,
            "forecast": forecast,
            "risk": risk_level,
            "color": color,
            "report_path": str(filepath)
        }
    
    def generate_all_heavy_reports(self):
        """Generate Heavy AI reports for all 8 basins"""
        print("\n🌍 VORTEX HEAVY AI - 8 BASIN FORECASTS")
        print("=" * 70)
        
        results = []
        basins = [
            "North Atlantic", "Tropical Atlantic", "Mediterranean",
            "East Pacific", "West Pacific", "Indian",
            "South Indian", "South Pacific"
        ]
        
        for basin in basins:
            print(f"\n📍 {basin}:")
            result = self.generate_heavy_forecast_report(basin)
            if result:
                results.append(result)
        
        # Update web JSON
        self.update_web_json(results)
        
        return results
    
    def update_web_json(self, results):
        """Update web interface JSON with Heavy AI predictions"""
        json_path = self.web_data_dir / "basins_heavy.json"
        
        basins_data = []
        for r in results:
            fc = r['forecast']
            basins_data.append({
                "name": r['basin'],
                "code": r['basin'][:3].lower().replace(' ', ''),
                "ri": fc['ri_probability'],
                "risk": r['risk'],
                "color": r['color'],
                "intensity": fc['forecast_points']['0h'],
                "peak": fc['peak_intensity'],
                "peak_hour": fc['peak_hour'],
                "change": fc['total_change'],
                "confidence": fc['confidence'],
                "model": "Heavy AI (LSTM+Transformer)",
                "trajectory": fc['trajectory'][:13]
            })
        
        data = {
            "last_update": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "model": "VORTEX Heavy AI Edition",
            "total_basins": len(basins_data),
            "basins": basins_data
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"\n🌐 Heavy AI web JSON updated: {json_path}")


if __name__ == "__main__":
    import sys
    
    print("🚀 VORTEX Heavy AI Edition - LSTM + Transformer")
    print("=" * 70)
    
    manager = VortexHeavyAIReportManager()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        results = manager.generate_all_heavy_reports()
        print(f"\n🎯 Generated {len(results)} Heavy AI reports")
        
    elif len(sys.argv) > 1:
        basin = " ".join(sys.argv[1:])
        result = manager.generate_heavy_forecast_report(basin)
        if result:
            print(f"\n✅ Report saved: {result['report_path']}")
        else:
            print(f"\n❌ Basin '{basin}' not found")
            print("\nAvailable basins:")
            basins = ["North Atlantic", "Tropical Atlantic", "Mediterranean",
                     "East Pacific", "West Pacific", "Indian",
                     "South Indian", "South Pacific"]
            for b in basins:
                print(f"  • {b}")
                
    else:
        print("\nUsage:")
        print("  --all              : Generate forecasts for all 8 basins")
        print("  <basin_name>       : Generate forecast for specific basin")
        print("\nExample:")
        print("  python report_manager_heavy_ai.py --all")
        print("  python report_manager_heavy_ai.py \"West Pacific\"")
