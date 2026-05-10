#!/usr/bin/env python3
"""Generate 10 cover images for AI tools review articles via SiliconFlow API."""

import requests
import json
import time
import os
import sys
from pathlib import Path

API_KEY = "sk-oprkkpaskefzpyzyifequbpmdjkqmdkmqdgstvidzkftrmnl"
API_URL = "https://api.siliconflow.cn/v1/images/generations"
OUTPUT_DIR = Path.home() / "Desktop/aitoolsmaster/static/images/posts"

IMAGES = [
    {
        "filename": "ai-writing-tools.webp",
        "prompt": "Minimalist dark workspace with laptop, glowing AI text bubbles floating, blue and purple neon accents, tech magazine style, 1200x628"
    },
    {
        "filename": "ai-image-generators.webp",
        "prompt": "Abstract colorful digital art explosion, neon colors on dark background, AI creating art, futuristic, 1200x628"
    },
    {
        "filename": "ai-coding-assistants.webp",
        "prompt": "Dark code editor screen with glowing green code lines, AI assistant icon in corner, cyberpunk vibe, 1200x628"
    },
    {
        "filename": "ai-video-generators.webp",
        "prompt": "Film reel merging with digital data streams, dark cinema aesthetic, neon blue and red, 1200x628"
    },
    {
        "filename": "ai-voice-generators.webp",
        "prompt": "Sound wave visualization in neon blue on dark background, microphone silhouette, podcast studio feel, 1200x628"
    },
    {
        "filename": "ai-seo-tools.webp",
        "prompt": "Abstract bar chart graph growing upward, search engine result page snippet, dark mode analytics dashboard, 1200x628"
    },
    {
        "filename": "ai-social-media-tools.webp",
        "prompt": "Social media icon constellation (Facebook, Instagram, Twitter logos) on dark gradient background, connected by glowing lines, 1200x628"
    },
    {
        "filename": "free-ai-tools.webp",
        "prompt": "Gift box glowing with neon light, dollar sign with strikethrough, 'FREE' text concept, dark purple background, 1200x628"
    },
    {
        "filename": "ai-productivity-tools.webp",
        "prompt": "Minimalist desk setup with glowing AI assistant orb, calendar and checkmarks floating, dark navy background, 1200x628"
    },
    {
        "filename": "ai-headshot-generators.webp",
        "prompt": "Professional portrait photo half-completed with digital grid lines, before slash after concept, dark blue gradient, 1200x628"
    }
]

def download_image(url, filepath):
    """Download an image from a URL and save to filepath."""
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()
    with open(filepath, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

def generate_image(prompt, filename):
    """Generate an image via SiliconFlow API and save it."""
    output_path = OUTPUT_DIR / filename
    print(f"\n[{filename}] Generating...", flush=True)
    
    payload = {
        "model": "Kwai-Kolors/Kolors",
        "prompt": prompt,
        "n": 1,
        "size": "1200x628"
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        resp = requests.post(API_URL, json=payload, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        
        if "images" in data and len(data["images"]) > 0:
            img_url = data["images"][0]["url"]
            print(f"  Downloading from: {img_url}", flush=True)
            download_image(img_url, output_path)
            file_size = os.path.getsize(output_path)
            print(f"  Saved: {output_path} ({file_size / 1024:.1f} KB)", flush=True)
            return True
        else:
            print(f"  ERROR: No images in response", flush=True)
            print(f"  Response: {json.dumps(data, indent=2)[:500]}", flush=True)
            return False
            
    except Exception as e:
        print(f"  ERROR: {e}", flush=True)
        return False

def main():
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"API URL: {API_URL}")
    print(f"Model: Kwai-Kolors/Kolors")
    print(f"Total images: {len(IMAGES)}")
    
    results = []
    for i, img in enumerate(IMAGES, 1):
        print(f"\n--- Image {i}/{len(IMAGES)}: {img['filename']} ---")
        success = generate_image(img["prompt"], img["filename"])
        results.append((img["filename"], success))
        
        if i < len(IMAGES):
            print("  Waiting 3s before next request...", flush=True)
            time.sleep(3)
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("=" * 60)
    for filename, success in results:
        status = "OK" if success else "FAIL"
        print(f"  [{status}] {filename}")

if __name__ == "__main__":
    main()
