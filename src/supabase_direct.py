"""
VORTEX Supabase Direct Connection
مع SERVICE_ROLE KEY - جلب العدد باستخدام HEAD request
"""
import requests
import json
import datetime
from typing import Dict, List, Optional

class VortexSupabase:
    def __init__(self):
        self.url = "https://ofoylamviehwpeukmdei.supabase.co"
        self.service_key = "sb_secret_pJutKnDxAGGmENW3OATFyQ_U7U59awg"
        self.headers = {
            "apikey": self.service_key,
            "Authorization": f"Bearer {self.service_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        print("=" * 60)
        print("🚀 VORTEX SUPABASE - SERVICE ROLE MODE (FIXED)")
        print("=" * 60)
        print(f"📍 URL: {self.url}")
        print("🔑 Key: SERVICE_ROLE (secure)")
        print("=" * 60)

    def get_total_storms_count(self) -> int:
        """✅ جلب العدد الإجمالي باستخدام HEAD request"""
        try:
            response = requests.head(
                f"{self.url}/rest/v1/storms",
                headers=self.headers,
                params={"select": "storm_id"},  # لا حاجة لـ limit
                timeout=10
            )
            if response.status_code == 200:
                # Supabase يعيد العدد في رأس Content-Range
                content_range = response.headers.get("content-range", "0-0/0")
                total = content_range.split("/")[-1]
                print(f"📊 Total storms in database: {total}")
                return int(total) if total.isdigit() else 0
            else:
                print(f"❌ Failed to get count: HTTP {response.status_code}")
                return 0
        except Exception as e:
            print(f"❌ Error: {e}")
            return 0

    def get_active_storms(self, limit: int = 100) -> List[Dict]:
        """جلب العواصف النشطة"""
        try:
            response = requests.get(
                f"{self.url}/rest/v1/storms",
                headers=self.headers,
                params={
                    "select": "*",
                    "status": "eq.active",
                    "limit": limit,
                    "order": "wind_speed_kt.desc"  # الأقوى أولاً
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Found {len(data)} active storms")
                return data
            else:
                print(f"❌ Error {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Exception: {e}")
            return []

    def get_storm_count_by_basin(self):
        """عدد العواصف حسب الحوض"""
        basins = ['atlantic', 'pacific', 'indian', 'southern']
        print("\n📊 Storms by basin:")
        for basin in basins:
            response = requests.get(
                f"{self.url}/rest/v1/storms",
                headers=self.headers,
                params={
                    "select": "storm_id",
                    "basin": f"eq.{basin}",
                    "limit": 1000
                },
                timeout=5
            )
            if response.status_code == 200:
                count = len(response.json())
                print(f"   {basin}: {count} storms")

if __name__ == "__main__":
    db = VortexSupabase()
    
    # 1. العدد الإجمالي
    total = db.get_total_storms_count()
    
    # 2. العواصف النشطة
    storms = db.get_active_storms(limit=10)
    
    print(f"\n🌀 Top 5 most intense active storms:")
    for i, s in enumerate(storms[:5]):
        wind = s.get('wind_speed_kt', 0)
        cat = s.get('category', '?')
        name = s.get('name', 'Unnamed')
        print(f"   {i+1}. {name}: {wind:.0f} kt (Cat {cat})")
    
    # 3. التوزيع حسب الحوض
    db.get_storm_count_by_basin()
