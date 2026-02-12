#!/data/data/com.termux/files/usr/bin/bash

# ============================================
# VORTEX COMPLETE OPERATIONAL SYSTEM
# Heavy AI → Netlify/public/ → Live Site
# ============================================

echo ""
echo "🌪️  VORTEX OPERATIONAL SYSTEM v2.1"
echo "========================================="
echo ""
echo "📍 Netlify path: /storage/emulated/0/Download/vortex/Netlify/public/"
echo "📍 Live URL:     https://vortex-cyclone.netlify.app"
echo "========================================="
echo ""

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
echo "⏰ Starting: $TIMESTAMP"
echo ""

# Step 1: Run Heavy AI
echo "🧠 [1/4] Running Heavy AI predictions..."
python src/report_manager_heavy_ai.py --all

# Step 2: Deploy to Netlify/public/
echo ""
echo "🚀 [2/4] Deploying to Netlify/public/..."
python src/deploy_to_netlify.py --deploy

# Step 3: Check for Critical Alerts
echo ""
echo "🚨 [3/4] Checking for critical RI events..."
python src/alert_system.py

# Step 4: Show Live Status
echo ""
echo "📊 [4/4] Live System Status:"
echo "========================================="
echo "🌐 Netlify Live:  https://vortex-cyclone.netlify.app"
echo "📁 Heavy AI JSON: https://vortex-cyclone.netlify.app/data/basins_heavy.json"
echo "📁 Light AI JSON: https://vortex-cyclone.netlify.app/data/basins.json"
echo "📁 Status JSON:   https://vortex-cyclone.netlify.app/data/status.json"
echo "========================================="
echo ""
echo "✅ VORTEX System Fully Operational"
echo "⏰ Completed: $(date +"%Y-%m-%d %H:%M:%S")"
echo "========================================="
