"""
RI Probability Calculator - Lightweight Version
لا يحتاج إلى joblib أو scikit-learn
"""
import numpy as np
import json
from pathlib import Path

class RIProbabilityLight:
    """
    نسخة خفيفة من مصنف RI
    تعتمد على قواعد محسنة بدلاً من مكتبات خارجية
    """
    
    def __init__(self):
        self.feature_names = [
            'sst', 'ohc', 'vws', 'rh', 
            'es', 'of', 'llv', 'it'
        ]
        self.weights = {
            'sst': 0.15,
            'ohc': 0.15,
            'vws': 0.15,
            'rh': 0.10,
            'es': 0.15,
            'of': 0.10,
            'llv': 0.10,
            'it': 0.10
        }
    
    def predict_proba(self, features):
        """
        حساب احتمالية RI باستخدام نظام قواعد متقدم
        """
        if isinstance(features, dict):
            f = features
        else:
            f = {
                'sst': features[0],
                'ohc': features[1],
                'vws': features[2],
                'rh': features[3],
                'es': features[4],
                'of': features[5],
                'llv': features[6],
                'it': features[7]
            }
        
        score = 0.0
        
        # SST
        if f['sst'] > 29: score += self.weights['sst'] * 1.0
        elif f['sst'] > 28: score += self.weights['sst'] * 0.8
        elif f['sst'] > 27: score += self.weights['sst'] * 0.5
        elif f['sst'] > 26: score += self.weights['sst'] * 0.2
        
        # OHC
        if f['ohc'] > 90: score += self.weights['ohc'] * 1.0
        elif f['ohc'] > 70: score += self.weights['ohc'] * 0.8
        elif f['ohc'] > 50: score += self.weights['ohc'] * 0.5
        elif f['ohc'] > 30: score += self.weights['ohc'] * 0.2
        
        # VWS
        if f['vws'] < 8: score += self.weights['vws'] * 1.0
        elif f['vws'] < 12: score += self.weights['vws'] * 0.8
        elif f['vws'] < 16: score += self.weights['vws'] * 0.5
        elif f['vws'] < 20: score += self.weights['vws'] * 0.2
        
        # RH
        if f['rh'] > 80: score += self.weights['rh'] * 1.0
        elif f['rh'] > 70: score += self.weights['rh'] * 0.8
        elif f['rh'] > 60: score += self.weights['rh'] * 0.5
        elif f['rh'] > 50: score += self.weights['rh'] * 0.2
        
        # ES
        if f['es'] > 0.85: score += self.weights['es'] * 1.0
        elif f['es'] > 0.75: score += self.weights['es'] * 0.8
        elif f['es'] > 0.65: score += self.weights['es'] * 0.5
        elif f['es'] > 0.55: score += self.weights['es'] * 0.2
        
        # OF
        if f['of'] > 0.75: score += self.weights['of'] * 1.0
        elif f['of'] > 0.65: score += self.weights['of'] * 0.8
        elif f['of'] > 0.55: score += self.weights['of'] * 0.5
        elif f['of'] > 0.45: score += self.weights['of'] * 0.2
        
        # LLV
        if f['llv'] > 18: score += self.weights['llv'] * 1.0
        elif f['llv'] > 14: score += self.weights['llv'] * 0.8
        elif f['llv'] > 10: score += self.weights['llv'] * 0.5
        elif f['llv'] > 6: score += self.weights['llv'] * 0.2
        
        # IT
        if f['it'] > 12: score += self.weights['it'] * 1.0
        elif f['it'] > 8: score += self.weights['it'] * 0.8
        elif f['it'] > 4: score += self.weights['it'] * 0.5
        elif f['it'] > 0: score += self.weights['it'] * 0.2
        
        return min(0.95, score)
