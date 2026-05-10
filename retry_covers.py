#!/usr/bin/env python3
"""Retry the 2 failed images with a longer delay between them."""

import requests
import json
import time
import os
from pathlib import Path

API_KEY = "sk-oprkkpaskefzpyzyifequbpmdjkqmdkmqdgstvidzkftrmnl"
API_URL = "https://api.siliconflow.cn/v1/images/generations"
OUTPUT_DIR = Path.home() / "Desktop/aitoolsmaster/static/images/posts"

IMAGES = [
    {
        "filename": "free-ai-tools.webp",
        "prompt": "Gift box glowing with neon light, dollar sign with strikethrough, 'FREE' text concept, dark purple background, 1200x628"
    },
    {
        "filename": "ai-productivity-tools.webp",
        "prompt": "Minimalist desk setup with glowing AI assistant orb, calendar and checkmarks floating, dark navy background, 1200x628"
    }
]

def download_image(url, filepath):
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()
    with open(filepath, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

def generate_image(prompt, filename, retries=3):
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
    
    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(API_URL, json=payload, headers=headers, timeout=120)
            
            if resp.status_code == 429:
                wait = 15 * attempt
                print(f"  Rate limited (attempt {attempt}/{retries}). Waiting {wait}s...", flush=True)
                time.sleep(wait)
                continue
            
            resp.raise_for_status()
            data = resp.json()
            
            if "images" in data and len(data["images"]) > 0:
                img_url = data["images"][0]["url"]
                download_image(img_url, output_path)
                file_size = os.path.getsize(output_path)
                print(f"  Saved: {output_path} ({file_size / 1024:.1f} KB)", flush=True)
                return True
            else:
                print(f"  No images in response: {json.dumps(data, indent=2)[:300]}", flush=True)
                return False
                
        except Exception as e:
            print(f"  Attempt {attempt} error: {e}", flush=True)
            if attempt < retries:
                time.sleep(10 * attempt)
    
    return False

for i, img in enumerate(IMAGES, 1):
    print(f"\n--- Retry {i}/2: {img['filename']} ---")
    generate_image(img["prompt"], img["filename"], retries=3)
    if i < len(IMAGES):
        print("  Waiting 10s before next...")
        time.sleep(10)

print("\nDone.")
