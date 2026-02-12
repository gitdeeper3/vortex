#!/usr/bin/env python
"""
Vortex Report Manager - AI Enhanced Version
يستخدم جميع تقنيات الذكاء الاصطناعي:
- Random Forest للتنبؤ بـ RI
- Parameters Optimization للمعاملات
- Hybrid Predictor للتنبؤ الهجين
"""
import os
import sys
import datetime
import numpy as np
from pathlib import Path

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir)
sys.path.insert(0, src_dir)

# استيراد نماذج AI
from algorithms.hybrid_predictor import VortexAIPipeline
from algorithms.ri_probability_ml import RIProbabilityML
from algorithms.time_stepping_ai import AITimeSteppingOptimizer, AITimeSteppingForecast
from utils.paths import get_report_path, ensure_directories

class VortexAIReportManager:
    """مدير التقارير بنسخة AI"""
    
    def __init__(self):
        # إنشاء المجلدات
        self.reports_dir = get_report_path("daily")
        ensure_directories()
        
        # تهيئة نظام AI المتكامل
        print("🧠 Initializing Vortex AI System...")
        self.ai_pipeline = VortexAIPipeline()
        
        # تحسين المعاملات
        self.optimizer = AITimeSteppingOptimizer()
        self.optimizer.load_optimal_params()
        
        print(f"📁 Reports directory: {self.reports_dir}")
        print("✅ AI System Ready")
    
    def generate_ai_forecast_report(self, 
                                   basin: str = "Atlantic",
                                   initial_intensity: float = 75.0,
                                   mpi: float = 130.0,
                                   shear: float = 10.0,
                                   sst: float = 28.5,
                                   ohc: float = 75.0,
                                   rh: float = 72.0,
                                   es: float = 0.75,
                                   of: float = 0.65,
                                   llv: float = 12.0,
                                   it: float = 6.0) -> str:
        """
        توليد تقرير باستخدام الذكاء الاصطناعي
        """
        try:
            # تجهيز البيانات للنماذج
            storm_data = {
                'initial_intensity': initial_intensity,
                'mpi': mpi,
                'es': es,
                'of': of,
                'llv': llv,
                'it': it,
                'category': self._get_category(initial_intensity),
                'forecast_hours': 72
            }
            
            environmental_data = {
                'sst': sst,
                'ohc': ohc,
                'vws': shear,
                'rh': rh
            }
            
            # توقع AI متكامل
            print("🤖 Running AI ensemble forecast...")
            ai_forecast = self.ai_pipeline.complete_forecast(
                storm_data, environmental_data
            )
            
            # حساب مستوى الخطر
            ri_prob = ai_forecast['ri_probability'] * 100
            hybrid_intensity = ai_forecast['hybrid_forecast']
            
            if ri_prob >= 70:
                risk_level = "CRITICAL"
                risk_color = "🔴"
            elif ri_prob >= 50:
                risk_level = "HIGH"
                risk_color = "🟠"
            elif ri_prob >= 30:
                risk_level = "MEDIUM"
                risk_color = "🟡"
            else:
                risk_level = "LOW"
                risk_color = "🟢"
            
            # تحسين 24/48/72h توقعات
            intensity_24h = initial_intensity + (hybrid_intensity - initial_intensity) * 0.3
            intensity_48h = initial_intensity + (hybrid_intensity - initial_intensity) * 0.6
            intensity_72h = hybrid_intensity
            
            # إنشاء التقرير
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            
            report = f"""
{'='*60}
VORTEX AI ENHANCED FORECAST - {risk_color} {risk_level} RISK
{'='*60}
Generated: {timestamp} UTC
Basin: {basin}
Model: Hybrid AI (Physical + Machine Learning)

{'='*60}
AI MODEL STATUS
{'='*60}
• Random Forest RI Classifier: {'✅ ACTIVE' if self.ai_pipeline.ri_classifier.trained else '⚠️ BASELINE'}
• Parameter Optimization: {'✅ ACTIVE' if self.optimizer.optimal_params else '⚠️ DEFAULT'}
• Hybrid Predictor: {'✅ ACTIVE' if self.ai_pipeline.hybrid_predictor.trained else '⚠️ PHYSICAL ONLY'}
• Ensemble Confidence: {'HIGH' if self.ai_pipeline.hybrid_predictor.trained else 'MEDIUM'}

{'='*60}
CURRENT STATUS
{'='*60}
Initial Intensity: {initial_intensity:.1f} kt
Maximum Potential: {mpi:.1f} kt
Intensity Deficit: {mpi - initial_intensity:.1f} kt
Saffir-Simpson Category: {self._get_category(initial_intensity)}

{'='*60}
ENVIRONMENTAL CONDITIONS
{'='*60}
Sea Surface Temperature: {sst:.1f} °C
Ocean Heat Content: {ohc:.1f} kJ/cm²
Vertical Wind Shear: {shear:.1f} kt
Mid-Level Humidity: {rh:.1f}%

{'='*60}
STORM STRUCTURE PARAMETERS
{'='*60}
Eyewall Symmetry: {es:.2f}
Outflow Efficiency: {of:.2f}
Low-Level Vorticity: {llv:.1f} (10⁻⁵ s⁻¹)
Intensity Trend: {it:+.1f} kt/12h

{'='*60}
AI ENHANCED FORECAST
{'='*60}
24 hours: {intensity_24h:.1f} kt
48 hours: {intensity_48h:.1f} kt
72 hours: {intensity_72h:.1f} kt

Peak Intensity (AI): {max(intensity_24h, intensity_48h, intensity_72h):.1f} kt
Total Change: {hybrid_intensity - initial_intensity:+.1f} kt

{'='*60}
RAPID INTENSIFICATION ANALYSIS
{'='*60}
AI RI Probability: {ri_prob:.1f}%
Risk Level: {risk_level}

RI Conditions (AI Assessment):
{'✅' if shear < 15 else '❌'} Low Wind Shear ({shear:.1f} kt < 15 kt)
{'✅' if ohc > 60 else '❌'} High Ocean Heat ({ohc:.1f} kJ/cm² > 60)
{'✅' if sst > 28 else '❌'} Warm SST ({sst:.1f}°C > 28°C)
{'✅' if es > 0.7 else '❌'} Symmetric Eyewall ({es:.2f} > 0.7)
{'✅' if of > 0.6 else '❌'} Efficient Outflow ({of:.2f} > 0.6)

{'='*60}
MODEL COMPARISON
{'='*60}
Physical Model Only: {ai_forecast['physical_forecast']:.1f} kt
AI Enhanced Hybrid: {ai_forecast['hybrid_forecast']:.1f} kt
AI Improvement: {ai_forecast['improvement']:+.1f} kt

{'='*60}
OPERATIONAL NOTES
{'='*60}
• AI Model Version: 1.0.0 (Ensemble)
• Training Data: Synthetic (2000 samples)
• Next AI Retraining: Daily
• Next Update: 6 hours
• Forecast ID: {datetime.datetime.now().strftime('%Y%m%d%H%M')}-{basin[:3].upper()}-AI

{'='*60}
"""
            # حفظ التقرير
            filename = f"{datetime.datetime.now().strftime('%Y-%m-%d-%H%M')}-{basin[:3].lower()}-ai-forecast.txt"
            filepath = os.path.join(self.reports_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"✅ AI Report saved: {filepath}")
            print(f"   RI Probability: {ri_prob:.1f}% | Risk: {risk_level}")
            print(f"   AI Improvement: {ai_forecast['improvement']:+.1f} kt")
            
            return str(filepath)
            
        except Exception as e:
            error_msg = f"Error generating AI forecast: {str(e)}"
            print(f"❌ {error_msg}")
            import traceback
            traceback.print_exc()
            return error_msg
    
    def _get_category(self, intensity):
        """تحديد فئة Saffir-Simpson"""
        if intensity < 34: return "Tropical Depression"
        elif intensity < 64: return "Tropical Storm"
        elif intensity < 83: return "Category 1"
        elif intensity < 96: return "Category 2"
        elif intensity < 113: return "Category 3"
        elif intensity < 137: return "Category 4"
        else: return "Category 5"
    
    def train_all_models(self):
        """تدريب جميع نماذج AI"""
        print("\n🧠 Training all AI models...")
        
        # 1. تدريب Random Forest
        print("\n🌲 Training Random Forest RI Classifier...")
        self.ai_pipeline.ri_classifier.train()
        self.ai_pipeline.ri_classifier.save_model()
        
        # 2. تحسين المعاملات
        print("\n🧬 Optimizing physical parameters...")
        historical = self.optimizer.generate_synthetic_historical_data(100)
        self.optimizer.optimize_parameters(historical)
        self.optimizer.save_optimal_params()
        
        # 3. تدريب Hybrid Predictor
        print("\n🤖 Training Hybrid Predictor...")
        training_data = self.ai_pipeline.hybrid_predictor.generate_synthetic_training_data(1000)
        self.ai_pipeline.hybrid_predictor.train(training_data)
        self.ai_pipeline.hybrid_predictor.save_model()
        
        print("\n✅ All AI models trained successfully!")
        return True
    
    def generate_basin_reports_ai(self):
        """توليد تقارير AI لجميع الأحواض"""
        print("\n🌍 Generating AI-enhanced basin reports...")
        
        basins = [
            ("Atlantic", 75.0, 130.0, 10.0, 28.5, 75.0, 72.0, 0.75, 0.65, 12.0, 6.0),
            ("Pacific", 70.0, 125.0, 12.0, 29.0, 80.0, 70.0, 0.73, 0.68, 11.5, 5.5),
            ("Indian", 65.0, 120.0, 14.0, 28.0, 70.0, 68.0, 0.70, 0.62, 10.8, 4.5)
        ]
        
        reports = []
        for basin_config in basins:
            print(f"\n📊 {basin_config[0]} Basin (AI):")
            report_path = self.generate_ai_forecast_report(*basin_config)
            reports.append(report_path)
        
        return reports


if __name__ == "__main__":
    import sys
    
    print("🚀 Vortex AI Report Manager v1.0")
    print("=" * 50)
    
    manager = VortexAIReportManager()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--train":
        # تدريب جميع النماذج
        manager.train_all_models()
        
    elif len(sys.argv) > 1 and sys.argv[1] == "--ai-all":
        # تقارير AI لجميع الأحواض
        reports = manager.generate_basin_reports_ai()
        print(f"\n🎯 Generated {len(reports)} AI-enhanced reports!")
        print(f"📁 Reports saved to: {manager.reports_dir}")
        
    else:
        # تقرير AI واحد
        print("\n📊 Generating single AI forecast...")
        manager.generate_ai_forecast_report("Atlantic")
    
    print("\n✅ AI Report generation complete!")
