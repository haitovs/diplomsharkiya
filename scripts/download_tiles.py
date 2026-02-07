import os
import requests
import math
import time

# Configuration
ZOOM_LEVELS = range(10, 15)  # 10 to 14
# Approximate Bounding Box for Ashgabat
# North: 38.02, South: 37.88, West: 58.28, East: 58.48
LAT_MIN = 37.88
LAT_MAX = 38.02
LON_MIN = 58.28
LON_MAX = 58.48

OUTPUT_DIR = "src/assets/tiles"
USER_AGENT = "SharkiyaEventDiscovery/1.0"

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def download_tile(z, x, y):
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    path = f"{OUTPUT_DIR}/{z}/{x}/{y}.png"
    
    if os.path.exists(path):
        return  # Skip if exists

    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    try:
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            with open(path, "wb") as f:
                f.write(resp.content)
            print(f"Downloaded: {z}/{x}/{y}")
            time.sleep(0.1)  # Respect usage policy
        else:
            print(f"Failed: {url} ({resp.status_code})")
    except Exception as e:
        print(f"Error {url}: {e}")

def main():
    print("🌍 Starting tile download for Ashgabat...")
    for z in ZOOM_LEVELS:
        x_min, y_min = deg2num(LAT_MAX, LON_MIN, z) # Top-Left
        x_max, y_max = deg2num(LAT_MIN, LON_MAX, z) # Bottom-Right
        
        # Swap if needed (y increases downwards)
        if y_min > y_max: y_min, y_max = y_max, y_min
        
        print(f"Zoom {z}: X[{x_min}-{x_max}], Y[{y_min}-{y_max}]")
        
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                download_tile(z, x, y)

    print("✅ Download complete!")

if __name__ == "__main__":
    main()
