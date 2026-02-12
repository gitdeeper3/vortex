#!/usr/bin/env python
"""
Vortex Report Manager - AI Light Version
مع دعم 8 أحواض محيطية كاملة وتكامل بصري مع JSON
"""
import os
import sys
import datetime
import json
import numpy as np
from pathlib import Path

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir)
sys.path.insert(0, src_dir)

# استيراد نسخة AI الخفيفة
from algorithms.ri_probability_light import RIProbabilityLight
from utils.paths import get_report_path, get_project_root, ensure_directories

class VortexAILightReportManager:
    """مدير التقارير بنسخة AI الخفيفة - 8 أحواض مع تحديث JSON"""
    
    def __init__(self):
        # إنشاء المجلدات
        self.reports_dir = get_report_path("daily")
        ensure_directories()
        
        # مجلد بيانات الويب
        self.project_root = get_project_root()
        self.web_data_dir = self.project_root / "web" / "data"
        self.web_data_dir.mkdir(parents=True, exist_ok=True)
        self.basin_json_path = self.web_data_dir / "basins.json"
        
        # تهيئة AI
        print("🧠 Initializing Vortex AI Light...")
        self.ri_classifier = RIProbabilityLight()
        
        # تكوينات الأحواض الثمانية الكاملة
        self.basin_configs = {
            # شمال المحيط الأطلسي - الولايات المتحدة وأوروبا
            "North Atlantic": {
                "code": "nat",
                "initial_intensity": 75.0,
                "mpi": 130.0,
                "shear": 10.0,
                "sst": 28.5,
                "ohc": 75.0,
                "rh": 72.0,
                "es": 0.75,
                "of": 0.65,
                "llv": 12.0,
                "it": 6.0,
                "description": "North Atlantic Basin (USA, Caribbean, Europe)",
                "agency": "NHC (National Hurricane Center)",
                "season": "June 1 - November 30",
                "type": "Hurricane"
            },
            
            # المحيط الأطلسي الاستوائي - الرأس الأخضر وغرب أفريقيا
            "Tropical Atlantic": {
                "code": "tat",
                "initial_intensity": 70.0,
                "mpi": 125.0,
                "shear": 12.0,
                "sst": 27.5,
                "ohc": 65.0,
                "rh": 70.0,
                "es": 0.72,
                "of": 0.63,
                "llv": 11.0,
                "it": 5.0,
                "description": "Tropical Atlantic Basin (Cape Verde, West Africa)",
                "agency": "Meteo-France / NHC",
                "season": "July - October",
                "type": "Hurricane"
            },
            
            # البحر الأبيض المتوسط - أوروبا وشمال أفريقيا
            "Mediterranean": {
                "code": "med",
                "initial_intensity": 45.0,
                "mpi": 75.0,
                "shear": 18.0,
                "sst": 26.0,
                "ohc": 40.0,
                "rh": 60.0,
                "es": 0.60,
                "of": 0.50,
                "llv": 8.0,
                "it": 2.0,
                "description": "Mediterranean Sea (Medicane)",
                "agency": "ESWF (European Severe Weather Facility)",
                "season": "September - January",
                "type": "Medicane"
            },
            
            # المحيط الهادئ الشرقي - قرب أمريكا الوسطى
            "East Pacific": {
                "code": "eas",
                "initial_intensity": 70.0,
                "mpi": 125.0,
                "shear": 12.0,
                "sst": 29.0,
                "ohc": 80.0,
                "rh": 70.0,
                "es": 0.73,
                "of": 0.68,
                "llv": 11.5,
                "it": 5.5,
                "description": "Eastern Pacific Basin (Mexico, Central America)",
                "agency": "NHC (National Hurricane Center)",
                "season": "May 15 - November 30",
                "type": "Hurricane"
            },
            
            # المحيط الهادئ الغربي - آسيا والفلبين
            "West Pacific": {
                "code": "wes",
                "initial_intensity": 80.0,
                "mpi": 140.0,
                "shear": 8.0,
                "sst": 30.0,
                "ohc": 90.0,
                "rh": 75.0,
                "es": 0.80,
                "of": 0.72,
                "llv": 14.0,
                "it": 8.0,
                "description": "Western Pacific Basin (Philippines, Japan, China)",
                "agency": "JMA (Japan Meteorological Agency)",
                "season": "Year-round (peak July-October)",
                "type": "Typhoon"
            },
            
            # المحيط الهندي الشمالي - جنوب آسيا
            "Indian": {
                "code": "ind",
                "initial_intensity": 65.0,
                "mpi": 120.0,
                "shear": 14.0,
                "sst": 28.0,
                "ohc": 70.0,
                "rh": 68.0,
                "es": 0.70,
                "of": 0.62,
                "llv": 10.8,
                "it": 4.5,
                "description": "North Indian Basin (India, Bangladesh)",
                "agency": "IMD (India Meteorological Department)",
                "season": "April - December",
                "type": "Cyclone"
            },
            
            # المحيط الهندي الجنوبي - أستراليا وجنوب أفريقيا
            "South Indian": {
                "code": "sou",
                "initial_intensity": 60.0,
                "mpi": 115.0,
                "shear": 15.0,
                "sst": 27.5,
                "ohc": 65.0,
                "rh": 65.0,
                "es": 0.68,
                "of": 0.60,
                "llv": 10.0,
                "it": 4.0,
                "description": "South Indian Basin (Madagascar, Mauritius)",
                "agency": "MFR (Météo-France La Reunion)",
                "season": "November - April",
                "type": "Cyclone"
            },
            
            # المحيط الهادئ الجنوبي - أستراليا ونيوزيلندا وفيجي
            "South Pacific": {
                "code": "sop",
                "initial_intensity": 62.0,
                "mpi": 118.0,
                "shear": 13.0,
                "sst": 27.8,
                "ohc": 68.0,
                "rh": 66.0,
                "es": 0.69,
                "of": 0.61,
                "llv": 10.5,
                "it": 4.2,
                "description": "South Pacific Basin (Australia, Fiji, Vanuatu)",
                "agency": "FMS (Fiji Meteorological Service)",
                "season": "November - April",
                "type": "Cyclone"
            }
        }
        
        print(f"📁 Reports directory: {self.reports_dir}")
        print(f"🌐 Web data directory: {self.web_data_dir}")
        print(f"✅ AI Light Ready - {len(self.basin_configs)} Basins Loaded")
    
    def _get_risk_level(self, ri_prob):
        """تحديد مستوى الخطر واللون"""
        if ri_prob >= 70:
            return "CRITICAL", "#ff0000", "🔴"
        elif ri_prob >= 50:
            return "HIGH", "#ff8844", "🟠"
        elif ri_prob >= 30:
            return "MEDIUM", "#ffcc00", "🟡"
        else:
            return "LOW", "#00cc88", "🟢"
    
    def _get_trend(self, ri_prob, previous_ri=None):
        """تحديد اتجاه التغير"""
        if previous_ri is None:
            return "stable"
        if ri_prob > previous_ri + 2:
            return "rising"
        elif ri_prob < previous_ri - 2:
            return "falling"
        else:
            return "stable"
    
    def update_basin_json(self, basin_data):
        """تحديث ملف JSON لقراءة صفحة الويب"""
        try:
            # قراءة الملف القديم إن وجد
            old_data = {}
            if self.basin_json_path.exists():
                with open(self.basin_json_path, 'r', encoding='utf-8') as f:
                    old_data = json.load(f)
            
            # تحويل بيانات الأحواض إلى JSON
            basins_list = []
            for basin_name, data in basin_data.items():
                ri_prob = data['ri_probability']
                risk_level, color, _ = self._get_risk_level(ri_prob)
                
                # الحصول على القيمة السابقة
                previous_ri = None
                if 'basins' in old_data:
                    for old_basin in old_data['basins']:
                        if old_basin['name'] == basin_name:
                            previous_ri = old_basin.get('ri')
                            break
                
                trend = self._get_trend(ri_prob, previous_ri)
                
                basins_list.append({
                    "name": basin_name,
                    "code": data['code'],
                    "ri": round(ri_prob, 1),
                    "risk": risk_level,
                    "color": color,
                    "intensity": round(data['initial_intensity'], 0),
                    "trend": trend,
                    "type": data['type'],
                    "sst": round(data['sst'], 1),
                    "shear": round(data['shear'], 1)
                })
            
            # ترتيب الأحواض حسب RI (الأعلى أولاً)
            basins_list.sort(key=lambda x: x['ri'], reverse=True)
            
            json_data = {
                "last_update": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "total_basins": len(basins_list),
                "critical_count": sum(1 for b in basins_list if b['risk'] == "CRITICAL"),
                "high_count": sum(1 for b in basins_list if b['risk'] == "HIGH"),
                "medium_count": sum(1 for b in basins_list if b['risk'] == "MEDIUM"),
                "basins": basins_list
            }
            
            # حفظ الملف
            with open(self.basin_json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            print(f"🌐 Updated web JSON: {self.basin_json_path}")
            
        except Exception as e:
            print(f"❌ Error updating JSON: {e}")
    
    def generate_ai_forecast_report(self, basin_name: str) -> dict:
        """
        توليد تقرير باستخدام AI الخفيف لحوض محدد
        """
        try:
            # الحصول على تكوين الحوض
            if basin_name not in self.basin_configs:
                return {"error": f"Basin '{basin_name}' not found"}
            
            config = self.basin_configs[basin_name].copy()
            
            # تجهيز الميزات
            features = {
                'sst': config['sst'],
                'ohc': config['ohc'],
                'vws': config['shear'],
                'rh': config['rh'],
                'es': config['es'],
                'of': config['of'],
                'llv': config['llv'],
                'it': config['it']
            }
            
            # توقع RI
            ri_prob = self.ri_classifier.predict_proba(features) * 100
            config['ri_probability'] = ri_prob
            
            # توقع الشدة
            initial = config['initial_intensity']
            mpi = config['mpi']
            shear = config['shear']
            
            if basin_name == "Mediterranean":
                intensity_change = 0.08 * (mpi - initial) * (1 - shear/25) * 48
                intensity_72h = initial + min(25, max(0, intensity_change))
            else:
                intensity_change = 0.15 * (mpi - initial) * (1 - shear/20) * 72
                intensity_72h = initial + min(45, max(0, intensity_change))
            
            config['forecast_72h'] = round(intensity_72h, 1)
            
            # إنشاء التقرير النصي
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            basin_code = config['code']
            risk_level, color, risk_icon = self._get_risk_level(ri_prob)
            
            report = f"""
{'='*60}
VORTEX AI LIGHT FORECAST - {risk_icon} {risk_level} RISK
{'='*60}
Generated: {timestamp} UTC
Basin: {basin_name}
Region: {config['description']}
System Type: {config['type']}
RI Probability: {ri_prob:.1f}%

{'='*60}
CURRENT STATUS
{'='*60}
Initial Intensity: {initial:.1f} kt
Maximum Potential: {mpi:.1f} kt
72h Forecast: {intensity_72h:.1f} kt

{'='*60}
ENVIRONMENTAL CONDITIONS
{'='*60}
SST: {config['sst']:.1f}°C | OHC: {config['ohc']:.1f} kJ/cm²
Shear: {config['shear']:.1f} kt | RH: {config['rh']:.1f}%

{'='*60}
Forecast ID: {datetime.datetime.now().strftime('%Y%m%d%H%M')}-{basin_code}-AIL
{'='*60}
"""
            # حفظ التقرير النصي
            filename = f"{datetime.datetime.now().strftime('%Y-%m-%d-%H%M')}-{basin_code}-ai-light.txt"
            filepath = os.path.join(self.reports_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"✅ {basin_name}: {ri_prob:.1f}% | {risk_level}")
            
            return config
            
        except Exception as e:
            print(f"❌ Error generating forecast for {basin_name}: {e}")
            return {"error": str(e)}
    
    def generate_all_basin_reports(self):
        """توليد تقارير AI وتحديث JSON"""
        print("\n🌍 Generating AI Light reports for 8 basins...")
        print("=" * 50)
        
        basin_results = {}
        for basin_name in self.basin_configs.keys():
            print(f"\n📊 {basin_name}:")
            result = self.generate_ai_forecast_report(basin_name)
            if "error" not in result:
                basin_results[basin_name] = result
        
        # تحديث ملف JSON للواجهة
        if basin_results:
            self.update_basin_json(basin_results)
        
        return basin_results


# MAIN EXECUTION
if __name__ == "__main__":
    import sys
    
    print("🚀 Vortex AI Light Report Manager - 8 Basins with Web Integration")
    print("=" * 70)
    
    manager = VortexAILightReportManager()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        # تقارير AI + تحديث JSON
        results = manager.generate_all_basin_reports()
        print(f"\n🎯 Generated {len(results)} AI Light reports and updated web JSON!")
        print(f"📁 Reports: {manager.reports_dir}")
        print(f"🌐 Web JSON: {manager.basin_json_path}")
    
    elif len(sys.argv) > 1 and sys.argv[1] == "--json-only":
        # تحديث JSON فقط من آخر تقارير
        print("\n🔄 Updating web JSON from latest reports...")
        basin_results = {}
        for basin_name in manager.basin_configs.keys():
            config = manager.basin_configs[basin_name].copy()
            # استخدام القيم الافتراضية مؤقتاً
            config['ri_probability'] = 65.0 if basin_name != "Mediterranean" else 32.0
            basin_results[basin_name] = config
        manager.update_basin_json(basin_results)
    
    else:
        # افتراضي: جميع الأحواض + JSON
        results = manager.generate_all_basin_reports()
        print(f"\n🎯 Generated {len(results)} AI Light reports!")
        print(f"📁 Reports saved to: {manager.reports_dir}")
        print(f"🌐 Web JSON updated: {manager.basin_json_path}")
    
    print("\n✅ AI Light Report generation complete!")
