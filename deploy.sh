#!/bin/bash
# AI Tools Master - Deploy to Cloudflare Pages
# Prerequisites: wrangler CLI (npm install -g wrangler)
# Run: bash deploy.sh

set -e

echo "=== Building Hugo site ==="
cd "$(dirname "$0")"
hugo --minify

echo ""
echo "=== Deploying to Cloudflare Pages ==="
echo "You need to authenticate with Cloudflare first."
echo "A browser window will open for login."
echo ""
read -p "Press Enter to continue..."

npx wrangler pages deploy public/ --project-name=aitoolsmaster

echo ""
echo "=== Done! ==="
echo "After deployment, go to Cloudflare Dashboard to:"
echo "1. Set custom domain"
echo "2. Enable HTTPS"
echo "3. Configure Google AdSense"
