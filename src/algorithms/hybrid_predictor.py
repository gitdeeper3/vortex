"""
Hybrid Predictor: يجمع بين النموذج الفيزيائي والذكاء الاصطناعي
Physical + Machine Learning ensemble for superior accuracy
"""
import numpy as np
import joblib
import logging
from pathlib import Path
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

class VortexHybridPredictor:
    """
    نظام تنبؤ هجين:
    - 70% نموذج فيزيائي (time-stepping)
    - 30% تعلم آلي (تصحيح الأخطاء)
    
    المزايا:
    - دقة أعلى من النموذج الفيزيائي وحده
    - يتعلم من أخطاء الماضي
    - يتكيف مع أحواض المحيطات المختلفة
    """
    
    def __init__(self):
        self.physical_weight = 0.7
        self.ai_weight = 0.3
        self.error_corrector = None
        self.scaler = StandardScaler()
        self.trained = False
        
    def _get_model_path(self):
        """الحصول على مسار حفظ النموذج الهجين"""
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent
        models_dir = project_root / "models"
        models_dir.mkdir(exist_ok=True)
        return models_dir / "hybrid_predictor.pkl"
    
    def _generate_training_features(self, storm_data, physical_forecast):
        """
        توليد الميزات لتدريب مصحح الأخطاء
        """
        features = []
        
        # الميزات البيئية
        features.append(storm_data.get('sst', 28.5))
        features.append(storm_data.get('ohc', 60.0))
        features.append(storm_data.get('vws', 12.0))
        features.append(storm_data.get('rh', 70.0))
        
        # ميزات الإعصار
        features.append(storm_data.get('initial_intensity', 75.0))
        features.append(storm_data.get('mpi', 130.0))
        features.append(storm_data.get('category', 2))
        
        # ميزات التوقع
        features.append(physical_forecast)
        features.append(storm_data.get('forecast_hour', 72))
        
        return np.array(features)
    
    def train(self, training_data):
        """
        تدريب مصحح الأخطاء
        
        Parameters:
        -----------
        training_data : List[Dict]
            قائمة تحتوي على:
            - storm_data: بيانات الإعصار
            - physical_forecast: توقع النموذج الفيزيائي
            - actual_intensity: الشدة الفعلية
        """
        logger.info("🤖 Training hybrid predictor...")
        
        X = []
        y = []  # خطأ النموذج الفيزيائي
        
        for item in training_data:
            features = self._generate_training_features(
                item['storm_data'],
                item['physical_forecast']
            )
            X.append(features)
            
            error = item['actual_intensity'] - item['physical_forecast']
            y.append(error)
        
        X = np.array(X)
        y = np.array(y)
        
        # تطبيع
        X_scaled = self.scaler.fit_transform(X)
        
        # تدريب نموذج Gradient Boosting
        self.error_corrector = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=4,
            min_samples_split=5,
            min_samples_leaf=3,
            subsample=0.8,
            random_state=42
        )
        
        self.error_corrector.fit(X_scaled, y)
        self.trained = True
        
        # تقييم
        train_score = self.error_corrector.score(X_scaled, y)
        logger.info(f"✅ Training complete!")
        logger.info(f"   R² score: {train_score:.3f}")
        logger.info(f"   Mean absolute error: {np.mean(np.abs(y)):.2f} kt")
        
        return train_score
    
    def predict(self, storm_data, physical_forecast):
        """
        توقع هجين = (0.7 * فيزيائي) + (0.3 * (فيزيائي + تصحيح))
        """
        if not self.trained or self.error_corrector is None:
            logger.warning("⚠️  Error corrector not trained, using pure physical model")
            return physical_forecast
        
        try:
            # توليد الميزات
            features = self._generate_training_features(storm_data, physical_forecast)
            features_scaled = self.scaler.transform([features])
            
            # توقع الخطأ
            predicted_error = self.error_corrector.predict(features_scaled)[0]
            
            # تصحيح التوقع الفيزيائي
            ai_adjusted = physical_forecast + predicted_error
            
            # التوقع الهجين
            hybrid = (self.physical_weight * physical_forecast + 
                     self.ai_weight * ai_adjusted)
            
            return hybrid
            
        except Exception as e:
            logger.error(f"Error in hybrid prediction: {e}")
            return physical_forecast
    
    def generate_synthetic_training_data(self, n_samples=500):
        """
        توليد بيانات تدريب اصطناعية للتجريب
        """
        np.random.seed(42)
        training_data = []
        
        for _ in range(n_samples):
            # بيانات إعصار عشوائية
            storm_data = {
                'sst': np.random.uniform(26, 32),
                'ohc': np.random.uniform(30, 110),
                'vws': np.random.uniform(5, 25),
                'rh': np.random.uniform(50, 90),
                'initial_intensity': np.random.uniform(40, 100),
                'mpi': np.random.uniform(100, 160),
                'category': np.random.randint(0, 5),
                'forecast_hour': np.random.choice([24, 48, 72])
            }
            
            # توقع فيزيائي (به خطأ)
            physical_bias = np.random.normal(-5, 8)
            physical_forecast = (
                storm_data['initial_intensity'] + 
                (storm_data['mpi'] - storm_data['initial_intensity']) * 0.3 +
                physical_bias
            )
            
            # شدة فعلية (الحقيقة)
            actual_intensity = (
                physical_forecast + 
                np.random.normal(0, 5) +
                (storm_data['sst'] - 28) * 2 +
                (25 - storm_data['vws']) * 0.5
            )
            
            training_data.append({
                'storm_data': storm_data,
                'physical_forecast': physical_forecast,
                'actual_intensity': max(0, actual_intensity)
            })
        
        return training_data
    
    def save_model(self):
        """حفظ النموذج الهجين"""
        if not self.trained:
            logger.warning("⚠️  No trained model to save")
            return False
        
        model_path = self._get_model_path()
        try:
            joblib.dump({
                'error_corrector': self.error_corrector,
                'scaler': self.scaler,
                'physical_weight': self.physical_weight,
                'ai_weight': self.ai_weight
            }, model_path)
            logger.info(f"✅ Hybrid model saved to {model_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to save model: {e}")
            return False
    
    def load_model(self):
        """تحميل نموذج مدرب مسبقاً"""
        model_path = self._get_model_path()
        if model_path.exists():
            try:
                saved = joblib.load(model_path)
                self.error_corrector = saved['error_corrector']
                self.scaler = saved['scaler']
                self.physical_weight = saved['physical_weight']
                self.ai_weight = saved['ai_weight']
                self.trained = True
                logger.info(f"✅ Loaded hybrid model from {model_path}")
                return True
            except Exception as e:
                logger.error(f"❌ Failed to load model: {e}")
        return False


