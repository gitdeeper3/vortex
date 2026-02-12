#!/data/data/com.termux/files/usr/bin/bash

# VORTEX Netlify Auto-Updater
# One-command update for vortex-cyclone.netlify.app

echo "🌪️  VORTEX NETLIFY AUTO-UPDATER"
echo "================================="
echo ""

# Step 1: Run Heavy AI
echo "🧠 Step 1: Running Heavy AI forecasts..."
python src/report_manager_heavy_ai.py --all

# Step 2: Deploy to Netlify
echo ""
echo "🚀 Step 2: Deploying to Netlify..."
python src/deploy_to_netlify.py --deploy

# Step 3: Show completion
echo ""
echo "================================="
echo "✅ UPDATE COMPLETE!"
echo "================================="
echo ""
echo "🌐 Live site: https://vortex-cyclone.netlify.app"
echo "📊 Heavy AI:   https://vortex-cyclone.netlify.app/data/basins_heavy.json"
echo "📊 Light AI:   https://vortex-cyclone.netlify.app/data/basins.json"
echo ""
echo "🕐 Timestamp: $(date)"
