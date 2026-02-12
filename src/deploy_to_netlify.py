#!/usr/bin/env python
"""
VORTEX Netlify Auto-Deploy Script - Enhanced Edition
CORRECT PATH: /storage/emulated/0/Download/vortex/Netlify/public/
"""
import os
import sys
import json
import shutil
import datetime
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir)
sys.path.insert(0, src_dir)

from utils.paths import get_project_root

class VortexNetlifyDeployer:
    def __init__(self):
        self.project_root = get_project_root()
        
        # 🔴 المسار الصحيح لمجلد Netlify/public
        self.netlify_public_dir = self.project_root / "Netlify" / "public"
        self.data_dir = self.netlify_public_dir / "data"
        
        print("🌐 VORTEX Netlify Deployer - Enhanced Edition")
        print("=" * 60)
        print(f"📍 Netlify public folder: {self.netlify_public_dir}")
        print(f"📍 Target URL: https://vortex-cyclone.netlify.app")
        
    def ensure_directories(self):
        """Ensure Netlify/public/data directory exists"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Netlify/public/data directory ready")
        
    def copy_web_files(self):
        """Copy index.html from web/ to Netlify/public/"""
        print("\n📂 Copying web files to Netlify/public...")
        
        # Copy index.html
        web_index = self.project_root / "web" / "index.html"
        netlify_index = self.netlify_public_dir / "index.html"
        
        if web_index.exists():
            shutil.copy2(web_index, netlify_index)
            print(f"  ✅ index.html copied to Netlify/public/")
        else:
            print(f"  ⚠️ web/index.html not found")
        
        return True
    
    def enhance_json_with_metadata(self, json_path):
        """Add timestamp, model version, and confidence to JSON"""
        if not json_path.exists():
            return
            
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add metadata
        data['last_updated'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        data['last_updated_iso'] = datetime.datetime.now().isoformat() + 'Z'
        data['model_version'] = 'Heavy AI v2.1 (LSTM+Transformer)'
        data['next_update'] = (datetime.datetime.now() + datetime.timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S UTC')
        
        # Add confidence display text
        for basin in data.get('basins', []):
            if 'confidence' in basin:
                conf = basin['confidence']
                if conf >= 90:
                    basin['confidence_text'] = 'Very High'
                elif conf >= 80:
                    basin['confidence_text'] = 'High'
                elif conf >= 70:
                    basin['confidence_text'] = 'Good'
                elif conf >= 60:
                    basin['confidence_text'] = 'Moderate'
                else:
                    basin['confidence_text'] = 'Low'
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        return data
    
    def copy_json_data(self):
        """Copy JSON files from web/data/ to Netlify/public/data/"""
        print("\n📊 Copying & Enhancing Heavy AI JSON data...")
        
        source_data_dir = self.project_root / "web" / "data"
        json_files = list(source_data_dir.glob("*.json"))
        
        if not json_files:
            print("  ⚠️ No JSON files found in web/data/")
            return False
            
        for json_file in json_files:
            dst = self.data_dir / json_file.name
            shutil.copy2(json_file, dst)
            
            # Add metadata to the copied file
            self.enhance_json_with_metadata(dst)
            print(f"  ✅ {json_file.name} (enhanced + copied to Netlify/public/data/)")
            
        return True
    
    def create_status_json(self):
        """Create a status endpoint for API health check"""
        status = {
            "status": "operational",
            "model": "VORTEX Heavy AI",
            "version": "2.1",
            "basins": 8,
            "last_update": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
            "next_scheduled_update": (datetime.datetime.now() + datetime.timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S UTC'),
            "endpoints": {
                "light_ai": "/data/basins.json",
                "heavy_ai": "/data/basins_heavy.json",
                "status": "/data/status.json"
            },
            "deploy_path": str(self.netlify_public_dir)
        }
        
        status_path = self.data_dir / "status.json"
        with open(status_path, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2)
        print(f"  ✅ status.json created in Netlify/public/data/")
    
    def generate_netlify_toml(self):
        """Generate netlify.toml in Netlify folder"""
        toml_path = self.project_root / "Netlify" / "netlify.toml"
        
        toml_content = """[build]
  publish = "public"