# نظام التنبؤ الهجين المتكامل
class VortexAIPipeline:
    """
    نظام AI متكامل يجمع كل التقنيات:
    1. Random Forest لاحتمالية RI
    2. Parameters Optimization للمعاملات
    3. Hybrid Predictor للتنبؤ الهجين
    """
    
    def __init__(self):
        from ri_probability_ml import RIProbabilityML
        from time_stepping_ai import AITimeSteppingForecast
        
        self.ri_classifier = RIProbabilityML()
        self.physical_model = AITimeSteppingForecast()
        self.hybrid_predictor = VortexHybridPredictor()
        
        # محاولة تحميل النماذج المدربة
        self.hybrid_predictor.load_model()
    
    def complete_forecast(self, storm_data, environmental_data):
        """
        توقع كامل بجميع تقنيات AI
        """
        # 1. حساب RI Probability
        ri_features = [
            environmental_data.get('sst', 28.5),
            environmental_data.get('ohc', 60.0),
            environmental_data.get('vws', 12.0),
            environmental_data.get('rh', 70.0),
            storm_data.get('es', 0.7),
            storm_data.get('of', 0.6),
            storm_data.get('llv', 12.0),
            storm_data.get('it', 5.0)
        ]
        ri_probability = self.ri_classifier.predict_proba(ri_features)
        
        # 2. توقع فيزيائي محسن
        physical_forecast = self.physical_model.forecast_intensity(
            storm_data.get('initial_intensity', 75.0),
            [storm_data.get('mpi', 130.0)] * 100,
            {'vws': [environmental_data.get('vws', 12.0)] * 100},
            storm_data.get('forecast_hours', 72)
        )
        
        final_physical = physical_forecast['intensity_forecast_kt'][-1]
        
        # 3. توقع هجين
        hybrid_forecast = self.hybrid_predictor.predict(
            {**storm_data, **environmental_data},
            final_physical
        )
        
        return {
            'ri_probability': ri_probability,
            'physical_forecast': final_physical,
            'hybrid_forecast': hybrid_forecast,
            'improvement': hybrid_forecast - final_physical,
            'ai_enhanced': True
        }


# اختبار
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🤖 Vortex AI - Hybrid Predictor System")
    print("=" * 50)
    
    # إنشاء النظام الهجين
    hybrid = VortexHybridPredictor()
    
    # توليد بيانات تدريب
    print("\n📊 Generating synthetic training data...")
    training_data = hybrid.generate_synthetic_training_data(1000)
    print(f"   Generated {len(training_data)} samples")
    
    # تدريب النموذج
    hybrid.train(training_data)
    
    # حفظ النموذج
    hybrid.save_model()
    
    # اختبار التنبؤ
    print("\n📈 Testing hybrid prediction...")
    test_storm = {
        'sst': 29.0,
        'ohc': 75.0,
        'vws': 12.0,
        'rh': 72.0,
        'initial_intensity': 75.0,
        'mpi': 130.0,
        'category': 2,
        'forecast_hour': 72
    }
    
    physical = 108.0  # توقع فيزيائي
    hybrid_pred = hybrid.predict(test_storm, physical)
    
    print(f"\n   Physical forecast: {physical:.1f} kt")
    print(f"   Hybrid forecast: {hybrid_pred:.1f} kt")
    print(f"   AI correction: {hybrid_pred - physical:+.1f} kt")
    
    print("\n🎯 Hybrid Predictor Ready!")
