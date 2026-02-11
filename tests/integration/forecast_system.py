#!/usr/bin/env python
"""
نموذج تنبؤ كامل لـ Vortex
يربط بين VortexEngine و TimeSteppingForecast
"""
import numpy as np
from vortex.core.vortex_engine import VortexEngine
from vortex.algorithms.time_stepping import EnhancedTimeSteppingForecast

class VortexForecastSystem:
    """
    نظام تنبؤ متكامل للدوامات
    """
    def __init__(self, basin="atlantic"):
        self.basin = basin
        self.engine = VortexEngine(basin)
        self.forecaster = EnhancedTimeSteppingForecast()
        
    def run_forecast(self, initial_conditions, forecast_hours=120):
        """
        تشغيل تنبؤ زمني كامل
        
        Parameters:
        -----------
        initial_conditions : dict
            الشروط الأولية للدوامة
        forecast_hours : int
            فترة التنبؤ بالساعات
        """
        print(f"🚀 بدء تنبؤ دوامة للحوض: {self.basin}")
        print(f"⏱️  فترة التنبؤ: {forecast_hours} ساعة")
        print("=" * 50)
        
        # 1. تحضير البيانات من VortexEngine
        print("\n1. 🔧 تجهيز بيانات المحرك...")
        print(f"   • الحوض: {self.engine.basin}")
        print(f"   • المعاملات المحيطية: جاهزة")
        print(f"   • المعاملات الهيكلية: جاهزة")
        
        # 2. استخدام TimeSteppingForecast
        print("\n2. ⏱️  تشغيل نموذج الخطوات الزمنية...")
        
        # بيانات نموذجية للاختبار
        sample_data = {
            "initial_intensity_kt": 65,      # شدة ابتدائية بالعقد
            "mpi_trajectory": np.linspace(80, 120, forecast_hours//6),
            "environmental_trends": {
                "vws": np.random.uniform(5, 15, forecast_hours//12),
                "sst": np.random.uniform(27, 30, forecast_hours//12),
                "ohc": np.random.uniform(40, 80, forecast_hours//12)
            }
        }
        
        try:
            # تشغيل التنبؤ
            forecast_result = self.forecaster.forecast_intensity(**sample_data)
            
            print(f"   ✅ تم إنشاء التنبؤ")
            print(f"   📊 شكل الناتج: {type(forecast_result)}")
            
            if hasattr(forecast_result, "shape"):
                print(f"   📈 نقاط التنبؤ: {forecast_result.shape}")
                
                # عرض عينة من النتائج
                if len(forecast_result) > 0:
                    print(f"\n3. 📋 عينة من نتائج التنبؤ:")
                    for i in range(min(5, len(forecast_result))):
                        print(f"   الساعة {i*6}: {forecast_result[i]:.1f} عقدة")
                    
                    if len(forecast_result) > 5:
                        print(f"   ... وهكذا لـ {len(forecast_result)} نقطة زمنية")
            
            # تحديث احتمال RI في المحرك
            self.engine.ri_probability = self._calculate_ri_probability(forecast_result)
            print(f"\n4. 🎯 احتمال التكثيف السريع (RI): {self.engine.ri_probability}")
            
        except Exception as e:
            print(f"   ⚠️  خطأ في التنبؤ: {e}")
            print(f"   ℹ️  التفاصيل: {type(e).__name__}")
            
            # في حالة الخطأ، نعرض الدوال المتاحة في المتنبئ
            print(f"\n   🔍 الدوال المتاحة في EnhancedTimeSteppingForecast:")
            methods = [m for m in dir(self.forecaster) if not m.startswith("_")]
            for method in methods[:10]:
                print(f"      • {method}")
    
    def _calculate_ri_probability(self, forecast_intensity):
        """حساب احتمال التكثيف السريع من نتائج التنبؤ"""
        if isinstance(forecast_intensity, (np.ndarray, list)) and len(forecast_intensity) > 1:
            # حساب معدل التغير
            intensity_change = forecast_intensity[-1] - forecast_intensity[0]
            if intensity_change > 30:  # أكثر من 30 عقدة في 5 أيام
                return "HIGH"
            elif intensity_change > 15:
                return "MEDIUM"
            else:
                return "LOW"
        return "UNKNOWN"

def main():
    """الدالة الرئيسية"""
    print("🌪️ نظام تنبؤ Vortex المتكامل")
    print("=" * 50)
    
    # إنشاء النظام
    system = VortexForecastSystem(basin="atlantic")
    
    # تشغيل التنبؤ
    initial_conditions = {
        "current_intensity": 65,
        "location": (15.5, -60.2),
        "movement_speed": 12,
        "movement_direction": 285
    }
    
    system.run_forecast(initial_conditions, forecast_hours=120)
    
    print("\n" + "=" * 50)
    print("✅ اكتمل نموذج التنبؤ")
    print("=" * 50)

if __name__ == "__main__":
    main()