[[redirects]]
  from = "/data/*"
  to = "/data/:splat"
  status = 200

[[headers]]
  for = "/data/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"
    Cache-Control = "public, max-age=3600"
    Content-Type = "application/json"

[[headers]]
  for = "/"
  [headers.values]
    X-VORTEX-Model = "Heavy AI v2.1"
    X-VORTEX-Basins = "8"
    X-VORTEX-Updated = "UTC"
"""
        with open(toml_path, 'w') as f:
            f.write(toml_content)
        print(f"\n✅ netlify.toml generated in Netlify/ folder")
    
    def deploy(self):
        """Full deployment to Netlify/public/"""
        print("\n🚀 Deploying to Netlify/public/ with Enhanced Metadata...")
        print("=" * 60)
        
        self.ensure_directories()
        self.copy_web_files()
        self.copy_json_data()
        self.create_status_json()
        self.generate_netlify_toml()
        
        print("\n" + "=" * 60)
        print("✅ DEPLOYMENT READY - ENHANCED EDITION")
        print("=" * 60)
        print(f"\n📁 Netlify public folder: {self.netlify_public_dir}")
        print(f"\n🌐 Live URL: https://vortex-cyclone.netlify.app")
        print(f"\n📊 JSON endpoints (live):")
        print(f"   • Light AI:  https://vortex-cyclone.netlify.app/data/basins.json")
        print(f"   • Heavy AI:  https://vortex-cyclone.netlify.app/data/basins_heavy.json")
        print(f"   • Status:    https://vortex-cyclone.netlify.app/data/status.json")
        print(f"\n🕐 Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        return True


class VortexAutoUpdater:
    def __init__(self):
        self.project_root = get_project_root()
        
    def run_heavy_ai(self):
        print("\n🧠 Running VORTEX Heavy AI...")
        print("=" * 60)
        
        from report_manager_heavy_ai import VortexHeavyAIReportManager
        manager = VortexHeavyAIReportManager()
        results = manager.generate_all_heavy_reports()
        return len(results)
    
    def full_update(self):
        """Complete update cycle: Heavy AI → Deploy to Netlify/public/"""
        print("\n🔄 VORTEX AUTO-UPDATE CYCLE - ENHANCED")
        print("=" * 60)
        
        basins = self.run_heavy_ai()
        print(f"\n✅ Heavy AI complete: {basins} basins updated")
        
        self.deploy_to_netlify()
        
        print("\n" + "=" * 60)
        print("🎯 NETLIFY UPDATE COMPLETE!")
        print("=" * 60)
        print("\n🌐 Site is now live with enhanced metadata:")
        print("   https://vortex-cyclone.netlify.app")
        print("\n📁 Deployment path:")
        print(f"   {self.project_root}/Netlify/public/")
        
        return True
    
    def deploy_to_netlify(self):
        deployer = VortexNetlifyDeployer()
        return deployer.deploy()


if __name__ == "__main__":
    import sys
    
    print("🚀 VORTEX Netlify Auto-Deploy - ENHANCED")
    print("=" * 60)
    print("📍 Target: /storage/emulated/0/Download/vortex/Netlify/public/")
    print("📍 Live:   https://vortex-cyclone.netlify.app")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--deploy":
        deployer = VortexNetlifyDeployer()
        deployer.deploy()
        
    elif len(sys.argv) > 1 and sys.argv[1] == "--update":
        updater = VortexAutoUpdater()
        updater.full_update()
        
    else:
        print("\nUsage:")
        print("  --deploy    : Deploy existing files to Netlify/public/")
        print("  --update    : Run Heavy AI + Deploy to Netlify/public/")
        print("\n✅ Correct paths:")
        print("  • Netlify public: /storage/emulated/0/Download/vortex/Netlify/public/")
        print("  • Live URL:      https://vortex-cyclone.netlify.app")
